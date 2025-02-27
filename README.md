# Web Scanner

A basic website scanning application built with FastAPI. It utilizes the HTTPX CLI to gather metadata about websites, processes the output using custom extractors and builders, and exposes a REST API to initiate scans.

## Features

- Scan a website and retrieve metadata.
- Asynchronous processing with FastAPI.
- API documentation available via Swagger and ReDoc.

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

The application uses an environment variable for the logging level. By default, it is set to `INFO`. To change the logging level, set the `LOG_LEVEL` environment variable in your `docker-compose.yml` file.

## Running the Application

To build and run the application service, execute:

```bash
cd backend
docker compose up --build app
```

## Accessing the Application

- **Home Page:** [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing the Application

To run the test suite using Docker Compose, execute:

```bash
cd backend
docker compose up --build tests
```

This command builds the Docker image for testing and runs the test suite (using `pytest`). When the tests finish, the container will exit and display the results in your terminal.

## API Endpoints

### 1. **Run HTTPX Scan**
   - **Endpoint:** `POST /api/scan`
   - **Description:** Runs an HTTPX scan on the given domain and returns metadata.
   - **Request Body:**
     ```json
     {
       "domain": "nginx.org"
     }
     ```
   - **Response:**
     ```json
     {
       "domain": "nginx.org",
       "related_ips": [
         "52.58.199.22",
         "3.125.197.172"
       ],
       "webpage_title": "nginx",
       "status_code": 200,
       "webserver": "nginx/1.27.2",
       "technologies": [
         "Nginx:1.27.2"
       ],
       "cnames": []
     }
     ```

### 2. **Health Check**
   - **Endpoint:** `GET /api/health`
   - **Description:** Checks if the API is running and healthy.
   - **Response:**
     ```json
     {
       "status": "ok"
     }
     ```

