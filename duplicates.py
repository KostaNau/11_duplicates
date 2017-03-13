import os
import itertools
import argparse
from collections import defaultdict


def parse_arg() -> str:
    parser = argparse.ArgumentParser(description='Anti-Duplicator. \
    The script finds files with equal name and size in a target directory.')
    parser.add_argument('-target', help="path to the target directory")
    args = parser.parse_args()
    target_directory = args.target
    return target_directory


def get_filepaths(target_directory: str) -> str:
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path):
                yield file_path


def are_duplicates(filepath1: str, filepath2: str) -> bool:
    return os.path.basename(filepath1) == os.path.basename(filepath2) and \
            os.path.getsize(filepath1) == os.path.getsize(filepath2)


def find_duplicates(paths_pool: iter) -> defaultdict:
    duplicates = defaultdict(list)
    for file_path_1, file_path_2 in itertools.combinations(paths_pool, 2):
        if are_duplicates(file_path_1, file_path_2):
            duplicates[os.path.basename(file_path_1)].append(file_path_1)
            duplicates[os.path.basename(file_path_1)].append(file_path_2)
    return duplicates


def output_duplicates(duplicates: defaultdict) -> None:
    for name, paths in duplicates.items():
        print('File name: {}'.format(name))
        for path in paths:
            print('Path: {}'.format(path))
        print('==========================================================')


if __name__ == '__main__':
    root_directory = parse_arg()
    all_paths = get_filepaths(root_directory)
    duplicates = find_duplicates(all_paths)
    output_duplicates(duplicates)
