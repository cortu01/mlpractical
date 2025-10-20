#!/bin/bash
# Configure Jupyter notebook server to use password authentication and HTTPS
# Make sure Conda environment is active as we will assume it is later
[ -z "$CONDA_PREFIX" ] && echo "Error: Conda environment must be activated." && exit 1

if [ "$#" -gt 2 ]; then
    echo "Usage: bash secure-notebook-server.sh [jupyter-path] [openssl-config-path]"
    exit 1
fi

# If specified, read Jupyter directory from passed argument
JUPYTER_DIR=${1:-"$HOME/.jupyter"}
# If specified, read OpenSSL config file path from passed argument
# This is needed due to bug in how Conda handles config path
export OPENSSL_CONF=${2:-"$CONDA_PREFIX/ssl/openssl.cnf"}
SEPARATOR="================================================================="

# Create default config file if one does not already exist
if [ ! -f "$JUPYTER_DIR/jupyter_notebook_config.py" ]; then
    echo "No existing notebook configuration file found, creating new one..."
    echo "$SEPARATOR"
    jupyter notebook --generate-config
    echo "$SEPARATOR"
    echo "Notebook configuration file created."
fi

# Get user to enter notebook server password
echo "Setting up notebook server password. Enter password when prompted..."
echo "$SEPARATOR"
# Try different password generation methods for compatibility
HASH=""
if python -c "import notebook.auth" 2>/dev/null; then
    HASH=$(python -c "from notebook.auth import passwd; print(passwd())")
elif python -c "import jupyter_server.auth" 2>/dev/null; then
    HASH=$(python -c "from jupyter_server.auth import passwd; print(passwd())")
else
    echo "Error: Could not find password hashing module. Please ensure Jupyter is properly installed."
    exit 1
fi
echo "$SEPARATOR"
echo "Password hash generated."

# Generate self-signed OpenSSL certificate and key file
echo "Creating SSL certificate..."
echo "$SEPARATOR"
openssl req \
    -x509 -nodes -days 365 \
    -subj "/C=UK/ST=Scotland/L=Edinburgh/O=University of Edinburgh/OU=School of Informatics/CN=$USER/emailAddress=$USER@sms.ed.ac.uk" \
    -newkey rsa:2048 -keyout "$JUPYTER_DIR/key.key" \
    -out "$JUPYTER_DIR/cert.pem" 2>/dev/null
echo "$SEPARATOR"
echo "SSL certificate created."

# Set proper permissions on key file
chmod 600 "$JUPYTER_DIR/key.key"

# Add password hash and certificate + key file paths to config file
echo "Configuring Jupyter notebook..."
echo "$SEPARATOR"

# Configure password (try both old and new configuration names for compatibility)
echo "   Setting password..."
if ! grep -q "\.password" "$JUPYTER_DIR/jupyter_notebook_config.py"; then
    echo "c.NotebookApp.password = u'$HASH'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
    echo "c.ServerApp.password = u'$HASH'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
fi

# Configure certificate file
echo "   Setting certificate file..."
if ! grep -q "\.certfile" "$JUPYTER_DIR/jupyter_notebook_config.py"; then
    echo "c.NotebookApp.certfile = u'$JUPYTER_DIR/cert.pem'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
    echo "c.ServerApp.certfile = u'$JUPYTER_DIR/cert.pem'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
fi

# Configure key file
echo "   Setting key file..."
if ! grep -q "\.keyfile" "$JUPYTER_DIR/jupyter_notebook_config.py"; then
    echo "c.NotebookApp.keyfile = u'$JUPYTER_DIR/key.key'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
    echo "c.ServerApp.keyfile = u'$JUPYTER_DIR/key.key'" >> "$JUPYTER_DIR/jupyter_notebook_config.py"
fi

echo "$SEPARATOR"
echo "Jupyter notebook server secured successfully!"
echo "You can now start your notebook server with: jupyter notebook --no-browser"
