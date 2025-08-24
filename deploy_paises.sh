#!/bin/bash

# This script automates the deployment of the pAIses Flask application on CentOS 7.
# It handles cloning/pulling the repository, setting up the virtual environment,
# installing dependencies, running database migrations, and setting up the systemd service.
#
# IMPORTANT: Run this script with sudo or as root.
#
# Usage: UV_BIN=$(which uv) curl -sL <URL_TO_THIS_SCRIPT> | bash
# Or: UV_BIN=$(which uv) bash deploy_paises.sh

PROJECT_DIR="/opt/paises"
REPO_URL="https://github.com/ftonioloviemar/pAIses.git"

# --- 1. Ensure project directory and clone/pull repository ---

echo "Ensuring project directory $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR" || { echo "Failed to create project directory."; exit 1; }

if [ -d "$PROJECT_DIR/.git" ]; then
    echo "Repository already cloned. Pulling latest changes..."
    (cd "$PROJECT_DIR" && git pull) || { echo "Failed to pull latest changes."; exit 1; }
else
    echo "Cloning repository into $PROJECT_DIR..."
    git clone "$REPO_URL" "$PROJECT_DIR" || { echo "Failed to clone repository."; exit 1; }
fi

# --- 2. Navigate to project directory ---
cd "$PROJECT_DIR" || { echo "Failed to change to project directory."; exit 1; }

# --- 3. Install dependencies using uv ---

echo "Setting up virtual environment and installing dependencies..."
# uv will automatically create/manage the venv

# --- 4. Run database migrations ---

echo "Running database migrations..."
"$UV_BIN" run flask migrate-db || { echo "Failed to run migrate-db."; exit 1; }
"$UV_BIN" run flask migrate-ranking-difficulty || { echo "Failed to run migrate-ranking-difficulty."; exit 1; }

# --- 5. Set up systemd service ---

echo "Setting up systemd service..."
# Ensure the setup_service.sh script is executable
chmod +x setup_service.sh || { echo "Failed to make setup_service.sh executable."; exit 1; }
./setup_service.sh "$UV_BIN" || { echo "Failed to run setup_service.sh."; exit 1; }

# --- 6. Final service check ---

echo "Ensuring service is running..."
systemctl is-active --quiet paises || systemctl start paises || { echo "Failed to start paises service."; exit 1; }

echo "
Deployment complete!"
echo "The pAIses application should now be running and accessible."
echo "
Remember to adjust firewall rules if necessary (e.g., to open port 5000)."
echo "For production, consider using Gunicorn/uWSGI with Nginx/Apache."
echo "To check the service status: sudo systemctl status paises"
