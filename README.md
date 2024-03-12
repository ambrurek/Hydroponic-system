
# Hydroponic System API

This project provides a RESTful API for managing hydroponic systems and measurements.
This is my first project using Django and Django Rest  FW so there are many things that I can still improve.
For any problems contact with me directly (ambrurek)

## Installation
After cloning repository create .env file in it and copy content of env.template to it\
Its needed to correctly build up app\
Use Docker compose to build app and all deps with postrges DB.
App will be served on 8000 port by deafult.

```bash
docker-compose build
docker-compose up
```

## Usage
In test.rest file you can find some request to api :) if you use VS-Code you can install REST CLIENT:
[REST CLIENT Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
to use those requests directly from file

#### API DOC
When App is running you can find swagger or redoc api doc on <ip>:<port>/swagger or <ip>:<port>/redoc

Additionaly some sample examples of request can be found below

## API Endpoints

### User Authentication

#### Login
```http
POST http://127.0.0.1:8000/user/login/
Content-Type: application/json

{"username": "your_username", "password": "your_password"}
```

#### Signup
```http
POST http://127.0.0.1:8000/user/register/
Content-Type: application/json

{"username": "your_username", "password": "your_password", "email": "your_email@example.com"}
```

#### Test Token
```http
GET http://127.0.0.1:8000/user/test
Content-Type: application/json 
Authorization: token your_token_here
```

### Hydroponic Systems

#### Create Hydroponic System
```http
POST http://127.0.0.1:8000/systems/hydroponic-systems/
Content-Type: application/json 
Authorization: token your_token_here

{
    "name": "your_system_name",
    "description": "your_system_description"
}
```

#### Get Hydroponic System Details
```http
GET http://127.0.0.1:8000/systems/hydroponic-systems/{system_id}/
Content-Type: application/json 
Authorization: token your_token_here
```

#### Get List of Hydroponic Systems
```http
GET http://127.0.0.1:8000/systems/hydroponic-systems/
Content-Type: application/json 
Authorization: token your_token_here
```

### Measurements

#### Create Measurement
```http
POST http://127.0.0.1:8000/systems/measurements/
Content-Type: application/json 
Authorization: token your_token_here

{
    "system": "your_system_id",
    "temperature_raw": "25F",
    "ph": "00.22",
    "tds": "122.1232"
}
```

#### Get Hydroponic System Details with Last X Measurements
```http
GET http://127.0.0.1:8000/systems/hydroponic-systems/{system_id}
Content-Type: application/json 
Authorization: token your_token_here

{"last_measurements":"5"}
```

```
