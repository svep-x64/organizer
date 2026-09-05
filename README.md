# Organizer
Customize automatic organization of your local files

## Features
- Organize files by their extension
- Recursively process directories
- Optionally process hidden files
- Ignore selected directories
- Preview changes with `--dry-run`
- Choose how to handle duplicate filenames
- Use multiple configuration files

## Installation
```bash
# clone repo
git clone https://github.com/svep-x64/organizer

# build it
cd organizer
pip install .
```
After installation, you can use `organizer` command
```bash
organizer --help
```

## Configuration 
You can create and use as many configuration files as you need with the `--config` option
To see default config file place, look at `--help`

### Rules
The `rules` object maps file extensions to destination directories

For example:
```json
{
    "rules": {
        ".txt": "/home/user/Documents/text",
        ".mp3": "/home/user/Music"
    }
}
```
A file named `example.txt` will be moved to:
```
/home/user/Documents/text/example.txt
```

### Ignore
Directories listed in `ignore` will be skipped during work

Use absolute paths:
```json
{
    "ignore": [
        "/home/user/Documents/IMPORTANT"
    ]
}
```

### Complete config example
```json
{
    "rules": {
        ".txt": "/home/user/Documents/text",
        ".mp3": "/home/user/Music"
    },
    "ignore": [
        "/home/user/Documents/IMPORTANT"
    ]
}
```

## Usage 
Try to run `organizer --help`, to see what it can do
```console
$ organizer --help
usage: organizer [-h] [-c CONFIG] [-a] [-R] [--dry-run] [--show-all]
                 [--skip] [--rename] [--overwrite]
                 [directory]

positional arguments:
  directory            Set work directory (default: current work
                       directory)

options:
  -h, --help           show this help message and exit

  -c, --config CONFIG  Path to config file

  -a, --all            Process hidden files

  -R, --recursive      Recursively process all subdirectories

  --dry-run            Show the planned operations without making changes

  --show-all           Display skipped files in the output

  --skip               Skip the file if a file with same name already
                       exists in destination

  --rename             Rename the file if a file with same name already
                       exists in destination

  --overwrite          Overwrite the destination file if a file with same
                       name already exists
```

## Development
Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
Install the project and dependencies:
```bash
pip install -e .
```

To run the tests:
```bash
pip install pytest
pytest
```

---
