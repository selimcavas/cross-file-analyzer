import os
import glob
import operator
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Style


def convert_bytes_to_readable_format(size):
    if size >= 1024**3:
        size = f"{size / 1024**3:.2f} GB"
    elif size >= 1024**2:
        size = f"{size / 1024**2:.2f} MB"
    elif size >= 1024:
        size = f"{size / 1024:.2f} KB"
    else:
        size = f"{size} B"

    return size


def total_file_count_and_size():
    total_count = 0
    total_size = 0

    print(f"{Fore.RED}Preparing...{Style.RESET_ALL}")

    total_count = sum(len(files) for _, _, files in os.walk("/"))

    with tqdm(total=total_count, desc="Calculating total file size") as pbar:
        for root, dirs, files in os.walk("/", topdown=True):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
                pbar.update(1)

    return total_count, convert_bytes_to_readable_format(total_size)


def search_file_type_on_os(file_type):
    count = 0
    allocated_space = 0

    print(f"{Fore.RED}Preparing...{Style.RESET_ALL}")
    total_count = sum(len(files) for _, _, files in os.walk("/"))

    with tqdm(total=total_count, desc=f"Searching for files with extension '{file_type}'") as pbar:
        for root, dirs, files in os.walk("/"):
            for file in files:
                if file.endswith(file_type):
                    count += 1
                    allocated_space += os.path.getsize(
                        os.path.join(root, file))
                pbar.update(1)

    return count, convert_bytes_to_readable_format(allocated_space)


if __name__ == '__main__':
    total_count, total_size = total_file_count_and_size()
    print(f"Total count of files: {Fore.GREEN}{total_count}{Style.RESET_ALL}")
    print(f"Total size of files: {Fore.GREEN}{total_size}{Style.RESET_ALL}")
    file_type = ".txt"
    count, allocated_space = search_file_type_on_os(file_type)
    print(
        f"Count of {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{count}{Style.RESET_ALL}")
    print(
        f"Allocated space for {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{allocated_space}{Style.RESET_ALL}")
