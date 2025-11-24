from typing import Any, Dict, List
import re
import subprocess
import platform

from config import Config

class PowerShell:
    """
    An implementation of a tool that executes PowerShell commands and keeps track of the working directory.
    """

    def __init__(self, config: Config):
        self.config = config
        # The current working directory (this is tracked and updated throughout the session)
        self.cwd = config.root_dir
        # Determine the PowerShell executable
        self.pwsh_executable = self._find_powershell_executable()
        # Set the initial working directory
        self.exec_powershell_command(f"Set-Location '{self.cwd}'")

    def _find_powershell_executable(self) -> str:
        """
        Find the appropriate PowerShell executable for the platform.
        """
        # Try pwsh (PowerShell Core) first, which works cross-platform
        try:
            result = subprocess.run(
                ["pwsh", "-Version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return "pwsh"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fall back to Windows PowerShell on Windows
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["powershell.exe", "-Version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return "powershell.exe"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
        
        # Default to pwsh
        return "pwsh"

    def exec_powershell_command(self, cmd: str) -> Dict[str, str]:
        """
        Execute the PowerShell command after checking the allowlist.
        """
        if cmd:
            # Prevent command injection via backticks (PowerShell escape character) or variables
            # Allow $ only at the start of tokens (variable references) but not in suspicious contexts
            if re.search(r"[`]", cmd) or re.search(r"\$\(", cmd):
                return {"error": "Command injection patterns are not allowed."}

            # Check the allowlist
            for cmd_part in self._split_commands(cmd):
                if cmd_part not in self.config.allowed_commands:
                    return {"error": f"Parts of this command were not in the allowlist: '{cmd_part}'"}

            return self._run_powershell_command(cmd)

        return {"error": "No command was provided"}

    def to_json_schema(self) -> Dict[str, Any]:
        """
        Convert the function signature to a JSON schema for LLM tool calling.
        """
        return {
            "type": "function",
            "function": {
                "name": "exec_powershell_command",
                "description": "Execute a PowerShell command and return stdout/stderr and the working directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cmd": {
                            "type": "string",
                            "description": "The PowerShell command to execute"
                        }
                    },
                    "required": ["cmd"],
                },
            },
        }

    def _split_commands(self, cmd_str) -> List[str]:
        """
        Split a command string into individual commands, extracting the command names.
        PowerShell commands can be:
        - Cmdlets (e.g., Get-ChildItem)
        - Aliases (e.g., ls, dir, cd)
        - Separated by semicolons, pipes, or other operators
        """
        # Split by common PowerShell separators
        parts = re.split(r'[;|&]+', cmd_str)
        commands = []

        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Extract the first token (command name)
            # Handle quoted strings and parameters
            tokens = re.findall(r'[^\s]+', part)
            
            if tokens:
                # The first token is typically the command
                cmd = tokens[0]
                # Remove any leading/trailing quotes or parentheses
                cmd = cmd.strip("'\"()")
                if cmd:
                    commands.append(cmd)

        return commands

    def _run_powershell_command(self, cmd: str) -> Dict[str, str]:
        """
        Runs the PowerShell command and catches exceptions (if any).
        """
        stdout = ""
        stderr = ""
        new_cwd = self.cwd

        try:
            # Wrap the command so we can keep track of the working directory.
            # Use a unique marker to separate output from the working directory
            # Convert output to string to ensure we get clean text
            wrapped = f"{cmd}; Write-Output '__END__'; (Get-Location).Path"
            
            result = subprocess.run(
                [self.pwsh_executable, "-NoProfile", "-NonInteractive", "-NoLogo", "-Command", wrapped],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout for safety
                env={**subprocess.os.environ, 'NO_COLOR': '1'}  # Disable color output
            )
            
            stderr = result.stderr.strip()
            
            # Find the separator marker
            output_parts = result.stdout.split("__END__")
            
            if len(output_parts) >= 2:
                stdout = output_parts[0].strip()
                # Get the new working directory from the last part
                new_cwd = output_parts[-1].strip()
                if new_cwd and new_cwd != self.cwd:
                    self.cwd = new_cwd
            else:
                stdout = result.stdout.strip()
            
            # If no output/error at all, inform that the call was successful.
            if not stdout and not stderr:
                stdout = "Command executed successfully, without any output."
            
        except subprocess.TimeoutExpired:
            stdout = ""
            stderr = "Command execution timed out after 30 seconds."
        except Exception as e:
            stdout = ""
            stderr = str(e)

        return {
            "stdout": stdout,
            "stderr": stderr,
            "cwd": new_cwd,
        }
