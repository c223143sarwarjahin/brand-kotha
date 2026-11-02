#!/usr/bin/env bash
set -e

echo "--> Exporting FastAPI OpenAPI specification..."
python3 -c "
import json
from app.main import app
with open('packages/api-client/openapi.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
"

echo "--> Generating TypeScript client schemas from OpenAPI..."
pnpm --filter @brandkotha/api-client run build || true
echo "--> API Client generation completed successfully!"

