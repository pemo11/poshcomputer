#!/usr/bin/env python3
"""
PowerShell Natural Language Agent using Nemotron Nano v2 LLM

This agent interprets natural language requests and executes
restricted PowerShell commands to solve administrative tasks.
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

class PowerShellAgent:
    """Natural language agent that executes PowerShell commands."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the PowerShell agent.
        
        Args:
            config_path: Path to the configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize NVIDIA API client
        api_key = os.getenv('NVIDIA_API_KEY')
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
        
        api_endpoint = os.getenv('API_ENDPOINT', 'https://integrate.api.nvidia.com/v1')
        
        self.client = OpenAI(
            base_url=api_endpoint,
            api_key=api_key
        )
        
        # Check if PowerShell is available
        self._check_powershell()
    
    def _check_powershell(self):
        """Verify that PowerShell (pwsh) is installed."""
        try:
            result = subprocess.run(
                ['pwsh', '-Command', '$PSVersionTable.PSVersion'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"PowerShell detected: {result.stdout.strip()}")
            else:
                raise RuntimeError("PowerShell (pwsh) is not responding correctly")
        except FileNotFoundError:
            raise RuntimeError(
                "PowerShell (pwsh) is not installed. "
                "Please install PowerShell from https://github.com/PowerShell/PowerShell"
            )
    
    def _is_command_allowed(self, command: str) -> bool:
        """Check if a PowerShell command is in the restricted list.
        
        Args:
            command: The PowerShell command to check
            
        Returns:
            True if the command is allowed, False otherwise
        """
        # Extract the cmdlet name (first word)
        cmdlet = command.strip().split()[0] if command.strip() else ""
        
        # Check if it's in the allowed list
        return cmdlet in self.config['restricted_commands']
    
    def _validate_command(self, command: str) -> tuple[bool, str]:
        """Validate a PowerShell command for safety.
        
        Args:
            command: The PowerShell command to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not command or not command.strip():
            return False, "Empty command"
        
        # Check for dangerous patterns
        dangerous_patterns = [
            'Remove-', 'Delete-', 'Clear-', 'Set-', 'New-', 
            'Stop-', 'Restart-', 'Start-', 'Disable-', 'Enable-',
            'Install-', 'Uninstall-', 'Invoke-Expression', 'iex',
            ';', '|', '&', '>', '>>', '<'
        ]
        
        for pattern in dangerous_patterns:
            if pattern.lower() in command.lower():
                return False, f"Command contains dangerous pattern: {pattern}"
        
        # Check if command is in allowed list
        if not self._is_command_allowed(command):
            cmdlet = command.strip().split()[0] if command.strip() else ""
            return False, f"Command '{cmdlet}' is not in the restricted command list"
        
        return True, ""
    
    def execute_powershell(self, command: str) -> Dict[str, any]:
        """Execute a PowerShell command safely.
        
        Args:
            command: The PowerShell command to execute
            
        Returns:
            Dictionary with execution results
        """
        # Validate command
        is_valid, error_msg = self._validate_command(command)
        if not is_valid:
            return {
                'success': False,
                'error': error_msg,
                'output': '',
                'command': command
            }
        
        try:
            # Execute the command
            result = subprocess.run(
                ['pwsh', '-Command', command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else '',
                'command': command,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command execution timed out',
                'output': '',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': '',
                'command': command
            }
    
    def interpret_request(self, user_request: str) -> Optional[str]:
        """Use LLM to interpret natural language request into PowerShell command.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            PowerShell command or None if interpretation fails
        """
        # Build the system prompt
        system_prompt = f"""You are a PowerShell expert assistant. Convert natural language requests into PowerShell commands.

You can ONLY use these PowerShell cmdlets:
{', '.join(self.config['restricted_commands'])}

Rules:
1. Return ONLY the PowerShell command, no explanations
2. Use only cmdlets from the allowed list
3. Do not use pipes (|), semicolons (;), or redirection operators
4. Do not use any Set-, Remove-, Delete-, or other destructive commands
5. Keep commands simple and safe

If the request cannot be fulfilled with the allowed commands, respond with "CANNOT_EXECUTE"."""

        try:
            # Call the LLM
            response = self.client.chat.completions.create(
                model=self.config['nemotron_model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_request}
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            command = response.choices[0].message.content.strip()
            
            # Check if LLM couldn't fulfill request
            if command == "CANNOT_EXECUTE" or not command:
                return None
            
            return command
            
        except Exception as e:
            print(f"Error interpreting request: {e}", file=sys.stderr)
            return None
    
    def process_request(self, user_request: str) -> Dict[str, any]:
        """Process a natural language request end-to-end.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Dictionary with processing results
        """
        print(f"\n📝 User request: {user_request}")
        
        # Interpret the request
        print("🤖 Interpreting request with Nemotron Nano v2...")
        command = self.interpret_request(user_request)
        
        if not command:
            return {
                'success': False,
                'error': 'Could not interpret request or request requires disallowed commands',
                'user_request': user_request
            }
        
        print(f"💡 Interpreted command: {command}")
        
        # Execute the command
        print("⚡ Executing PowerShell command...")
        result = self.execute_powershell(command)
        
        return {
            'user_request': user_request,
            'interpreted_command': command,
            **result
        }


def main():
    """Main entry point for the agent."""
    print("🚀 PowerShell Natural Language Agent")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = PowerShellAgent()
        
        # Interactive mode
        if len(sys.argv) == 1:
            print("\n💬 Interactive mode. Type 'exit' to quit.")
            print("Enter your requests in natural language.\n")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("👋 Goodbye!")
                        break
                    
                    # Process request
                    result = agent.process_request(user_input)
                    
                    # Display results
                    if result['success']:
                        print(f"\n✅ Success!")
                        print(f"Output:\n{result['output']}")
                    else:
                        print(f"\n❌ Error: {result['error']}")
                
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
        else:
            # Single request mode
            user_request = ' '.join(sys.argv[1:])
            result = agent.process_request(user_request)
            
            if result['success']:
                print(f"\n✅ Success!")
                print(f"Output:\n{result['output']}")
                sys.exit(0)
            else:
                print(f"\n❌ Error: {result['error']}")
                sys.exit(1)
    
    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
