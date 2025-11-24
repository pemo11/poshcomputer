"""
Demo script showing how the PowerShell Computer Use Agent works.

This script demonstrates the agent's capabilities without requiring an LLM API key.
It simulates the agent's behavior by showing command execution results.
"""

import os
from config import Config
from powershell import PowerShell


def print_header(text):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_command(cmd, result):
    """Print a command and its result."""
    print(f"💻 Command: {cmd}")
    
    if 'cwd' in result:
        print(f"📁 Working Directory: {result['cwd']}")
    
    if result.get('stdout'):
        print(f"📤 Output:\n{result['stdout']}")
    
    if result.get('stderr'):
        print(f"⚠️  Errors:\n{result['stderr']}")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    
    print("-" * 70)


def demo_basic_commands():
    """Demonstrate basic PowerShell commands."""
    print_header("Demo 1: Basic PowerShell Commands")
    
    config = Config()
    pwsh = PowerShell(config)
    
    # Get current location
    result = pwsh.exec_powershell_command("Get-Location")
    print_command("Get-Location", result)
    
    # List files in current directory
    result = pwsh.exec_powershell_command("Get-ChildItem")
    print_command("Get-ChildItem", result)
    
    # Echo a message
    result = pwsh.exec_powershell_command("Write-Output 'Hello from PowerShell Agent!'")
    print_command("Write-Output 'Hello from PowerShell Agent!'", result)


def demo_directory_navigation():
    """Demonstrate directory navigation."""
    print_header("Demo 2: Directory Navigation")
    
    config = Config()
    pwsh = PowerShell(config)
    
    # Show current directory
    result = pwsh.exec_powershell_command("pwd")
    print_command("pwd", result)
    
    # Navigate to /tmp
    result = pwsh.exec_powershell_command("Set-Location /tmp")
    print_command("Set-Location /tmp", result)
    
    # Show new directory
    result = pwsh.exec_powershell_command("pwd")
    print_command("pwd", result)


def demo_security_features():
    """Demonstrate security features."""
    print_header("Demo 3: Security Features")
    
    config = Config()
    pwsh = PowerShell(config)
    
    # Try an allowed command
    result = pwsh.exec_powershell_command("Get-ChildItem")
    print("✅ Allowed command (Get-ChildItem):")
    print_command("Get-ChildItem", result)
    
    # Try a disallowed command
    result = pwsh.exec_powershell_command("Remove-Item dangerous.txt")
    print("🛡️  Blocked command (Remove-Item):")
    print_command("Remove-Item dangerous.txt", result)
    
    # Try command injection
    result = pwsh.exec_powershell_command("echo `malicious`")
    print("🛡️  Blocked injection (backtick):")
    print_command("echo `malicious`", result)


def demo_file_operations():
    """Demonstrate file operations."""
    print_header("Demo 4: File Operations")
    
    config = Config()
    pwsh = PowerShell(config)
    
    # Navigate to current directory
    result = pwsh.exec_powershell_command(f"Set-Location '{os.path.dirname(__file__)}'")
    print_command(f"Set-Location '{os.path.dirname(__file__)}'", result)
    
    # List Python files
    result = pwsh.exec_powershell_command("Get-ChildItem -Filter '*.py'")
    print_command("Get-ChildItem -Filter '*.py'", result)
    
    # Show content of config.py (first few lines)
    result = pwsh.exec_powershell_command("Get-Content config.py | Select-Object -First 10")
    print_command("Get-Content config.py | Select-Object -First 10", result)


def demo_aliases():
    """Demonstrate PowerShell aliases."""
    print_header("Demo 5: PowerShell Aliases")
    
    config = Config()
    pwsh = PowerShell(config)
    
    print("PowerShell supports both cmdlets and short aliases:\n")
    
    # Using aliases
    aliases = [
        ("ls", "List files (alias for Get-ChildItem)"),
        ("pwd", "Print working directory (alias for Get-Location)"),
        ("cat README.md", "Read file (alias for Get-Content)"),
        ("echo 'test'", "Print text (alias for Write-Output)"),
    ]
    
    for alias, description in aliases:
        print(f"📝 {description}")
        result = pwsh.exec_powershell_command(alias)
        if 'error' not in result:
            print(f"   ✅ '{alias}' executed successfully")
        else:
            print(f"   ℹ️  '{alias}': {result.get('error', 'N/A')}")
        print()


def main():
    """Run all demos."""
    print("\n" + "🔷" * 35)
    print("   PowerShell Computer Use Agent - Demo")
    print("🔷" * 35)
    
    print("\nThis demo shows the PowerShell agent's capabilities without requiring an LLM API key.")
    print("The agent can execute safe PowerShell commands with built-in security features.")
    
    try:
        demo_basic_commands()
        demo_directory_navigation()
        demo_security_features()
        demo_file_operations()
        demo_aliases()
        
        print_header("Demo Complete!")
        print("✅ All demonstrations completed successfully!")
        print("\nTo use the full agent with LLM capabilities:")
        print("  1. Configure your LLM API key in config.py")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Run: python main_from_scratch.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
