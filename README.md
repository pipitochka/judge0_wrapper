# Judge0 Wrapper

A FastAPI application that wraps Judge0 code execution engine with additional task checking functionality.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules https://github.com/JeeEssEm/judge0_wrapper.git
cd judge0_wrapper
```

If you already cloned without submodules:
```bash
git submodule update --init --recursive
```

2. Create environment file:
```bash
cp .env.example .env
```

3. (Optional) Edit `.env` file to customize configuration. The default values in `.env.example` are sufficient for local development.

4. Start all services:
```bash
./run.sh
```

5. Wait for services to initialize (first run may take a few minutes to download images and initialize database).

6. Access the services:
   - Task Checker API: http://localhost:8000/api/docs
   - Health check: http://localhost:8000/health
   - Judge0 API: http://localhost:2358

## Services

The application consists of the following Docker services:

- **task-checker**: FastAPI application for task checking
- **judge0-server**: Judge0 API server
- **judge0-worker**: Judge0 worker for code execution
- **db**: PostgreSQL database
- **redis**: Redis cache

## Configuration

Configuration is managed through environment variables in the `.env` file:

### Judge0 Configuration
- `REDIS_PASSWORD`: Redis authentication password
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: PostgreSQL credentials
- `AUTHN_TOKEN`: Optional authentication token for Judge0 API

### Task Checker Configuration
- `UVICORN_HOST`, `UVICORN_PORT`: Server host and port
- `AUTH_JWT_SECRET`: Secret key for JWT token generation
- `JUDGE0_AUTHN_TOKEN`: Token for authenticating with Judge0
- `JUDGE0_HOST`: Judge0 service hostname (default: judge0-server)

## Development

To view logs:
```bash
docker-compose logs -f task-checker
docker-compose logs -f judge0-server
```

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (clean slate):
```bash
docker-compose down -v
```

To rebuild after code changes:
```bash
docker-compose up -d --build task-checker
```

## API Documentation

Once running, visit http://localhost:8000/api/docs for interactive API documentation (Swagger UI).
