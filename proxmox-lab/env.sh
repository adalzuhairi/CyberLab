#!/bin/bash

# API Proxmox
export PM_API_URL="https://192.168.186.130:8006/api2/json"

# Token Proxmox
export PM_API_TOKEN_ID="terraform@pve!opentofu"

# Remplace uniquement la ligne ci-dessous par TON vrai secret
export PM_API_TOKEN_SECRET="6ed52d9e-4913-45c3-85b4-7498df445b54"

# Variables utilisées par OpenTofu
export TF_VAR_proxmox_endpoint="$PM_API_URL"
export TF_VAR_proxmox_api_token_id="$PM_API_TOKEN_ID"
export TF_VAR_proxmox_api_token_secret="$PM_API_TOKEN_SECRET"

echo "Variables OpenTofu chargées."
