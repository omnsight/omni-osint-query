# Omni OSINT Query
[![codecov](https://codecov.io/github/omnsight/omni-osint-query/graph/badge.svg?token=HYQJI9LHMK)](https://codecov.io/github/omnsight/omni-osint-query)

A FastAPI-based service providing OSINT (Open Source Intelligence) query capabilities, including features for finding neighbors and events related to a query.

### 🚀 Features

- Health checks to monitor service status.
- Query endpoint for searching OSINT data.
- Neighbors endpoint to find related entities.

### 🛠 Tech Stack

- Python
- FastAPI
- ArangoDB
- Redis
- Docker
- uv

## 📦 Getting Started

### Prerequisites

- Python 3.11+
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

## ⚙️ Configuration

Fill the `.env` file:

```bash
stage="local"

# ArangoDB
ARANGODB_HOST="http://localhost:8529"
ARANGODB_USERNAME="root"
ARANGODB_PASSWORD="password"
ARANGODB_DB_NAME="test_osint_db"
ARANGODB_EMBEDDING_DIMENSION="384"

# Redis
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_PASSWORD=""

# Embedding Model
EMBEDDING_AI_API_KEY=
EMBEDDING_AI_API_BASE_URL=
EMBEDDING_MODEL=
```

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
import { OpenAPI, QueryService, QueryRequest } from 'omni-osint-query/client'; // Adjust path if needed

// Configure the API client
OpenAPI.BASE = 'http://localhost:8000'; // Adjust if your server runs on a different host/port
// Configure authentication (e.g., with a bearer token)
OpenAPI.TOKEN = 'your-bearer-token';

async function main() {
  try {
    const requestBody: QueryRequest = {
      query: 'your-query-here',
      sources: ['source1', 'source2'],
    };

    const response = await QueryService.query(requestBody);
    console.log('Query Response:', response);
  } catch (error) {
    console.error('Error during query:', error);
  }
}

main();
```

## Local Development

Refer to [DEVELOPMENT.md](DEVELOPMENT.md) for local development setup.

## 📄 License

Distributed under the Apache-2.0 License. See [LICENSE](./LICENSE) for more information.
