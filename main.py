import os
import platform
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from colorama import Fore, Style
from multiprocessing import Pool, cpu_count


def count_files_in_dir(path):
    print(f"{Fore.RED}\nCounting files this may take ~ 1 min depending on search scope ...{Style.RESET_ALL}")
    return sum(len(files) for _, _, files in os.walk(path))


def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


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

    total_count = count_files_in_dir("/")

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

    total_count = count_files_in_dir("/")

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

    total_count = count_files_in_dir(path)

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


def search_file_name_on_os(file_name):
    file_paths = []
    total_count = count_files_in_dir("/")

    with tqdm(total=total_count, desc=f"Searching for files with name '{file_name}'") as pbar:
        for root, dirs, files in os.walk("/"):
            for file in files:
                if file_name in file:
                    try:
                        file_path = os.path.join(root, file)
                        file_paths.append(file_path)
                    except FileNotFoundError:
                        pass
                pbar.update(1)

    return file_paths


def get_top_10_largest_files(path):
    file_paths = []
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            file_paths.append(os.path.join(root, file))

    file_sizes = []
    with Pool(cpu_count()) as p:
        with tqdm(total=len(file_paths), desc="Calculating file sizes") as pbar:
            for size in p.imap_unordered(get_file_size, file_paths):
                file_sizes.append(size)
                pbar.update()

    largest_files = sorted(zip(file_paths, file_sizes),
                           key=lambda x: x[1], reverse=True)[:10]

    file_names = [os.path.basename(file) for file, _ in largest_files]
    sizes = [size for _, size in largest_files]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(file_names))

    ax.barh(y_pos, sizes, align='center', color='blue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels([os.path.basename(file) for file in file_names])
    ax.invert_yaxis()
    ax.set_xlabel('Size')
    ax.set_title('Top 10 Largest Files')

    for i, v in enumerate(sizes):
        ax.text(
            v + 1, i, f'{convert_bytes_to_readable_format(v)}', color='black', va='center')

    plt.tight_layout()
    plt.show()

    sorted_file_paths = [file for file, _ in largest_files]

    return sorted_file_paths


if __name__ == '__main__':
    print(
        f"\nRunning on OS: {Fore.CYAN} {platform.system()} {platform.release()} {Style.RESET_ALL}")

    while True:
        print(
            f"\n{Fore.YELLOW}{Style.BRIGHT} Please select an option:{Style.RESET_ALL}")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}1.{Style.RESET_ALL} Get total count and size of files on OS")
        print(f"{Fore.BLUE}{Style.BRIGHT}2.{Style.RESET_ALL} Search for files with a specific extension on OS")
        print(f"{Fore.BLUE}{Style.BRIGHT}3.{Style.RESET_ALL} Search for files with a specific extension on a specific directory")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}4.{Style.RESET_ALL} Find a file with a specific name on OS")
        print(f"{Fore.BLUE}{Style.BRIGHT}5.{Style.RESET_ALL} Get top 10 largest files on a specific directory")
        print(f"{Fore.BLUE}{Style.BRIGHT}6.{Style.RESET_ALL} Exit\n")

        choice = input("Enter your choice (1-6): \n")

        if choice == "1":
            total_count, total_size = total_file_count_and_size()
            print("\n")
            print(
                f"Total count of files: {Fore.GREEN}{total_count}{Style.RESET_ALL}")
            print(
                f"Total size of files: {Fore.GREEN}{total_size}{Style.RESET_ALL}")
        elif choice == "2":
            file_type = input(
                f"{Fore.YELLOW}{Style.BRIGHT}Enter file extension to search for (e.g. '.pdf'): {Style.RESET_ALL}")
            count, allocated_space = search_file_type_on_os(file_type)
            print("\n")
            print(
                f"Count of {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{count}{Style.RESET_ALL}")
            print(
                f"Allocated space for {Fore.GREEN}{file_type}{Style.RESET_ALL} files on OS: {Fore.MAGENTA}{allocated_space}{Style.RESET_ALL}")
        elif choice == "3":
            print("\n")
            file_type = input(
                f"{Fore.YELLOW}{Style.BRIGHT}Enter file extension to search for (e.g. '.pdf'): {Style.RESET_ALL}")
            path = input(
                f"{Fore.YELLOW}{Style.BRIGHT}Enter path to search in: {Style.RESET_ALL}")
            count, allocated_space = search_file_type_on_path(file_type, path)
            print("\n")
            print(f"Count of {Fore.GREEN}{Style.BRIGHT}{file_type}{Style.RESET_ALL} files on {Fore.BLUE}{path}{Style.RESET_ALL}: {Fore.MAGENTA}{Style.BRIGHT}{count}{Style.RESET_ALL}")
            print(
                f"Allocated space for {Fore.GREEN}{Style.BRIGHT}{file_type}{Style.RESET_ALL} files on {Fore.BLUE}{path}{Style.RESET_ALL}: {Fore.MAGENTA}{Style.BRIGHT}{allocated_space}{Style.RESET_ALL}")
        elif choice == "4":
            print("\n")
            file_name = input(
                f"{Fore.YELLOW}{Style.BRIGHT}Enter file name to search for (e.g. 'test.txt'): {Style.RESET_ALL}")
            file_paths = search_file_name_on_os(file_name)
            print("\n")
            if len(file_paths) == 0:
                print(
                    f"No files found with name {Fore.GREEN}{Style.BRIGHT}{file_name}{Style.RESET_ALL}")
            else:
                print(
                    f"Files found with name {Fore.GREEN}{Style.BRIGHT}{file_name}{Style.RESET_ALL}:")
                for file_path in file_paths:
                    print(
                        f"{Fore.MAGENTA}{Style.BRIGHT}{file_path}{Style.RESET_ALL}")
        elif choice == "5":
            print("\n")
            path = input(
                f"{Fore.YELLOW}{Style.BRIGHT}Enter path to search in: {Style.RESET_ALL}")
            largest_files = get_top_10_largest_files(path)
            print("\n")
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}Top 10 largest files on {Fore.BLUE}{path}{Style.RESET_ALL}:")
            for idx, file in enumerate(largest_files, start=1):
                print(f"{idx}. {Fore.GREEN}{Style.BRIGHT}{file}{Style.RESET_ALL} - {Fore.MAGENTA}{Style.BRIGHT}{convert_bytes_to_readable_format(get_file_size(file))}{Style.RESET_ALL}")
        elif choice == "6":
            print("\n")
            print(f"{Fore.RED}{Style.BRIGHT}Exiting program...{Style.RESET_ALL}")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
