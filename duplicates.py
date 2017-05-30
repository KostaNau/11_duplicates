import os
import argparse
import hashlib
import sys
from collections import defaultdict


def parse_arg() -> bytes:
    parser = argparse.ArgumentParser(description='Anti-Duplicator. \
    The script finds files with equal name and size or with hash comparison\
     in a target directory.')
    parser.add_argument('target',
                        help="path to the target directory")
    parser.add_argument('--md5',
                        type=bool,
                        default=False,
                        help="Toggle for md5 comparison. By default is False.")
    args = parser.parse_args()
    return args


def fetch_file_info(file_path: str, hash_md5: bool) -> str:
    f_info = os.path.getsize(file_path)
    if hash_md5:
        f_info = get_md5checksum(file_path)
    return f_info


def get_md5checksum(file_path: str) -> str:
    buffer_size = 4096
    try:
        f_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(buffer_size), b""):
                f_hash.update(chunk)
    except PermissionError as ex:
        sys.stderr.write('ERROR >>> {}'.format(ex))
    return f_hash.hexdigest()


def get_files_stack(target_directory: str, hash_md5=False) -> defaultdict:
    files_pool = defaultdict(list)
    for subdir, dirs, files in os.walk(target_directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            file_info = fetch_file_info(file_path, hash_md5)
            files_pool[file, file_info].append(file_path)
    return files_pool


def find_duplicates(files_pool: defaultdict) -> defaultdict:
    duplicates_pool = defaultdict(list)
    for name, paths in files_pool.items():
        if len(paths) > 1:
            duplicates_pool[name].extend(paths)
    return duplicates_pool


def output_duplicates(duplicates: defaultdict) -> None:
    for name, paths in duplicates.items():
        print('File name: {}'.format(name[0]))
        for path in paths:
            print('Path: {}'.format(path))
        print('==========================================================')
    print('Total duplicates: ', len(duplicates.keys()))


def main():
    options = parse_arg()
    root_directory = options.target
    files_pool = get_files_stack(root_directory, hash_md5=options.md5)
    duplicates = find_duplicates(files_pool)
    output_duplicates(duplicates)


if __name__ == '__main__':
    main()
