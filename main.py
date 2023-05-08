import os
import platform
import glob
import operator
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Style
from multiprocessing import Pool, cpu_count


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


def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0
    
def total_file_count_and_size():
    total_count = 0
    total_size = 0

    print(f"{Fore.RED}Preparing this may take ~ 1 min ...{Style.RESET_ALL}")

    total_count = sum(len(files) for _, _, files in os.walk("/"))

    file_paths = []
    for root, dirs, files in os.walk("/", topdown=True):
        for file in files:
            file_paths.append(os.path.join(root, file))

    with Pool(cpu_count()) as p:
        with tqdm(total=total_count, desc="Calculating total file size") as pbar:
            for size in p.imap_unordered(get_file_size, file_paths):
                total_size += size
                pbar.update()

    return total_count, convert_bytes_to_readable_format(total_size)


def search_file_type_on_os(file_type):
    count = 0
    allocated_space = 0

    print(f"{Fore.RED}Preparing this may take ~ 1 min ...{Style.RESET_ALL}")
    total_count = sum(len(files) for _, _, files in os.walk("/"))

    with tqdm(total=total_count, desc=f"Searching for files with extension '{file_type}'") as pbar:
        for root, dirs, files in os.walk("/"):
            for file in files:
                if file.endswith(file_type):
                    count += 1
                    try:
                        allocated_space += os.path.getsize(
                            os.path.join(root, file))
                    except FileNotFoundError:
                        pass
                pbar.update(1)


    return count, convert_bytes_to_readable_format(allocated_space)

def search_file_type_on_path(file_type, path):
    count = 0
    allocated_space = 0

    print(f"{Fore.RED}Preparing...{Style.RESET_ALL}")
    total_count = sum(len(files) for _, _, files in os.walk(path))

    with tqdm(total=total_count, desc=f"Searching for files with extension '{file_type}'") as pbar:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(file_type):
                    count += 1
                    try:
                        allocated_space += os.path.getsize(
                            os.path.join(root, file))
                    except FileNotFoundError:
                        pass
                pbar.update(1)

    return count, convert_bytes_to_readable_format(allocated_space)



if __name__ == '__main__':

    
    print(f"\nRunning on OS: {Fore.CYAN} {platform.system()} {platform.release()} {Style.RESET_ALL}")


    total_count, total_size = total_file_count_and_size()
    print(f"Total count of files: {Fore.GREEN}{total_count}{Style.RESET_ALL}")
    print(f"Total size of files: {Fore.GREEN}{total_size}{Style.RESET_ALL}")
    
    file_type = ".pdf"
    download_path = "/Users/selim/Downloads"
    
    count, allocated_space = search_file_type_on_os(file_type)
    print(
        f"Count of {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{count}{Style.RESET_ALL}")
    print(
        f"Allocated space for {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{allocated_space}{Style.RESET_ALL}")
    
    count, allocated_space = search_file_type_on_path(file_type, download_path)
    print(
        f"Count of {Fore.GREEN}{file_type}{Style.RESET_ALL} files on {Fore.MAGENTA}{download_path}{Style.RESET_ALL}: {Fore.MAGENTA}{count}{Style.RESET_ALL}")
    print(
        f"Allocated space for {Fore.GREEN}{file_type}{Style.RESET_ALL} files on {Fore.MAGENTA}{download_path}{Style.RESET_ALL}: {Fore.MAGENTA}{allocated_space}{Style.RESET_ALL}")
    
