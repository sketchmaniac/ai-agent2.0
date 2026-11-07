import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Resolve symlinks too, so paths that lead outside are rejected.
        working_dir_real = os.path.realpath(working_dir_abs)
        target_path_real = os.path.realpath(target_path)

        try:
            is_within_working_directory = (
                os.path.commonpath([working_dir_real, target_path_real])
                == working_dir_real
            )
        except ValueError:
            is_within_working_directory = False

        if not is_within_working_directory:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside '
                "the permitted working directory"
            )

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_directory = os.path.dirname(target_path)
        os.makedirs(parent_directory, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f"({len(content)} characters written)"
        )

    except Exception as error:
        return f"Error: {error}"
