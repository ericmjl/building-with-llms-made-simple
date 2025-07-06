# Building with LLMs Made Simple

A tutorial on how to build Python programs with LLMs enhanced in the mix.

Made with ❤️ by Eric J. Ma (@ericmjl).

## Installation Instructions

This tutorial requires several components to be installed:

### 0. Install Pixi

Pixi is a package management tool that we'll use to manage dependencies. Install it using one of these methods:

**Linux & macOS** (using curl):

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows** (using PowerShell):

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

After installation, you may need to restart your terminal for the changes to take effect.

### 1. Install Ollama

Ollama is required to run the local LLM models used in this tutorial.

- **Linux**: Visit [https://ollama.com/download/linux](https://ollama.com/download/linux)
- **macOS**: Visit [https://ollama.com/download/mac](https://ollama.com/download/mac)
- **Windows**: Visit [https://ollama.com/download/windows](https://ollama.com/download/windows)

Follow the installation instructions for your platform.

### 2. Run the Installation Script

After installing Ollama, run the following command to:

- Pull the required LLM models
- Install uv (Python package manager)
- Set up a virtual environment
- Install all required dependencies

```bash
pixi run start
```

The command will:

1. Pull the following Ollama models:
   - `llama3.2`
   - `phi4`
   - `gemma2:2b`
2. Install uv if not already installed
3. Create a Python virtual environment
4. Install all required dependencies

> Please do this before arrival to the tutorial session,
> as they may take some time to download!

### 3. Running the Notebooks

After installation is complete, you can run the notebooks using:

```bash
# Run the first notebook
uvx marimo edit --sandbox notebooks/01_simple_bot.py

# Or run the second notebook
uvx marimo edit --sandbox notebooks/02_structured_bot.py
```

## Manual Installation (Alternative)

If you prefer to install components manually:

1. Install Ollama from [https://ollama.com/download](https://ollama.com/download)

2. Pull the required models:

   ```bash
   ollama pull llama3.2
   ollama pull phi4
   ollama pull gemma2:2b
   ```

3. Install uv:

   ```bash
   curl -fsSL https://astral.sh/uv/install.sh | bash
   ```

4. Run a notebook:

   ```bash
   cd notebooks/
   uvx marimo edit --sandbox 01_simple_bot.py
   ```

## Troubleshooting

- **Ollama Model Download Issues**: If you encounter issues downloading models, ensure you have a stable internet connection and sufficient disk space.
- **uv Installation Problems**: If uv installation fails, you can try installing it using pip: `pip install uv`
- **Notebook Errors**: Ensure all dependencies are correctly installed and that Ollama is running in the background.
