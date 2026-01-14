import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    absolute_file_path = os.path.abspath(target_file)
    command = ["python", absolute_file_path]

    if args is not None:
        command.extend(args)

    try:
        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            text=True,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as e:
            return f"Error: executing Python file: {e}"

    if completed.returncode != 0:
        return f"Error: Process exited with code {completed.returncode}"

    if completed.stdout == "" or completed.stderr == "":
        return "No output produces"

    return f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file through the Python interpreter",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Additional arguments to pass to the Python interpreter",
            )
        },
    ),
)