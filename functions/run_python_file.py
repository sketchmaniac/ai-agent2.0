import os
import subprocess
import sys


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Resolve symlinks too, so a path that points outside is rejected.
        working_dir_real = os.path.realpath(working_dir_abs)
        file_path_real = os.path.realpath(absolute_file_path)

        try:
            is_within_working_directory = (
                os.path.commonpath([working_dir_real, file_path_real])
                == working_dir_real
            )
        except ValueError:
            is_within_working_directory = False

        if not is_within_working_directory:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside '
                "the permitted working directory"
            )

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Use the same Python interpreter that is running this function.
        command = [sys.executable, absolute_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if not output:
            output.append("No output produced")

        return "\n".join(output)

    except Exception as error:
        return f"Error: executing Python file: {error}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory, optionally passing command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
