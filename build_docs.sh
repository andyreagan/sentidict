#!/bin/bash
# Simple script to build and optionally serve documentation

set -e  # Exit on error

# Function to display usage information
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --clean     Clean documentation build directory before building"
    echo "  --serve     Start a local server to view documentation (port 8000)"
    echo "  --help      Show this help message"
}

# Default values
CLEAN=false
SERVE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --clean)
            CLEAN=true
            shift
            ;;
        --serve)
            SERVE=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Install dependencies if needed
if ! python -c "import sphinx" &>/dev/null; then
    echo "Installing documentation dependencies..."
    pip install -e ".[docs]"
fi

# Clean build directory if requested
if [ "$CLEAN" = true ]; then
    echo "Cleaning documentation build directory..."
    cd docs && make clean && cd ..
fi

# Build documentation
echo "Building documentation..."
cd docs && make html && cd ..

echo "Documentation built successfully!"
echo "Open docs/_build/html/index.html in your browser to view it."

# Serve documentation if requested
if [ "$SERVE" = true ]; then
    echo "Starting local server at http://localhost:8000"
    python -m http.server -d docs/_build/html 8000
fi
