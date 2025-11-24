"""
Basic unit tests for the PowerShell Computer Use Agent.

These tests verify that the core functionality works correctly without requiring an LLM API.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from powershell import PowerShell


def test_powershell_initialization():
    """Test that PowerShell can be initialized."""
    config = Config()
    pwsh = PowerShell(config)
    
    assert pwsh.cwd is not None
    assert pwsh.pwsh_executable in ['pwsh', 'powershell.exe']
    print("✅ PowerShell initialization test passed")


def test_basic_commands():
    """Test basic PowerShell command execution."""
    config = Config()
    pwsh = PowerShell(config)
    
    # Test Get-Location
    result = pwsh.exec_powershell_command("Get-Location")
    assert "error" not in result
    assert result['cwd'] is not None
    print("✅ Get-Location test passed")
    
    # Test Write-Output
    result = pwsh.exec_powershell_command("Write-Output 'test'")
    assert "error" not in result
    assert "test" in result['stdout']
    print("✅ Write-Output test passed")
    
    # Test Get-ChildItem
    result = pwsh.exec_powershell_command("Get-ChildItem")
    assert "error" not in result
    print("✅ Get-ChildItem test passed")


def test_directory_navigation():
    """Test that directory navigation works and is tracked."""
    config = Config()
    pwsh = PowerShell(config)
    
    initial_dir = pwsh.cwd
    
    # Change to /tmp
    result = pwsh.exec_powershell_command("Set-Location /tmp")
    assert "error" not in result
    assert pwsh.cwd != initial_dir
    assert "/tmp" in pwsh.cwd or "\\tmp" in pwsh.cwd.lower()
    print("✅ Directory navigation test passed")


def test_command_allowlist():
    """Test that the command allowlist works."""
    config = Config()
    pwsh = PowerShell(config)
    
    # Test allowed command
    result = pwsh.exec_powershell_command("Get-ChildItem")
    assert "error" not in result
    
    # Test disallowed command
    result = pwsh.exec_powershell_command("Remove-Item test.txt")
    assert "error" in result
    assert "allowlist" in result['error']
    print("✅ Command allowlist test passed")


def test_command_injection_prevention():
    """Test that command injection attempts are blocked."""
    config = Config()
    pwsh = PowerShell(config)
    
    # Test backtick injection
    result = pwsh.exec_powershell_command("echo `malicious`")
    assert "error" in result
    assert "injection" in result['error']
    
    # Test $() injection
    result = pwsh.exec_powershell_command("echo $(Get-Process)")
    assert "error" in result
    assert "injection" in result['error']
    print("✅ Command injection prevention test passed")


def test_aliases():
    """Test that PowerShell aliases work."""
    config = Config()
    pwsh = PowerShell(config)
    
    # Test common aliases
    for alias in ['ls', 'pwd', 'cd /tmp', 'echo hello']:
        result = pwsh.exec_powershell_command(alias)
        # Should not have allowlist errors (might have other errors like file not found)
        if "error" in result:
            assert "allowlist" not in result.get('error', '')
    
    print("✅ Alias test passed")


def test_file_operations():
    """Test file operations in a temporary directory."""
    config = Config()
    pwsh = PowerShell(config)
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory
        result = pwsh.exec_powershell_command(f"Set-Location '{tmpdir}'")
        assert "error" not in result
        
        # Create a test file
        result = pwsh.exec_powershell_command("New-Item -ItemType File -Name test.txt")
        assert "error" not in result
        
        # List files
        result = pwsh.exec_powershell_command("Get-ChildItem")
        assert "error" not in result
        assert "test.txt" in result['stdout']
        
        # Read file content (empty file)
        result = pwsh.exec_powershell_command("Get-Content test.txt")
        # Empty file should succeed
        assert "error" not in result
        
    print("✅ File operations test passed")


def test_json_schema():
    """Test that the JSON schema is correctly generated."""
    config = Config()
    pwsh = PowerShell(config)
    
    schema = pwsh.to_json_schema()
    
    assert schema['type'] == 'function'
    assert 'function' in schema
    assert schema['function']['name'] == 'exec_powershell_command'
    assert 'parameters' in schema['function']
    assert 'cmd' in schema['function']['parameters']['properties']
    print("✅ JSON schema test passed")


def run_all_tests():
    """Run all tests."""
    print("\nRunning PowerShell Computer Use Agent Tests\n" + "=" * 50 + "\n")
    
    try:
        test_powershell_initialization()
        test_basic_commands()
        test_directory_navigation()
        test_command_allowlist()
        test_command_injection_prevention()
        test_aliases()
        test_file_operations()
        test_json_schema()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        print("=" * 50 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
