A project created based on the REST APIs with Flask and Python course taught by Jose Salvatierra

# API Docs

## /register
User authentication is required when using "unsafe" requests, which including POST, DELETE, and PUT, since these methods modify our database. This endpoint is used to register a new user.
```
Header:
    Content-Type: application/json

Body:
{
    "username": <string:username>       #required
    "password": <string:password>       #required
}
```
#### Successful Request
When an user is created successfully, a 201 Created response will be sent back, alongside with this message:
```
{
    "message": "User created successfully."
}
```
#### Unsuccessful Request
When an user with this username already exists in our database, a 400 Bad Request response will be sent back, alongside with this message:
```
{
    "message": "A user with that username already exists."
}
```
In case you forgot to put an username, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": {
        "username": "Username cannot be blank."
    }
}
```
The same thing happens when you forget to put a password, a 400 Bad Request response will be returned with this message:
```
{
    "message": {
        "password": "Password cannot be blank."
    }
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to create this user."
}
```
## /auth
Once you create an user in our server, you can retrieve the access token anytime you want! This endpoint will return an access token whenever a registered user information is provided.
```
Header:
    Content-Type: application/json

Body:   
{
    "username": <string:username>       #required    
    "password": <string:password>       #required
}
```
#### Successful request
When a registered user with correct password requests successfully, a 200 OK response will be sent back, alongside with the access token:
```
{
    "access_token": <string:access_token>
}
```
#### Unsuccessful request
In case you forgot to put an username, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": {
        "username": "Username cannot be blank."
    }
}
```
The same thing happens when you forget to put a password, a 400 Bad Request response will be returned with this message:
```
{
    "message": {
        "password": "Password cannot be blank."
    }
}
```
When the client enters an unregistered user, or an registered user with incorrect password, or missing either password or username, a 401 Unauthorized response will be sent back, alongside with this message:
```
{
    "description": "Invalid credentials",
    "error": "Bad Request",
    "status_code": 401
}
```

## GET /store_list
We have some items, now we need to put them in some stores for others to buy! This endpoint helps us acknowledge what stores we currently have! Just a quick reminder, don't forget to put some stores in the database first!
```
No request body needed.
```
#### Successful request
Whatever the request is, there is always a 200 OK response with our stores (none or many):
```
[
    {
        "store_id": <int:store_id>,
        "name": <string:name>,
        "items": [
            item1_info,...
        ]
    }
]

```

## GET /stores/store_id
With this endpoint we can easily access to a particular store we currently have in our database, and all the items in this store as well! Just a quick reminder, don't forget to put the store_id!
```
No request body needed.
```
#### Successful request
In case you find your store, congratulations! There is always a 200 OK response with your store as well:
```
{
    "store_id": <int:store_id>,
    "name": <string:name>,
    "items": [
        item1_info,...
    ]
}
```
#### Unsuccessful request
Too bad we cannot find your store! We return a 404 Not Found response to notify you that:
```
{
    "message": "Store not found."
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to get this store."
}
```

## POST /stores
With this endpoint we can easily upload our favorite store we currently have to our database!
```
Header:
    Content-Type: application/json
    Authorization Required

Body:
{
    "name': <string:name>             #required
}
```
#### Successful request
In case we can upload your store, congratulations! We return a 201 Created response with your store as well:
```
{
    "store_id": <int:store_id>,
    "name": <string:name>,
    "items": [
        item1_info,...
    ]
}
```
#### Unsuccessful request
In case you forgot to put a store name, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": "This store needs a name."
}
```
Did you forget to authorize yourself? You bet. Since our stores are important, we cannot allow anyone to go and just upload some random stores! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to post this store."
}
```

## DELETE /stores/<int:store_id>
With this endpoint we can easily remove our unwanted store we currently have in our database! Just a quick reminder, remove all the items in the store before deleting the store!
```
Header:
    Authorization Required
```
#### Successful request
In case we can remove the store you hated, congratulations! We return a 200 OK response with this message:
```
{
    "message": "Store deleted."
}
```
#### Unsuccessful request
We found the store, but there are some items in this store, so we cannot just remove it! A 400 Bad Request for you to make sure delete all the items in the store before deleting the store!
```
{
    "message": "This store still contains some items."
}
```
In case you forgot to put a store name, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": "This store needs a name."
}
```
Did you forget to authorize yourself? You bet. Since our stores are important, we cannot allow anyone to go and just delete some random stores! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
Too bad we cannot find the store you hated, maybe it was removed a long time ago! A 404 Not Found response will be return with this message:
```
{
    "message": "Store not found."
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to delete this store."
}
```

## PUT /stores/<int:store_id>
Did you put wrong information about your favorite store into the database? Well, you can simply use this PUT method, it will update an existing one based on the store_id you provided.
```
Header:
    Content-Type: application/json
    Authorization Required

