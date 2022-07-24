---
canonical_url: https://networkandcode.hashnode.dev/online-shop-with-nextjs-and-harperdb
categories: harperdb, material-ui, nextjs, stripe
date: 2021-06-30
tags: harperdb, material-ui, nextjs, stripe
title: Online shop with NextJS and HarperDB
---

*This post appeared on [hashnode.dev](https://networkandcode.hashnode.dev/online-shop-with-nextjs-and-harperdb)*

Hey All, this post is for someone who wants to build or run an online shop with minimal instructions. The code is available at https://github.com/networkandcode/shop and a sample deployment is available at https://shop-two-chi.vercel.app/

This should help deploying a small site with hundreds of items, if not thousands. So far, I have managed to add features to this site such as authentication, categories, sub categories, items, checkout etc. A todo list is being tracked [here](https://github.com/networkandcode/shop/blob/main/TODO.md).

# Environment Variables
I am beginning with env vars cause thats what is mainly needed for the deployment part and then will take you through some of the setup and walkthrough. The following environment variables need to be added, either to .env.local or at platforms such as Vercel before deploying. The names of the environment variables are self explanatory.

```
# Stripe keys
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY
STRIPE_SUCCESS_URL
STRIPE_CANCEL_URL

# Company details
NEXT_PUBLIC_COMPANY_NAME="Shop"
NEXT_PUBLIC_HTML_TITLE="Buy Food Items, Apparel, and Accessories at best price."
NEXT_PUBLIC_MY_DOMAIN="example.com"
NEXT_PUBLIC_SUB_TITLE_1="Affordable rates and best quality assured."
NEXT_PUBLIC_SUB_TITLE_2="COD is available at select locations."
#NEXT_PUBLIC_YOUTUBE_URL="https://youtube.com/c/<ChannelName>"
#NEXT_PUBLIC_WHATSAPP_NUMBER=<phone-number-with-country-code>

# Admin email
NEXT_PUBLIC_ADMIN = "admin@example.com"

# HarperDB
HDB_PASSWORD
HDB_USERNAME
NEXT_PUBLIC_HDB_PASSWORD
NEXT_PUBLIC_HDB_SCHEMA
NEXT_PUBLIC_HDB_URL
NEXT_PUBLIC_HDB_USERNAME

# Color
NEXT_PUBLIC_THEME_COLOR
NEXT_PUBLIC_THEME_COLOR_SEC
```

With  no other customization in the code, if you manage to update just the variables above, you should have a decent site. However, you need to setup the services appropariately before gaining there credentials :). 

# HarperDB Setup
I have used HarperDB studio for setting up the following

## Tables 
- attributes: To store all fixed attributes for an item, something that a buyer can not change, but just view.
- cart_items
- categories : all the categories and sub categories.
- favorites
- items
- variable_attributes (attributes that can be changed by the buyer)

## Roles
- super_user role, this is present by default, it has admin access to all tables
- read_only role, to read data from all tables except cart_items and favorites

## Users
Two users, one with super_user role(refers to env varaible HDB_USERNAME) and one with read_only role(refers to NEXT_PUBLIC_HDB_USERNAME).

The read only user is used for accessing items and categories publicly from the client(browser), and the super user with privileged access is used for operations such as modifying items, updating cart, via the server. Note that variables that start with NEXT_PUBLIC are accessible from the client itself.

## Attributes
The attributes and variable_attributes records are modified directly via the HarperDB studio at the moment, and not through code. Sample records and screenshots are below.

```
{
  name: 'Pattern',
  values: [
    'Checks',
    'Stripes',
    'Plain',
    'Printed'
  ]
}
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625058393289/prsjXGdLh.png)

```
{
  name: 'Size',
  values: [
    'xs',
    's',
    'm',
    'l',
    'xl',
    'xxl',
    'xxxl'
  ]
}
```
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625052460346/2pw4QmrVC.png)

# Admin walkthrough

## Sign in

Click the PowerSettings icon at the top right
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625069481028/8LFiOxGP7.png)
and then login with your admin email and password

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625069609997/Qr2vsQiJM.png)

Cick on the supervisor icon to add items or categories
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625069773105/Y4etMiGhcq.png)

## Add items
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625069860641/RHGtpad5a.png)
Here you can enter the name, description and price of the item. You have to select the category or subcategory from the drop-down list. And finally upload a relevant image for the item.

## Add categories
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625069910383/052VT2p2W.png)
Enter the name of the category to be created, select a parent category only if you are creating a sub category. And select the fixed(buyers can't change) and variable(buyers can change) attributes if required. And finally upload a relevant image for the category. Please do not include '/' in the category name.

# Buyer walk through
Signin just like admin, and select a category from the homepage, for example Accessories, it has 1 item as shown in parantheses.

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625073267307/7rDvOGcj-.png)

Click on the Item pic

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625071073867/jNxqfqr-M.png)
 This opens up a dialog, set the quantity and any other attributes if applicable and update the cart.

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625071190425/R5cMXAQZnG.png)

Once the cart is updated, the dialog can be closed. The checkout icon at the appbar should show the total cart amount. 
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625071317667/FQFbRXeoI.png)
Clicking on that would take you to the checkout  page

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625071376365/AnayvtSTc.png)

Click on proceed to pay, and then the proceed to payment gateway button 
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625072159097/cwZdhOAgF.png)

The email will be populated automatically, fill rest of the details and pay, If you have used stripe's test api key, you can enter the card number as 4242 4242 4242 4242. Click pay and you are done.

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625072375067/ZQ9Kfk1XB.png)

Well, thats the overview of the website I have developed for the #HarperDBHackathon, hope it has some stuff in it, and there could definitely be bugs, and lots of room for improvement. Suggestions are welcome, and thank you @[Hashnode](@hashnode) and HarperDB for the opportunity.

Here is some final notes on what I liked about HarperDB:
- Tabular and JSON way of representing records (in the studio).
- Support for both SQL and NoSQL queries.
- Good reference to multiple libraries(I have chosen fetch and axios), on the docs site.
- Roles are neat, no confusion, no complexity, anyone can easily understand what they mean.

*Credits:  Firebase(for authentication and storage), HarperDB, @hashnode, Material-UI, NextJS, ReactJS, Stripe, Unsplash, Vercel, and lots of other great online resources*

--end-of-post--

