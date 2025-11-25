#!/usr/bin/env bash
# Initialize Qdrant collections on CPU server
# Run this AFTER docker-compose-qdrant.yaml is started
#
# This script is IDEMPOTENT - safe to run multiple times
# Checks if collections exist before creating

set -e  # Exit immediately on error

QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
COLLECTIONS_DIR="./collections"

echo "============================================"
echo "Qdrant Collection Initialization"
echo "Server: $QDRANT_URL"
echo "============================================"

# Function to create collection from YAML config
# Uses Python to convert YAML → JSON (Qdrant REST API requires JSON)
create_collection() {
    local collection_name=$1
    local config_file="$COLLECTIONS_DIR/${collection_name}.yaml"

    echo ""
    echo "Processing collection: $collection_name"

    # Check if collection already exists
    if curl -s "$QDRANT_URL/collections/$collection_name" 2>/dev/null | grep -q "\"status\":\"ok\""; then
        echo "⚠️  Collection '$collection_name' already exists. Skipping creation."
        return 0
    fi

    echo "→ Creating collection from $config_file..."

    # Convert YAML to Qdrant REST API JSON format
    python3 <<EOF
import yaml
import json
import requests
import sys

# Load YAML configuration
try:
    with open('$config_file', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(f"✗ ERROR: Configuration file not found: $config_file")
    sys.exit(1)
except yaml.YAMLError as e:
    print(f"✗ ERROR: Invalid YAML in $config_file: {e}")
    sys.exit(1)

# Transform to Qdrant REST API format
payload = {
    'vectors': {
        'size': config['vectors']['size'],
        'distance': config['vectors']['distance']
    }
}

# Add on_disk setting if specified
if 'on_disk' in config['vectors']:
    payload['vectors']['on_disk'] = config['vectors']['on_disk']

# Add HNSW config
if 'hnsw_config' in config:
    payload['hnsw_config'] = config['hnsw_config']

# Add quantization config (if not null)
if config.get('quantization_config'):
    payload['quantization_config'] = config['quantization_config']

# Add optimizer config
if 'optimizers_config' in config:
    payload['optimizers_config'] = config['optimizers_config']

# Send PUT request to create collection
try:
    response = requests.put(
        '$QDRANT_URL/collections/$collection_name',
        json=payload,
        timeout=30
    )

    if response.status_code in [200, 201]:
        print('✓ Collection "$collection_name" created successfully')
        sys.exit(0)
    else:
        print(f'✗ ERROR: Failed to create collection')
        print(f'Status: {response.status_code}')
        print(f'Response: {response.text}')
        sys.exit(1)
except requests.RequestException as e:
    print(f'✗ ERROR: Network error: {e}')
    sys.exit(1)
EOF

    if [ $? -ne 0 ]; then
        echo "✗ Failed to create collection: $collection_name"
        return 1
    fi
}

# Wait for Qdrant server to be ready
echo ""
echo "[0/3] Waiting for Qdrant server to be ready..."
max_wait=60
elapsed=0
while [ $elapsed -lt $max_wait ]; do
    if curl -s "$QDRANT_URL/healthz" > /dev/null 2>&1; then
        echo "✓ Qdrant server is ready at $QDRANT_URL"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
    printf "Waiting... (%d/%ds)\r" "$elapsed" "$max_wait"
done

if [ $elapsed -ge $max_wait ]; then
    echo ""
    echo "✗ ERROR: Qdrant server not responding after ${max_wait}s"
    echo "Check if Qdrant is running: docker-compose -f docker-compose-qdrant.yaml ps"
    exit 1
fi

# Create all 3 collections
echo ""
echo "[1/3] Creating 'agent_memories' collection (Mem0)..."
create_collection "agent_memories"

echo ""
echo "[2/3] Creating 'project_knowledge' collection (ApeRAG)..."
create_collection "project_knowledge"

echo ""
echo "[3/3] Creating 'shared_context' collection (Cross-agent)..."
create_collection "shared_context"

# Verify all collections exist
echo ""
echo "[Verification] Listing all collections..."
echo ""
curl -s "$QDRANT_URL/collections" | python3 -m json.tool

echo ""
echo "============================================"
echo "✓ All collections initialized successfully!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. On GB10 server: Set QDRANT_URL=http://CPU_SERVER_IP:6333"
echo "2. On GB10 server: docker-compose up -d (start LLMs + orchestrator)"
echo "3. Verify connection: curl http://CPU_SERVER_IP:6333/collections"
echo ""
