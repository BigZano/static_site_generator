#!/bin/bash

# Build script for production deployment
# This builds the site with the GitHub Pages base path

echo "Building site for production..."
python3 src/main.py "/static_site_generator/"
echo "Production build complete!"