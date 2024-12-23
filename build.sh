#!/bin/bash

# Install wkhtmltopdf
apt-get update
apt-get install -y wkhtmltopdf

# Install Python dependencies
pip install -r requirements.txt
