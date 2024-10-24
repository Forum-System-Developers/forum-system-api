<img src="logo.png" alt= "logo" width="100px"
style = "margin-top: 20px;"/>

# Forum System API

WEB application for Telerik Academy

## Table of Contents

- <a href="#introduction">Introduction</a>
- <a href="#features">Features</a>  <!-- Corrected hyperlink -->
- <a href="#installation">Installation</a>
- <a href="#usage">Usage</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#testing">Testing</a>

## Introduction 

The `forum-system-api` is a web application designed for Telerik Academy. It provides a platform for users to create, manage, and participate in forum discussions.

## Features

- User authentication and authorization
- Create, read, update, and delete topics and replies
- Category management with private and public categories
- User permissions and roles
- RESTful API endpoints

## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/forum-system-api.git
    cd forum-system-api
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up the environment variables:
    ```sh
    cp .env.example .env
    # Update .env with your configuration
    ```

4. Run the application:
    ```sh
    python forum_system_api/main.py
    ```

## Usage

Once the application is running, you can access the API endpoints at `http://localhost:8000/docs`, or use tools like Postman or cURL to interact with the API.

## Project Structure
```
forum-system-api/
├── api/  
│   └── api_v1/ 
│       └── routes/ 
├── config.py 
├── main.py 
├── persistence/ 
│   ├── database.py 
│   └── models/ 
├── schemas/  
├── services/ 
├── pyproject.toml 
├── README.md 
└── tests/
```
## Testing

To run the tests, use the following command:

```sh
poetry run pytest
