---
canonical_url: https://dev.to/networkandcode/setup-iot-core-on-google-cloud-with-terraform-4h6a
categories: cloud, googlecloud, iot, terraform
cover_image: https://source.unsplash.com/featured/?iot
tags: cloud, googlecloud, iot, terraform
title: Setup IoT core on Google cloud with Terraform
---

Hello :wave:, we shall see how to provision a minimal IoT infrastructure on Google cloud with Terraform.

I shall be doing this straight on the Google cloud shell...

## Project
Set your gcloud config...

Get you projects list and set one of the projects as the current project.
```
$ gcloud projects list

$ gcloud config set project <project-id>
```

## Directories
Let's create two directories for the terraform resources, one for the service account and another for rest of the resources.
```
$ mkdir ~/sa
$ mkdir ~/iot
```
and one more hidden directory for storing the keys/certificates.
```
$ mkdir ~/.auth
```

## TF Provider
We would set the Terraform provider configuration here.

Get the list of zones in the specific region. Note that cloud IoT is currently supported in  these regions: asia-east1, europe-west1, us-central1.
```
$ gcloud compute zones list --filter="region~asia-east1" | grep -i name
NAME: asia-east1-b
NAME: asia-east1-a
NAME: asia-east1-c
```

I would be using zone c.

Set the provider details in terraform with the available information.
```
$ cat ~/sa/main.tf 
provider "google" {
    project = "<project-id>"
    region = "asia-east1"
    zone = "asia-east1-c"
}

$ cp ~/sa/main.tf ~/iot/main.tf
```

## Service account
We are going to create a service account from our user account, which could be further used for creating other resources using terraform.
```
$ ls ~/sa
main.tf  outputs.tf  sa.tf

$ cat ~/sa/sa.tf
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account

resource "google_service_account" "iot_sa" {
  account_id   = "iot-sa"
  display_name = "IoT Service Account"
}

# note this requires the terraform to be run regularly
resource "time_rotating" "iot_sa_key_rotation" {
  rotation_days = 30
}

resource "google_service_account_key" "iot_sa_key" {
  service_account_id = google_service_account.iot_sa.name

  keepers = {
    rotation_time = time_rotating.iot_sa_key_rotation.rotation_rfc3339
  }
}

resource "google_project_iam_member" "iot_editor" {
  project = var.project_id
  role    = "roles/cloudiot.editor"
  member  = "serviceAccount:${google_service_account.iot_sa.email}"

  condition {
    title       = "expires_after_2022_07_31"
    description = "Expiring at midnight of 2022-07-31"
    expression  = "request.time < timestamp(\"2022-08-01T00:00:00Z\")"
  }
}

resource "google_project_iam_member" "pub_sub_editor" {
  project = var.project_id
  role    = "roles/pubsub.editor"
  member  = "serviceAccount:${google_service_account.iot_sa.email}"

  condition {
    title       = "expires_after_2022_07_31"
    description = "Expiring at midnight of 2022-07-31"
    expression  = "request.time < timestamp(\"2022-08-01T00:00:00Z\")"
  }
}

$ cat ~/sa/variables.tf
variable "project_id" {
  type = string
  default = "<project-id>"
}

$ cat ~/sa/outputs.tf
output "iot_sa_private_key" {
  description = "Private key of the IoT service account"
  value       = google_service_account_key.iot_sa_key.private_key
  sensitive = true
}
```

So we are creating a service account with editor roles on IoT core & Pub/Sub, a key for the service account with rotation, and then we would output the private key to save it locally for future use.

## API
We have to enable the Cloud IoT [API](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_service), you can get the fqdn of it using `$ gcloud services list --available --filter="name~.*iot.*"`. Let's add the terraform configuration which can enable it.
```
$ cat ~/sa/variables.tf
variable "project_id" {
  type = string
  default = "<project-id>"
}

$ cat ~/sa/apis.tf
resource "google_project_service" "cloudiot" {
  project = var.project_id
  service = "cloudiot.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_dependent_services = true
}
```

## Apply
We can now create the service account, it's associated resources, and enable the Cloud IoT API.
```
$ cd ~/sa
$ terraform init

# optional, to know what will be  changed
$ terraform plan

$ terraform apply --auto-approve
```

## Validate
Validate the service account creation, via the console.
![Service account](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/osu1meit8btydayjxdx9.png)

And the roles attached to it.
![Service account roles](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yg9mlgi34dhr1jgbe229.png) 

## Key
The private key of the service account could be retrieved from the terraform output.
```
$ terraform output -raw iot_sa_private_key | base64 -d > ~/.auth/iot_sa_private_key.json
```
We have saved the base64 decoded private key in a hidden auth directory at home.

## Credentials
We could now start using the service principal's private key as  a credential for rest of our Terraform activities, for which we have to set an environment variable.
```
$ export GOOGLE_APPLICATION_CREDENTIALS=~/.auth/iot_sa_private_key.json
```

Note: to remove the credential anytime, jus run `unset GOOGLE_APPLICATION_CREDENTIALS`

