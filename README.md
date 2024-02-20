# ProjectAssessment - Task 1

Author: Chua Yip Xuan

## Prerequisites

Before you begin, ensure you have met the following requirements:  
Docker  
Docker Compose  
Python >= 3.8  
FastAPI  
Uvicorn for ASGI server  
Pydantic for data validation  
Beanie for ODM with MongoDB  
Motor for the async MongoDB driver  
OpenAI Python Client  

## Setup and Installation

Clone the repository to your local machine:

```bash 
git clone https://github.com/oxxuanxxo/ProjectAssessment.git
cd ProjectAssessment
```
1. Create a .env file in the root directory of the project.
2. Head to https://platform.openai.com/api-keys and generate an API Key.
3. Add the following line to the .env file:

```.env file
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

To start the application, run the following command in the root directory of the project:

```bash
docker-compose up -d
```

## Accessing the Application

Once the application is running, you can access the API through:

Localhost URL: http://localhost:8000/docs

This URL hosts the automatically generated interactive API documentation provided by FastAPI's Swagger UI.

## Usage

(NIL)

## Stopping the Application

To stop and remove the containers, networks, and volumes associated with the application, run:
```bash
docker-compose down
```