# String Analysis API

A FastAPI based service for analyzing strings, containerized with Docker for easy setup and deployment.

## Prerequisites

Before running this project, make sure Docker is installed on your machine.

Install Docker Desktop (includes Docker Compose):
https://docs.docker.com/get-docker/

Verify the installation:

```bash
docker --version
docker compose version
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shahzaibaziz/string_analysis.git
cd string_analysis
```

### 2. Build and run the application

```bash
docker compose up
```

To run it in detached mode (in the background):

```bash
docker compose up -d
```

To force a rebuild of the image before starting:

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Interactive API docs (Swagger UI):

```
http://localhost:8000/docs
```

## Useful Commands

Stop the running containers:

```bash
docker compose down
```

Stop and remove volumes as well:

```bash
docker compose down -v
```

View logs:

```bash
docker compose logs -f
```

Check running containers:

```bash
docker compose ps
```

Restart the service:

```bash
docker compose restart
```

Rebuild without cache:

```bash
docker compose build --no-cache
```

Open a shell inside the running container:

```bash
docker compose exec api /bin/sh
```

## Configuration

Environment variables used by the service:

| Variable  | Default   | Description                     |
|-----------|-----------|----------------------------------|
| HOST      | 0.0.0.0   | Host address the app binds to   |
| PORT      | 8000      | Port the app listens on inside the container |
| RELOAD    | false     | Enables auto reload for development |
| LOG_LEVEL | INFO      | Logging verbosity                |

## Notes

The `./app` directory is mounted read only into the container, so code changes on your host will reflect inside the container but the container cannot write back to it. If you need live reload during development, set `RELOAD=true` and mount the volume as read write instead.