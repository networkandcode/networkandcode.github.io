export interface WorkRole {
  company: string;
  role: string;
  location: string;
  period: string;
  highlights: string[];
}

export const workExperienceAchievements: WorkRole[] = [
  {
    company: "UST",
    role: "Solution Architect I - Enterprise Solutions",
    location: "Trivandrum, India",
    period: "Jun 2019 – Present",
    highlights: [
      "Led development of AI chatbot with generative and agentic AI capabilities (observability, business insights, web automation, cost analysis with MCP tools and RAG).",
      "Designed and developed an AI-powered Data Analytics agent with failure handling, retry logic, and improved UX for tool progress messages.",
      "Built and deployed a FinOps agent with Langfuse integration for cost observability, including Helm-based deployment and Dockerized packaging on AWS.",
      "Diagnosed and resolved production issues in a Slack-based conversational agent — fixing memory/context retention and message summarization capabilities.",
      "Set up CDK infrastructure for FinOps cloud resources in AWS (Astra account), following IaC best practices.",
      "Implemented Slack OAuth MCP for per-user credential management and integrated a Slack Remote MCP Server for seamless MCP framework communication.",
      "Owned end-to-end development and delivery of microservices integrated with Envoy gateway and OIDC-based authentication with Keycloak.",
      "Established GitHub Actions-based reusable workflows for application and infrastructure code.",
      "Led development of observability stacks with 200+ reusable assets; managed Agile projects, mentored teams, and drove knowledge sharing.",
      "Built OpenTelemetry compatible observability solutions with Helm charts, dashboards, and alerting templates for Grafana, Prometheus, Mimir, Loki, Tempo, and Keycloak on Kubernetes & GCP.",
      "Implemented executive and operations hierarchical/drilldown dashboards for AKS, Confluent Kafka, APM, and Linux system metrics in Grafana.",
      "Deployed Confluent Kafka on Kubernetes (CFK), integrated it with LDAPS, enabled RBAC, and implemented traffic routing with Istio in TLS pass-through mode.",
      "Supported setup of CI/CD with Jenkins and Harness for 30+ microservices and their migration from OpenShift to AKS.",
      "Provided solution for automated onebox deployments with ArgoCD, Argo Workflows, Helm, Jenkins, and Python.",
      "Developed Apache Beam Dataflow jobs in Python to ingest data from GCP Pub/Sub to MongoDB.",
      "Implemented DevOps environment on Azure with Terraform, Jenkins, Spinnaker, Helm, and Kubernetes (AKS)."
    ]
  },
  {
    company: "Juniper Networks",
    role: "Product Consultant 3",
    location: "Bangalore, India",
    period: "Feb 2019 — Jun 2019",
    highlights: [
      "Individual technical contributor for drafting LLDs/HLDs, simulating labs on VMM, and assisting ISP customers with deployment & support in testbeds/POCs and Production.",
      "Executed design, validation, testing, deployment, acceptance testing, knowledge transfer, and post-installation support.",
      "Installed AppFormix on standalone, Kubernetes, and VMware ESXi platforms.",
      "Installed Contrail HealthBot in a multi-node environment using Docker Swarm.",
      "Contributed to internal GIT Wiki with guides on installing HealthBot, AppFormix, and Contrail Networking in OpenStack environments.",
      "Worked on JunOS Space/ServiceNow project fixing incident generation and SFTP access issues, and upgraded AI scripts on SRX."
    ]
  },
  {
    company: "Mphasis Ltd",
    role: "Sr. Principal Infrastructure Engineer",
    location: "Chennai, India",
    period: "Sep 2016 — Jan 2019",
    highlights: [
      "Led a team of 10+ members, managing task assignments, activity reports, performance ratings, and nominations — team contributed 40+ SOPs, 50+ client appreciations, and 20+ monthly awards.",
      "Implemented LAN & WLAN setups of 50+ sites in APJ & EMEA with varying scopes (new setups, migrations, split-up & mergers, decommissioning).",
      "Developed Python-based scripts/tools (CLI & GUI using Paramiko, Netmiko, Tkinter, Kivy) for day-to-day tasks: configuration templates, CMDB audits, bulk DNS/ping, and regex config pattern search.",
      "Utilized multithreading and multiprocessing in Python code to accelerate network script execution time.",
      "Automated SSH hardening on 3K+ HP Comware devices and TACACS domain/server migration for 5K+ HP Comware/Cisco IOS devices.",
      "Conducted upskilling sessions on Python for network automation, Linux for networking, NETCONF, and OpenStack administration."
    ]
  },
  {
    company: "HCL Technologies",
    role: "Sr. Analyst",
    location: "Chennai, India",
    period: "Mar 2015 — Aug 2016",
    highlights: [
      "Global IT Networks Business Onboarding team: network design, implementation, and project coordination for business expansion, redesign, and migrations.",
      "Designed end-to-end networks, prepared RFPs, HLDs, LLDs in Visio, and BOMs for LAN/WLAN/WAN inventory and links.",
      "Implemented Microsoft Azure ExpressRoute setups, IPsec (Client-to-Site / Site-to-Site) / MPLS L3 VPNs, and shared/dedicated LANs.",
      "Installed and configured new Cisco IOS and Juniper JunOS EX/MX devices, setting up OSPF and BGP routing protocols."
    ]
  },
  {
    company: "BRT India",
    role: "Sr. Network Engineer",
    location: "Chennai, India",
    period: "May 2013 — Mar 2015",
    highlights: [
      "Prepared low-level designs (LLDs) with firm architectural quotes for enterprise LAN/WAN deployments and MPLS provider integrations.",
      "Followed ITIL change management processes for adding VLANs, VRFs, and IP VPN routes towards shared internet gateways.",
      "Provisioned Cisco and Juniper routing and switching equipment with OSPF and BGP configurations, providing handover and UAT to global NOC."
    ]
  },
  {
    company: "Sutherland Global Services",
    role: "Sr. Consultant",
    location: "Cochin, India",
    period: "Feb 2012 — Sep 2012",
    highlights: [
      "Delivered Tier-3 technical escalation support over phone, chat, and remote desktop for complex enterprise networking devices, links, and system peripherals.",
      "Configured network router port forwarding, NAT, and remote access protocols to troubleshoot CCTV, system services, and device connectivity.",
      "Diagnosed and resolved advanced operating system errors, software networking configurations, and application protocols."
    ]
  },
  {
    company: "CSS Corp",
    role: "Sr. Support Engineer",
    location: "Chennai, India",
    period: "Mar 2011 — Feb 2012",
    highlights: [
      "Provided technical assistance for VoIP gateway installations, VoIP adapter line provisioning, audio packet routing, and call completion troubleshooting.",
      "Configured and resolved connectivity issues on network modems, routers, VoIP devices, and enterprise telecommunications equipment for US & Canada clients.",
      "Maintained 100% CSAT ratings while meeting SLA requirements on incoming enterprise technical escalations."
    ]
  },
  {
    company: "Gecom",
    role: "Sr. Project Engineer",
    location: "Bahrain",
    period: "Jan 2010 — Jan 2011",
    highlights: [
      "Site survey, installation, commissioning, documentation, maintenance, and support for modems/routers/WAPs/switches, PBX, CCTVs/DVRs, biometric infra, and Clipsal C-Bus intelligent lighting automation.",
      "Orchestrated Clipsal C-Bus intelligent lighting automation wiring and switch event programming for Ministry projects and World Trade Center maintenance.",
      "Deployed CCTV & Security Panel systems at ATMs and bank premises."
    ]
  }
];
