# poshcomputer

A natural language agent that uses PowerShell and the NVIDIA Nemotron Nano v2 LLM to solve administrative tasks through natural language commands.

## Overview

This agent interprets natural language requests and executes PowerShell commands to perform administrative tasks. It uses a restricted list of safe, read-only PowerShell cmdlets to ensure security while providing powerful system information gathering capabilities.

## Features

- 🤖 **Natural Language Understanding**: Uses NVIDIA Nemotron Nano v2 LLM to interpret requests
- 🛡️ **Security First**: Restricted command list prevents destructive operations
- ⚡ **PowerShell Native**: Uses `pwsh` for cross-platform compatibility
- 🎯 **Administrative Tasks**: Focused on system information and diagnostics

## Prerequisites

1. **PowerShell 7+** (pwsh)
   - Linux: `sudo apt-get install -y powershell` or download from [PowerShell GitHub](https://github.com/PowerShell/PowerShell)
   - macOS: `brew install --cask powershell`
   - Windows: `winget install Microsoft.PowerShell`

2. **Python 3.8+**

3. **NVIDIA API Key** for Nemotron Nano v2 LLM
   - Get your API key from [NVIDIA NGC](https://catalog.ngc.nvidia.com/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pemo11/poshcomputer.git
cd poshcomputer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
```bash
cp .env.example .env
# Edit .env and add your NVIDIA_API_KEY
```

## Configuration

The `config.json` file contains:
- **restricted_commands**: List of allowed PowerShell cmdlets (read-only operations)
- **nemotron_model**: The LLM model to use
- **max_tokens**: Maximum response length
- **temperature**: LLM creativity setting (0.0-1.0)

### Allowed PowerShell Commands

The agent restricts execution to safe, read-only cmdlets:
- System Information: `Get-ComputerInfo`, `Get-Process`, `Get-Service`
- File System: `Get-Item`, `Get-ChildItem`, `Get-Content`, `Test-Path`
- Network: `Get-NetAdapter`, `Get-NetIPAddress`, `Test-Connection`
- Storage: `Get-Disk`, `Get-Volume`
- Utilities: `Get-Date`, `Get-Location`, `Select-Object`, `Where-Object`, `Sort-Object`

## Usage

### Interactive Mode

Run the agent without arguments for interactive mode:
```bash
python agent.py
```

Example session:
```
You: Show me all running processes
🤖 Interpreting request with Nemotron Nano v2...
💡 Interpreted command: Get-Process
⚡ Executing PowerShell command...
✅ Success!
Output:
[Process list displayed]

You: What's the current date and time?
🤖 Interpreting request with Nemotron Nano v2...
💡 Interpreted command: Get-Date
⚡ Executing PowerShell command...
✅ Success!
Output:
[Date/time displayed]

You: exit
👋 Goodbye!
```

### Single Command Mode

Execute a single request:
```bash
python agent.py "show me all services"
python agent.py "list files in the current directory"
python agent.py "check if localhost is reachable"
```

## Example Requests

The agent can handle various natural language requests:

- **Process Management**: "Show me all running processes", "List processes using the most CPU"
- **Services**: "Show me all services", "Check the status of services"
- **File System**: "List files in the current directory", "Show the contents of config.json"
- **Network**: "Test connection to google.com", "Show network adapters"
- **System Info**: "Get computer information", "Show disk volumes"
- **Date/Time**: "What's the current date?", "Show me the time"

## Security

The agent implements multiple security layers:

1. **Restricted Command List**: Only pre-approved cmdlets can be executed
2. **Command Validation**: Checks for dangerous patterns and operators
3. **No Destructive Operations**: All `Set-`, `Remove-`, `Delete-`, `Stop-` commands are blocked
4. **No Command Chaining**: Pipes, semicolons, and redirection are prohibited
5. **Timeout Protection**: Commands are limited to 30 seconds execution time

## Development

### Project Structure

```
poshcomputer/
├── agent.py           # Main agent implementation
├── config.json        # Configuration and allowed commands
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

### Adding New Commands

To add a new allowed command, edit `config.json` and add the cmdlet to the `restricted_commands` list. Only add safe, read-only commands.

## Troubleshooting

### PowerShell Not Found
```
RuntimeError: PowerShell (pwsh) is not installed
```
Install PowerShell 7+ following the prerequisites section.

### API Key Issues
```
ValueError: NVIDIA_API_KEY not found in environment variables
```
Ensure you've created a `.env` file with your `NVIDIA_API_KEY`.

### Command Not Allowed
```
Error: Command 'Get-EventLog' is not in the restricted command list
```
The requested command is not in the allowed list. Check `config.json` for available commands.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please ensure any new commands added to the restricted list are safe and read-only.

## Acknowledgments

- Built with [NVIDIA Nemotron Nano v2 LLM](https://catalog.ngc.nvidia.com/)
- Powered by [PowerShell](https://github.com/PowerShell/PowerShell) 
