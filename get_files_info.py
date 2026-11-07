import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot list "{directory}" as it is outside '
                "the permitted working directory"
            )

        entries = os.listdir(target_dir)
        entries.sort()

        results = []
        for entry in entries:
            entry_path = os.path.join(target_dir, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            results.append(
                f" - {entry}: file_size={size} bytes, is_dir={is_dir}"
            )

        return "\n".join(results)

    except Exception as error:
        return f"Error: {error}"