Body:
{
    "name': <string:name>           #required
}
```
#### Successful request
Yay we found your store in our database! We return a 200 OK response with the updated store:
```
{
    "store_id": <int:store_id>,
    "name": <string:name>,
    "items": [
        item1_info,...
    ]
}
```
#### Unsuccessful request
In case you forgot to put a store name, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": "This store needs a name."
}
```
Did you forget to authorize yourself? You bet. Since our stores are important, we cannot allow anyone to go and just update some random stores! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
We did not find the store you want to update. Maybe a 404 Not Found response might remind you:
```
{
    "message": "Store not found."
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to put this store."
}
```

## GET /stores/<int:store_id>/item_list
What is a store without our favorite items? With this endpoint we can easily access to all items we currently have in our store! Just a quick reminder, don't forget to put some items in the store first!
```
No request body needed.
```
#### Successful request
Whatever the request is, there is always a 200 OK response with our items (none or many):
```
[
    {
        "item_id": <int:item_id>,
        "name": <string:name>,
        "price": <float:price>,
        "store_id": <int:store_id>
    },
    ...
]
```

## GET /stores/<int:store_id>/items/<int:item_id>
With this endpoint we can easily access to a particular item we currently have in our store! Just a quick reminder, don't forget to put the item_id!
```
No request body needed.
```
#### Successful request
In case you find your item, congratulations! There is always a 200 OK response with your item as well:
```
{
    "item_id": <int:item_id>,
    "name": <string:name>,
    "price": <float:price>,
    "store_id": <int:store_id>
}
```
#### Unsuccessful request
Too bad we cannot find your store! We return a 404 Not Found response to notify you that:
```
{
    "message": "Store not found."
}
```
Too bad we cannot find your item! We return a 404 Not Found response to notify you that:
```
{
    "message": "Item not found."
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to get this item."
}
```

## POST /stores/<int:store_id>/items
With this endpoint we can easily upload our favorite item we currently have to our store! Just a quick reminder, don't forget to put the store_id!
```
Header:
    Content-Type: application/json
    Authorization Required

Body:
{
    "name": <string:name>,              #required
    "price": <float:price>              #required
}
```
#### Successful request
In case we can upload your item, congratulations! We return a 201 Created response with your item as well:
```
{
    "item_id": <int:item_id>,
    "name": <string:name>,
    "price": <float:price>,
    "store_id": <int:store_id>
}
```
#### Unsuccessful request
Too bad we cannot find the store you want to upload to! A 404 Not Found response will be return with this message:
```
{
    "message": "Store not found."
}
```
In case you forgot to put an item name, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": "This item needs a name."
}
```
The same thing happens when you forget to put a price, a 400 Bad Request response will be returned with this message:
```
{
    "message": "This item needs a price."
}
```
Did you forget to authorize yourself? You bet. Since our items are precious, we cannot allow anyone to go and just upload some random items! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to post this item."
}
```

## DELETE /stores/<int:store_id>/items/<int:item_id>
With this endpoint we can easily remove our unwanted item we currently have in our store! Just a quick reminder, don't forget to put the item_id!
```
Header:
    Authorization Required
```
#### Successful request
In case we can remove the item you hated, congratulations! We return a 200 OK response with this message:
```
{
    "message": "Item deleted."
}
```
#### Unsuccessful request
Too bad we cannot find the store you want to delete the item from! A 404 Not Found response will be return with this message:
```
{
    "message": "Store not found."
}
```
Too bad we cannot find the item you want to delete! A 404 Not Found response will be return with this message:
```
{
    "message": "Item not found."
}
```
Did you forget to authorize yourself? You bet. Since our items are precious, we cannot allow anyone to go and just delete some random items! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to delete this item."
}
```

## PUT /stores/<int:store_id>/items/<int:item_id>
Did you put wrong information about your favorite item into the database? Well, you can simply use this PUT method, it will update an existing one based on the store_id you provided.
```
Header:
    Content-Type: application/json
    Authorization Required

Body:
{
    "name": <string:name>,          #required   
    "price": <float:price>          #required
}
```
#### Successful request
Yay we found your item in our database! We return a 200 OK response with the updated item:
```
{
    "item_id": <int:item_id>,
    "name": <string:name>,
    "price": <float:price>,
    "store_id": <int:store_id>
}
```
#### Unsuccessful request
In case you forgot to put an item name, a 400 Bad Request response will be sent back alongside with this message:
```
{
    "message": "This item needs a name."
}
```
The same thing happens when you forget to put a price, a 400 Bad Request response will be returned with this message:
```
{
    "message": "This item needs a price."
}
```
Too bad we cannot find the store you want to update the item! A 404 Not Found response will be return with this message:
```
{
    "message": "Store not found."
}
```
Too bad we cannot find the item you want to update! A 404 Not Found response will be return with this message:
```
{
    "message": "Item not found."
}
```
Did you forget to authorize yourself? You bet. Since our items are precious, we cannot allow anyone to go and just update some random items! A 401 Unauthorized reminder for you!
```
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
Did you log in a long time ago? You should log in again since our protected system invalidates unused access token after some time! A 401 Unauthorized reminder for you!
```
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
When there is some unexpected error within our internal server, a 500 Internal Server Error response will be returned, and you should upload the bug for us to fix!
```
{
    "message": "An error occurred when trying to put this item."
}
```
