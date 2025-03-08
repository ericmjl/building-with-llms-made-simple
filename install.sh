#!/bin/bash
set -e

echo "=== Building with LLMs Made Simple - Installation Script ==="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama is not installed. Please install Ollama first:"
    echo "Visit: https://ollama.com/download/linux"
    exit 1
fi

echo "=== Pulling required Ollama models ==="
echo "This may take some time depending on your internet connection..."
echo ""

# Pull required models
echo "Pulling llama3.2..."
ollama pull llama3.2

echo "Pulling phi4..."
ollama pull phi4

echo "Pulling gemma2:2b..."
ollama pull gemma2:2b

echo ""
echo "=== Installing uv (Python package manager) ==="

# Check if uv is already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -fsSL https://astral.sh/uv/install.sh | bash

    # Add uv to PATH for the current session
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "uv is already installed."
fi

echo ""
echo "=== Setting up Python environment ==="

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate

# Install dependencies from the notebooks
echo "Installing dependencies..."
uv pip install llamabot==0.11.2 marimo pyprojroot==0.3.0 rich==13.9.4 pydantic==2.10.6

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "To run a notebook, use:"
echo "source .venv/bin/activate"
echo "uvx marimo edit --sandbox notebooks/01_simple_bot.py"
echo ""
echo "Or:"
echo "source .venv/bin/activate"
echo "uvx marimo edit --sandbox notebooks/02_structured_bot.py"
echo ""
