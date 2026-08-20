import parse_config
import argparse
import pathlib
import shutil
import ctypes
import os

parser = argparse.ArgumentParser()

parser.add_argument(
        "directory",
        nargs="?",
        type=lambda x: pathlib.Path(x).absolute(),
        default=pathlib.Path.cwd(),
)
parser.add_argument(
        "-c", "--config",
        type=lambda x: pathlib.Path(x).absolute(),
        default=pathlib.Path.cwd() / "organize.json",
)
parser.add_argument(
        "-R", "--recursive",
        action="store_true",
)
parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="check hidden files",
)

args = parser.parse_args()

files = [x.name for x in args.directory.glob('*')]

config_file = parse_config.Config(args.config)
config = config_file.parse()
ignore = list(map(lambda x: pathlib.Path(x).absolute(), config_file.ignore()))

def is_hidden(file_path: pathlib.Path) -> bool:
    if file_path.name.startswith("."): return True
    if os.name == "nt":
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
            return attrs != -1 and bool(attrs & 0x2)
        except AttributeError:
            pass
    return False

directories = []
directories.append(args.directory)
for directory in directories:
    if directory in ignore: continue
    if is_hidden(directory) and not args.all: continue
    for item in directory.iterdir():
        if is_hidden(item) and not args.all: continue
        if item.is_dir() and args.recursive:
            directories.append(item)
        if config.get(item.suffix, False):
            print(f'moving "{item.name}" to "{config[item.suffix]}"')
            shutil.move(item, config[item.suffix])
