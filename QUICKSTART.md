# Quick Start Guide

This guide will help you get started with the PowerShell Computer Use Agent quickly.

## Prerequisites

1. **PowerShell Core (pwsh)** - Install from https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell
2. **Python 3.8+** - Make sure Python is installed on your system
3. **LLM API Access** - Get an API key from NVIDIA's build.nvidia.com or use a local model

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/pemo11/poshcomputer.git
cd poshcomputer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your LLM

Edit `config.py` and update the following fields:

```python
llm_base_url: str = "https://integrate.api.nvidia.com/v1"
llm_model_name: str = "nvidia/nvidia-nemotron-nano-9b-v2"
llm_api_key: str = "YOUR-API-KEY-HERE"  # Replace with your actual API key
```

To get an API key for NVIDIA Nemotron:
1. Visit https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2
2. Click "View Code" or "Get API Key"
3. Sign up/login and generate your API key

### 4. Test Your Setup (Without LLM)

Run the demo to verify PowerShell commands work:

```bash
python demo.py
```

Run the test suite:

```bash
python test_powershell.py
```

### 5. Run the Agent

**Option 1: From-scratch implementation (simpler, recommended for learning)**

```bash
python main_from_scratch.py
```

**Option 2: LangGraph implementation (requires langchain packages)**

```bash
python main_langgraph.py
```

## First Commands

Try these commands when the agent starts:

1. **List files**: "Show me all files in the current directory"
2. **Check location**: "Where am I right now?"
3. **Navigate**: "Go to the /tmp directory"
4. **File content**: "Show me the content of README.md"
5. **Search**: "Find all Python files in this directory"

## Security Features

The agent is configured with safety features:

- ✅ Only whitelisted commands can be executed
- ✅ User confirmation required before each command runs
- ✅ Command injection patterns are blocked
- ✅ Dangerous commands like Remove-Item are not allowed
- ✅ 30-second timeout on all commands

## Customization

### Allow More Commands

Edit `config.py` and add commands to the `allowed_commands` list:

```python
allowed_commands: list = field(default_factory=lambda: [
    "Get-ChildItem", "Set-Location", "Get-Content",
    # Add your commands here
    "Get-Date", "Get-Process",
])
```

⚠️ **Warning**: Only add commands you trust. Each additional command increases security risk.

### Change Working Directory

By default, the agent operates in the directory where it's installed. To change this:

```python
root_dir: str = "/path/to/your/working/directory"
```

## Troubleshooting

### PowerShell not found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'pwsh'`

**Solution**: Install PowerShell Core from https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell

### LLM Connection Failed

**Error**: Connection errors or API key issues

**Solutions**:
1. Verify your API key is correct
2. Check that `llm_base_url` is accessible
3. Test your internet connection
4. For local models, ensure the server is running

### Command Not in Allowlist

**Error**: `Parts of this command were not in the allowlist`

**Solution**: Add the command to `allowed_commands` in `config.py` (only if you trust it)

### Command Injection Error

**Error**: `Command injection patterns are not allowed`

**Solution**: This is a security feature. Avoid using backticks (`) or `$()` in commands

## Examples

### Example Session

```
['/home/user/poshcomputer' 🙂] List all Python files

[🤖] Thinking...
    ▶️   Execute 'Get-ChildItem -Filter "*.py"'? [y/N]: y
config.py
helpers.py
main_from_scratch.py
main_langgraph.py
powershell.py
test_powershell.py
demo.py
--------------------------------------------------------------------------------

['/home/user/poshcomputer' 🙂] How many lines are in config.py?

[🤖] Thinking...
    ▶️   Execute 'Get-Content config.py | Measure-Object -Line'? [y/N]: y
Lines: 68
--------------------------------------------------------------------------------
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Review the [demo.py](demo.py) to see example usage
3. Examine [test_powershell.py](test_powershell.py) for API examples
4. Customize `config.py` for your specific needs

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review the original NVIDIA project: https://github.com/NVIDIA/GenerativeAIExamples
- Open an issue on GitHub for bugs or feature requests

## Safety Reminder

⚠️ This agent can execute PowerShell commands on your system. Always:
- Review commands before approving them
- Only add trusted commands to the allowlist
- Run in a safe environment when testing
- Never expose this agent to untrusted users
- Keep your API keys secret

Enjoy using your PowerShell Computer Use Agent! 🚀
