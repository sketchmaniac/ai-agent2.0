import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        working_dir_real = os.path.realpath(working_dir_abs)
        target_dir_real = os.path.realpath(target_dir)

        try:
            is_within_working_directory = (
                os.path.commonpath([working_dir_real, target_dir_real])
                == working_dir_real
            )
        except ValueError:
            is_within_working_directory = False

        if not is_within_working_directory:
            return (
                f'Error: Cannot list "{directory}" as it is outside '
                "the permitted working directory"
            )

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        results = []
        for item in sorted(os.listdir(target_dir)):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            results.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(results)

    except Exception as error:
        return f"Error: {error}"


# Keep the schema at the top level, outside the function and its try block.
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": (
            "Lists files in a specified directory relative to the working "
            "directory, providing file size and directory status"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": (
                        "Directory path to list files from, relative to the "
                        "working directory (default is the working directory itself)"
                    ),
                },
            },
        },
    },
}



