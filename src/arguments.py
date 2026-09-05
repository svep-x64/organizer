import platformdirs
import argparse
import pathlib

class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()

        # main argument specifying the working directory 
        self.add_argument(
                "directory",
                nargs="?",
                type=lambda x: pathlib.Path(x).absolute(),
                default=pathlib.Path.cwd(),
                help="Set work directory (default: current work directory)",
        )

        # specify config file
        CONFIG_DIR = pathlib.Path(platformdirs.user_config_dir("organizer")) 
        DEFAULT_CONFIG = CONFIG_DIR / "config.json"

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        # create config file if not exist
        if not DEFAULT_CONFIG.exists():
            DEFAULT_CONFIG.write_text("""
{
    "rules": {},
    "ignore": []
}
""")
            print(f"Created default config at {DEFAULT_CONFIG}")

        self.add_argument(
                "-c", "--config",
                type=lambda x: pathlib.Path(x).absolute(),
                default=DEFAULT_CONFIG,
                help=f"Path to config file (default: {DEFAULT_CONFIG})",
        )

        # hidden files are skipped by default
        self.add_argument(
                "-a", "--all",
                action="store_true",
                help="Process hidden files",
        )

        # recursively walk through all subdirectories
        self.add_argument(
                "-R", "--recursive",
                action="store_true",
                help="Recursively process all subdirectories",
        )

        # show the planned operations without making changes
        self.add_argument(
                "--dry-run",
                action="store_true",
                help="Show the planned operations without making changes",
        )

        # display skipped files
        self.add_argument(
                "--show-all",
                action="store_true",
                help="Display skipped files in the output",
        )

        # file exist case 1:
        self.add_argument(
                "--skip",
                action="store_true",
                help="Skip the file if a file with same name already exists in destination",
                default=True,
        )

        # file exists case 2:
        self.add_argument(
                "--rename",
                action="store_true",
                help="Rename the file if a file with same name already exists in destination"
        )

        # file exists case 3:
        self.add_argument(
                "--overwrite",
                action="store_true",
                help="Overwrite the destination file if a file with same name already exists"
        )

if __name__ == "__main__":
    parser = Parser()
    print(parser.parse_args())
