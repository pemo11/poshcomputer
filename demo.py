#!/usr/bin/env python3
"""
Example usage of the PowerShell Agent (Demo Mode)

This demonstrates the agent's command validation and execution
without requiring an API key. In production, you would provide
natural language input and the LLM would interpret it.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import PowerShellAgent

class DemoAgent(PowerShellAgent):
    """Demo version of the agent that doesn't require an API key."""
    
    def __init__(self):
        """Initialize without API client."""
        import json
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self._check_powershell()
    
    def demo_request(self, description: str, command: str):
        """Demonstrate processing a request with a pre-defined command.
        
        Args:
            description: Natural language description
            command: The PowerShell command to execute
        """
        print(f"\n📝 User request: {description}")
        print(f"💡 Interpreted command: {command}")
        print("⚡ Executing PowerShell command...")
        
        result = self.execute_powershell(command)
        
        if result['success']:
            print(f"\n✅ Success!")
            print(f"Output:\n{result['output']}")
        else:
            print(f"\n❌ Error: {result['error']}")
        
        return result

def main():
    """Run demo examples."""
    print("🚀 PowerShell Natural Language Agent - DEMO MODE")
    print("=" * 70)
    print("NOTE: This demo uses pre-defined commands. In production mode,")
    print("      the Nemotron Nano v2 LLM interprets natural language.")
    print("=" * 70)
    
    agent = DemoAgent()
    
    # Example 1: Get current date
    agent.demo_request(
        "What's the current date and time?",
        "Get-Date"
    )
    
    # Example 2: List running processes
    agent.demo_request(
        "Show me all running processes",
        "Get-Process"
    )
    
    # Example 3: Test network connectivity
    agent.demo_request(
        "Is localhost reachable?",
        "Test-Path /"
    )
    
    # Example 4: Get current location
    agent.demo_request(
        "Where am I?",
        "Get-Location"
    )
    
    # Example 5: Demonstrate blocked command
    print("\n" + "=" * 70)
    print("🛡️  SECURITY DEMO: Attempting to execute a dangerous command")
    print("=" * 70)
    agent.demo_request(
        "Delete all files (malicious request)",
        "Remove-Item *"
    )
    
    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("\nTo use the full agent with LLM interpretation:")
    print("  1. Get an API key from NVIDIA NGC")
    print("  2. Copy .env.example to .env and add your API key")
    print("  3. Run: python agent.py")
    print("=" * 70)

if __name__ == '__main__':
    main()
