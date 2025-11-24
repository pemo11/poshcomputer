# PowerShell Computer Use Agent with Nemotron

This code contains the implementation of a simple PowerShell shell agent that can operate the computer. This agent
is implemented in two different ways:

1. **From-scratch implementation**: where we show how to build the agent in pure Python with just the `openai` package as the dependency.
2. **LangGraph implementation**: where we show how the implementation can be simplified by LangGraph. This implementation requires the `langchain-openai` and `langgraph` packages.

This project is adapted from NVIDIA's [Bash Computer Use Agent](https://github.com/NVIDIA/GenerativeAIExamples/tree/be9acc9b9286a8b4ba3ef6d56dcb7ff989d5681a/nemotron/LLM/bash_computer_use_agent) to use PowerShell (pwsh) instead of Bash.

# How to run?

> ⚠️ **DISCLAIMER**: This software can execute arbitrary PowerShell commands on your system. Use at your own risk. The authors assume no responsibility for any damage, data loss, or security breaches resulting from its use. By using this software, you acknowledge and accept these risks.

## Prerequisites

- **PowerShell Core (pwsh)**: This agent uses PowerShell Core which is cross-platform (Windows, Linux, macOS).
  - Install from: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell
  - On Windows, the agent will fall back to Windows PowerShell if pwsh is not available.
- **Python 3.8+**: Required to run the agent code.

## Step 1: LLM setup

Setup your LLM endpoint in `config.py`:

- `llm_base_url` should point at your NVIDIA Nemotron Nano 9B v2 provider's base URL (or your hosted endpoint, if self-hosting).
- `llm_model_name` should be your NVIDIA Nemotron Nano 9B v2 provider's name for the model (or your hosted endpoint model name, if self-hosting).
- `llm_api_key` should be the API key for your provider (not needed if self-hosting).
- `llm_temperature` and `llm_top_p` are the sampling settings for your model. These are set to reasonable defaults for Nemotron with reasoning on mode.

An example with [`build.nvidia.com`](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2) as the provider:

```python
class Config:

    llm_base_url: str = "https://integrate.api.nvidia.com/v1"
    llm_model_name: str = "nvidia/nvidia-nemotron-nano-9b-v2"
    llm_api_key: str = "nvapi-XYZ"
    ...
```

> NOTE - You will need to obtain an API key if you're not locally hosting this model. Instructions available on [this page](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2) for `build.nvidia.com` by clicking the `View Code` button.

## Step 2: Install the dependencies

Use your favorite package manager to install the dependencies. For example:

```bash
pip install -r requirements.txt
```

## Step 3: Execute!

Choose one to run your PowerShell Agent:

```bash
python main_from_scratch.py  # From-scratch implementation
```

or

```bash
python main_langgraph.py  # LangGraph implementation
```

## Features

### PowerShell-Specific Capabilities

The agent can execute safe PowerShell commands including:

**Cmdlets (PowerShell native commands):**
- `Get-ChildItem` - List directory contents
- `Set-Location` - Change directory
- `Get-Content` - Read file contents
- `Get-Location` - Get current directory
- `New-Item` - Create files/directories
- `Copy-Item` - Copy files/directories
- `Write-Output` - Output text
- `Select-String` - Search text patterns
- And more...

**Aliases (short forms):**
- `ls`, `dir` - List directory
- `cd` - Change directory
- `cat`, `type` - Read files
- `pwd` - Get current directory
- `mkdir` - Create directory
- `cp` - Copy items
- `echo` - Output text

### Security

The agent includes several security features:

1. **Command Allowlist**: Only pre-approved commands can be executed
2. **User Confirmation**: Every command requires user approval before execution
3. **Injection Prevention**: Blocks common PowerShell command injection patterns
4. **Timeout Protection**: Commands have a 30-second timeout to prevent hanging
5. **Safe Defaults**: Dangerous commands like `Remove-Item`, `Clear-Item` are explicitly blocked

### Customization

You can customize the allowed commands in `config.py` by modifying the `allowed_commands` list. Be very careful when adding new commands, as this affects the security of the agent.

## Examples

**Example interaction:**
```
['C:\Users\YourName\Projects' 🙂] List all files in the current directory

[🤖] Thinking...
    ▶️   Execute 'Get-ChildItem'? [y/N]: y
Name                          LastWriteTime
----                          -------------
config.py                     11/24/2025 1:00:00 PM
powershell.py                 11/24/2025 1:00:00 PM
main_from_scratch.py          11/24/2025 1:00:00 PM
...
--------------------------------------------------------------------------------

['C:\Users\YourName\Projects' 🙂] Show me the content of README.md

[🤖] Thinking...
    ▶️   Execute 'Get-Content README.md'? [y/N]: y
# PowerShell Computer Use Agent with Nemotron
...
```

## Architecture

The project consists of several key components:

- **`config.py`**: Configuration for LLM and agent settings
- **`powershell.py`**: Core PowerShell command execution engine with security features
- **`helpers.py`**: Helper classes for message handling and LLM interaction
- **`main_from_scratch.py`**: Pure Python implementation of the agent loop
- **`main_langgraph.py`**: LangGraph-based implementation for simplified agent orchestration

## Troubleshooting

**PowerShell not found:**
- Ensure PowerShell Core (pwsh) is installed and in your PATH
- On Windows, the agent will automatically fall back to Windows PowerShell (powershell.exe)

**Command execution fails:**
- Check that the command is in the allowed commands list in `config.py`
- Verify there are no command injection patterns (backticks, `$()` constructs)
- Ensure you have permissions to run the command

**LLM connection issues:**
- Verify your API key is correct in `config.py`
- Check that `llm_base_url` is accessible
- Ensure you have an active internet connection for cloud-hosted models

## License

This project is adapted from NVIDIA's GenerativeAIExamples repository. Please refer to the original repository for license information.

## Credits

- Original Bash Computer Use Agent by NVIDIA: https://github.com/NVIDIA/GenerativeAIExamples
- Powered by NVIDIA Nemotron Nano 9B v2 LLM 
