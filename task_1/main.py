import os
import asyncio
import shutil
from argument_parser import ArgumentParser


async def read_folder(folder_path, destination_path):
    r = []
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isdir(full_path):
            r.append(read_folder(full_path, destination_path))
        else:
            r.append(copy_file(full_path, destination_path))

    await asyncio.gather(*r)


async def copy_file(file_path, destination_path):
    ext = get_file_extension(file_path)
    destination_dir = prepare_destination_directory(ext, destination_path)
    if destination_dir is None:
        return

    file_name = os.path.basename(file_path)
    file_destination = os.path.join(destination_dir, file_name)
    try:
        shutil.copy(file_path, file_destination)
    except Exception as e:
        print(f"Failed copying {file_path}: {e}")


def prepare_destination_directory(ext, destination_path):
    directory_path = os.path.join(destination_path, ext)
    if not os.path.exists(directory_path):
        try:
            os.mkdir(directory_path)
        except FileExistsError:
            print(f"Directory '{directory_path}' already exists.")
            return None
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_path}'.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return directory_path


def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == "":
        return "unknown"
    return ext


if __name__ == '__main__':
    args = ArgumentParser()
    asyncio.run(read_folder(args.source_folder, args.output_folder))
