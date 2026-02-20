# Omni Osint Query API Backend
[![codecov](https://codecov.io/github/omnsight/omni-osint-query/graph/badge.svg?token=HYQJI9LHMK)](https://codecov.io/github/omnsight/omni-osint-query)

## Overview

The Omni OSINT Query API is a backend service designed to provide a powerful and flexible interface for querying open-source intelligence (OSINT) data. It is built with a modern Python stack, leveraging FastAPI for high-performance API development and Pydantic for robust data validation.

This service integrates with a graph database to represent complex relationships between different OSINT entities, such as events, persons, organizations, and websites. It exposes a set of API endpoints that allow clients to perform sophisticated queries, such as searching for events within a specific date range, finding neighboring entities connected to a given entity, and more.

### Key Features

- **FastAPI-Based**: Built on FastAPI, the service is asynchronous, fast, and includes automatic OpenAPI documentation generation.
- **Graph-Based Data Model**: Leverages a graph database to model and query complex relationships between OSINT data points.
- **Entity-Relationship Queries**: Provides endpoints for searching entity neighborhoods, allowing clients to explore connections between data.
- **Event and Entity Search**: Supports querying for events and other entities with filters for date ranges, text search, and other attributes.
- **Authentication and Authorization**: Secures endpoints using JWT-based authentication and role-based access control.
- **Containerized**: Fully containerized with Docker, making it easy to set up and run in a local development environment or deploy to production.

## Project Structure

High-level overview of the project folder structure:

- `client/`: TypeScript client library generated from the OpenAPI definition. Contains source code and build scripts.
- `doc/`: Documentation artifacts, including `openapi.json` used for client generation.
- `src/omni_osint_query/`: Python source code for the backend application.
    - `routers/`: API route definitions.
    - `main.py`: Application entry point and configuration.
- `tools/`: Utility scripts (e.g., for exporting OpenAPI specs).
- `pyproject.toml` / `uv.lock`: Python dependency management and project configuration.
- `docker-compose.yml` / `Dockerfile`: Containerization configuration.

## Usage

### API Call Using Typescript Client

To use this client in your project, add the following to your `package.json`:

```json
{
  "dependencies": {
    "omni_osint_query": "github.com/omnsight/omni-osint-query#main"
  }
}
```

Here is a sample code snippet demonstrating how to use the client to invoke API calls.

```typescript
import { HealthService, OpenAPI } from 'omni_osint_query';

async function main() {
  // Configure the base URL and a static token
  OpenAPI.BASE = 'http://localhost:8000';
  OpenAPI.TOKEN = 'your-static-jwt-token-here';

  try {
    const health = await HealthService.healthCheckHealthGet();
    console.log('Health check result:', health);
  } catch (error) {
    console.error('Error fetching health check:', error);
  }
}
```

## Local Development

Refer to [DEVELOPMENT.md](DEVELOPMENT.md) for local development setup.
