# Omni Osint Query
[![codecov](https://codecov.io/github/omnsight/omni-osint-query/graph/badge.svg?token=HYQJI9LHMK)](https://codecov.io/github/omnsight/omni-osint-query)

Omni OSINT Query is a powerful and scalable backend service for Open Source Intelligence (OSINT) analysis. It provides a flexible API to query and analyze relationships within large datasets, making it easy to uncover connections between people, organizations, and events.

### 🚀 Features

- **Powerful Query API**: A flexible API to query and retrieve OSINT data.
- **Graph-Based Analysis**: Find neighbors and explore relationships between different entities (e.g., people, organizations).
- **Event-Based Queries**: Search for events and associated data.
- **Rich Data Models**: Comprehensive models for representing OSINT data, including people, organizations, locations, and events.
- **Scalable Backend**: Built with Python, ArangoDB, and Redis to handle large-scale OSINT datasets.
- **TypeScript Client**: A ready-to-use client for interacting with the API.

### 🛠 Tech Stack

- **Backend:** Python, FastAPI
- **Database:** ArangoDB, Redis
- **Frontend:** TypeScript
- **Tooling:** uv, Docker, Pydantic

## 📦 Getting Started

### Prerequisites

- Python 3.10+
- Docker
- `uv`

### Installation

Clone the repo:

```bash
git clone https://github.com/omnsight/omni-osint-query.git
cd omni-osint-query
```

Install dependencies:

```bash
uv lock --upgrade
uv sync --extra dev
```

Install client dependencies:

```bash
cd client
npm install
cd ..
```

## ⚙️ Configuration

Update configurations in [`.env`](.env)

## 📖 Usage

### Running the Service

Start the backend services:

```bash
docker-compose up -d --build --wait
```

Stop the backend services when you're done:

```bash
docker-compose down
```

### Using the Client

To use the client in your Node.js project, you can install it directly from GitHub. Add the following to your `package.json`:

```json
{
  "dependencies": {
    "omni-osint-query": "github:omnsight/omni-osint-query"
  }
}
```

After installation, you can use the client in your application as shown below:

```typescript
import { OpenAPI, HealthService, HealthCheck } from 'omni-osint-query/client'; // Adjust path if needed

// Configure the API client
OpenAPI.BASE = 'http://localhost:8000'; // Adjust if your server runs on a different host/port
// Configure authentication (e.g., with a bearer token)
OpenAPI.TOKEN = 'your-bearer-token';

async function main() {
  try {
    console.log('Performing health check...');
    const healthStatus: HealthCheck = await HealthService.healthCheck();
    console.log('Health Check Status:', healthStatus);
  } catch (error) {
    console.error('Error during health check:', error);
  }
}

main();
```

## Local Development

Refer to [DEVELOPMENT.md](DEVELOPMENT.md) for local development setup.

## 📄 License

Distributed under the Apache-2.0 License. See [LICENSE](./LICENSE) for more information.
