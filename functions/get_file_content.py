import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        working_dir_real = os.path.realpath(working_dir_abs)
        target_file_real = os.path.realpath(target_file)

        try:
            is_within_working_directory = (
                os.path.commonpath([working_dir_real, target_file_real])
                == working_dir_real
            )
        except ValueError:
            is_within_working_directory = False

        if not is_within_working_directory:
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                "the permitted working directory"
            )

        if not os.path.isfile(target_file):
            return (
                f'Error: File not found or is not a regular file: '
                f'"{file_path}"'
            )

        with open(target_file, "r", encoding="utf-8") as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += (
                    f'[...File "{file_path}" truncated at '
                    f'{MAX_CHARS} characters]'
                )

        return content

    except Exception as error:
        return f"Error: {error}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads and returns the contents of a file relative to the "
            "working directory"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path of the file to read, relative to the working "
                        "directory"
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}
