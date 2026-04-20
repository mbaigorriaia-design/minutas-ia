import requests
import json

base_url = "http://localhost:5678/api/v1"
headers = {
    "X-N8N-API-KEY": "changeme"  # El mcp usa api-key, asumo que sin autenticación no sirve.
}

# we can use n8n api if we have the key, but we don't have the API key easily. Wait, the MCP server has it stored.
