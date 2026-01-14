import os

from google.genai import types


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as file:
        content = file.read(10_000)

        # After reading the first MAX_CHARS...
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {10_000} characters]'

        return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the file content, limited to 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory",
            ),
        },
    ),
)
