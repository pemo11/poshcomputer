#!/usr/bin/env python3
"""
Test script for PowerShell Agent (without LLM)

This script tests the command validation and execution
without requiring an API key.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_command_validation():
    """Test command validation logic."""
    from agent import PowerShellAgent
    
    print("Testing command validation (without API key requirement)...")
    print("=" * 60)
    
    # Create a mock agent without initializing the API client
    class MockAgent(PowerShellAgent):
        def __init__(self):
            # Load configuration without initializing the client
            import json
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            # Skip API client initialization
            self._check_powershell()
    
    agent = MockAgent()
    
    # Test valid commands
    print("\n✅ Testing VALID commands:")
    valid_commands = [
        "Get-Process",
        "Get-Service",
        "Get-Date",
        "Get-ChildItem",
        "Test-Connection localhost"
    ]
    
    for cmd in valid_commands:
        is_valid, msg = agent._validate_command(cmd)
        status = "✅ PASS" if is_valid else f"❌ FAIL: {msg}"
        print(f"  {cmd:40} -> {status}")
    
    # Test invalid commands
    print("\n❌ Testing INVALID commands (should fail):")
    invalid_commands = [
        "Remove-Item test.txt",
        "Set-Service MyService",
        "Get-Process | Stop-Process",
        "Get-ChildItem > output.txt",
        "Invoke-Expression 'malicious code'",
        "Get-UnknownCommand"
    ]
    
    for cmd in invalid_commands:
        is_valid, msg = agent._validate_command(cmd)
        status = "✅ PASS (correctly blocked)" if not is_valid else f"❌ FAIL: Should have been blocked"
        print(f"  {cmd:40} -> {status}")
        if not is_valid:
            print(f"     Reason: {msg}")
    
    # Test actual execution of safe commands
    print("\n⚡ Testing EXECUTION of safe commands:")
    exec_commands = [
        "Get-Date",
        "Get-Location",
        "Test-Path /"
    ]
    
    for cmd in exec_commands:
        result = agent.execute_powershell(cmd)
        if result['success']:
            output_preview = result['output'].strip()[:60]
            print(f"  ✅ {cmd:30} -> {output_preview}...")
        else:
            print(f"  ❌ {cmd:30} -> Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == '__main__':
    test_command_validation()