## Certificate
The connection between the IoT devices and Google IoT core would be secure over TLS, hence a [certificate](https://cloud.google.com/iot/docs/create-device-registry#create_your_credentials) should be generated for our virtual device.
```
$ openssl req -x509 -newkey rsa:2048 -keyout ~/.auth/rsa_private.pem -nodes -out ~/.auth/rsa_cert.pem -subj "/CN=unused"

$ ls ~/.auth/ | grep pem
rsa_cert.pem
rsa_private.pem
```
The private key is in rsa_private.pem and the public certificate is in rsa_cert.pem.

We would keep the private key locally and refer to it while generating a client connection from our device(we are not dealing with the client side of things in  this post though), where as the public certificate would be attached to the remote side, in this case, the IoT core.

## Registry
Add the [terrafaorm](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudiot_registry) configuration for the device registry, pub/sub topics it would use.
```
$ cd ~/iot

$ cat registry.tf
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudiot_registry

resource "google_cloudiot_registry" "iot-registry" {
  name     = "iot-registry"

  event_notification_configs {
    pubsub_topic_name = google_pubsub_topic.additional-telemetry.id
    subfolder_matches = "test/path"
  }

  event_notification_configs {
    pubsub_topic_name = google_pubsub_topic.default-telemetry.id
    subfolder_matches = ""
  }

  state_notification_config = {
    pubsub_topic_name = google_pubsub_topic.default-devicestatus.id
  }

  mqtt_config = {
    mqtt_enabled_state = "MQTT_ENABLED"
  }

  http_config = {
    http_enabled_state = "HTTP_ENABLED"
  }

  log_level = "INFO"
}
```
We would be using 3 topics, all messages published by the client to the path /devices/DEVICE_ID/events would go to the default telemetry topic, and all messages for /devices/DEVICE_ID/state would go to the default device state topic. We have one additional topic with sub folder path "test/path" which means the messages published to /devices/DEVICE_ID/events/test/path would land there.

## Pub/Sub
A separate file for creating the pub/sub topics which will be linked to the registry.
```
resource "google_pubsub_topic" "default-devicestatus" {
  name = "default-devicestatus"
}

resource "google_pubsub_topic" "default-telemetry" {
  name = "default-telemetry"
}

resource "google_pubsub_topic" "additional-telemetry" {
  name = "additional-telemetry"
}
```
## Devices
We would be creating two devices, a basic one which should bind with the gateway, and an advanced device that could be standalone with out a gateway.

The authentication for the basic device will be handled by the gateway and hence, we don't have to set any credentials for the basic device.
```
$ cat basic-device.tf
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudiot_device

resource "google_cloudiot_device" "basic-device" {
  name     = "basic-device"
  registry = google_cloudiot_registry.iot-registry.id  
}

$ cat advanced-device.tf
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudiot_device

resource "google_cloudiot_device" "advanced-device" {
  name     = "advanced-device"
  registry = google_cloudiot_registry.iot-registry.id

  credentials {
    public_key {
        format = "RSA_X509_PEM"
        key = file("~/.auth/rsa_cert.pem")
    }
  }
}
```

## Gateway
And now the gateway.
```
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudiot_device

resource "google_cloudiot_device" "iot-gateway" {
  name     = "iot-gateway"
  registry = google_cloudiot_registry.iot-registry.id 

  credentials {
    public_key {
        format = "RSA_X509_PEM"
        key = file("~/.auth/rsa_cert.pem")
    }
  }

  gateway_config {
    gateway_type = "GATEWAY"
    gateway_auth_method = "ASSOCIATION_ONLY"
  }
}
```
I have setup ASSOCIATION_ONLY as the auth method, which means the device I will bind to this gateway would rely on this gateway for authentication and woudln't authenticate with its own credential.

## Apply
The resources can be created.
```
$ terraform init

# optional, to see what will change
$ terraform plan

$ terraform apply
```

## Bind
The basic device should be bounded with the gateway, so that the gateway generate JWTs on behalf of the device.
```
$ gcloud iot devices gateways bind --gateway iot-gateway --gateway-region asia-east1 --gateway-registry iot-registry --device basic-device --device-region asia-east1
```
I used gcloud for binding the device with the gateway as I was not able to quite find it in the terraform registry.

## Validate
Finally, check the resources on the console.

*Registry*
![Registry](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vy51868va1nsh7wet6b4.png)
 
*Devices*
![Devices](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aikr23urwn2o5sj9h9qu.png)

*Gateway*
![Gateway](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tayjuc9w5we9nwmsawrj.png)

*Device binding*
![Device binding](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f65crdcmkjl60zzu6u3b.png)

Seems all good :)

## Graph
Let's look at the graph that terraform can generate. We can view it on the cloud shell editor itself.

```
$ terraform graph | dot -Tsvg > graph.svg

$ ls *.svg
graph.svg
```

![Graph](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yobgj0gj78kor9hxoymo.png)
 
With this the post is complete, thanks for reading !!!
