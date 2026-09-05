from collections import deque
import pathlib

# walk through the directory tree and yield files to process
def iter_files(root: pathlib.Path,
               **options
               # options:
               # all: bool
               # recursive: bool
):
    dirs = deque()
    dirs.append(root)

    while dirs:
        for item in (dirs.popleft()).iterdir():
            # skip hidden files unless --all is specified
            if item.name.startswith(".") and not options.get("all", False): continue

            if item.is_dir():
                if item in options.get("ignore", {}): continue

                # process all subdirectories when --recursive is specified
                # like in BFS
                if options.get("recursive", False):
                    dirs.append(item)
            else:
                yield item

def destination(file: pathlib.Path, rules):
    path = rules.get(file.suffix, None)
    if path:
        dest_file = pathlib.Path(path).absolute() / file.name

        if file == dest_file: return None
        return dest_file
    else: return None

if __name__ == "__main__":
    print(destination(pathlib.Path.cwd() / "organizer.py", {".py": "/home/s64/Documents/"}))
