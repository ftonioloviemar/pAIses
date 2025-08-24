#!/bin/bash

UV_BIN="$1" # uv binary path passed as argument

# This script sets up a systemd service for the pAIses Flask application on CentOS 7.
# It assumes Python and uv are already installed.
#
# IMPORTANT: Run this script with sudo or as root.
#
# For production environments, consider using a WSGI server (like Gunicorn/uWSGI)
# and a reverse proxy (like Nginx/Apache) for better performance and security.

PROJECT_DIR="/opt/paises"
APP_USER="paisesuser"
APP_GROUP="paisesgroup"
SERVICE_NAME="paises"

# --- 1. Create user and group ---

# Create group if it doesn't exist
if ! getent group "$APP_GROUP" > /dev/null; then
    echo "Creating group: $APP_GROUP"
    groupadd "$APP_GROUP"
else
    echo "Group $APP_GROUP already exists."
fi

# Create user if it doesn't exist
if ! id -u "$APP_USER" > /dev/null 2>&1; then
    echo "Creating user: $APP_USER"
    useradd -r -g "$APP_GROUP" -s /sbin/nologin -d "$PROJECT_DIR" "$APP_USER"
else
    echo "User $APP_USER already exists."
fi

# --- 2. Ensure project directory and permissions ---

echo "Ensuring project directory $PROJECT_DIR exists and has correct permissions..."
# Create project directory if it doesn't exist
mkdir -p "$PROJECT_DIR"

# Set ownership and permissions
chown -R "$APP_USER":"$APP_GROUP" "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"

# --- 3. Create systemd service file ---

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "Creating systemd service file: $SERVICE_FILE"

cat <<EOF | tee "$SERVICE_FILE"
[Unit]
Description=pAIses Flask Application
After=network.target

[Service]
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/.venv/bin/uv run app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

# --- 4. Reload systemd, enable and start service ---

echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling and starting $SERVICE_NAME service..."
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo "
Setup complete!"
echo "To check the service status: sudo systemctl status $SERVICE_NAME"
echo "To stop the service: sudo systemctl stop $SERVICE_NAME"
echo "To start the service: sudo systemctl start $SERVICE_NAME"
echo "To restart the service: sudo systemctl restart $SERVICE_NAME"
echo "
Remember to adjust firewall rules if necessary (e.g., to open port 5000)."
echo "For production, consider using Gunicorn/uWSGI with Nginx/Apache."
