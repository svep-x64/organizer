from src import transfer
import shutil

class Run:
    def __init__(self, config, parse_args):
        self.config = config
        self.rules = self.config.rules()
        self.ignore = self.config.ignore()

        self.args = parse_args

        self.iterator = transfer.iter_files(
                self.args.directory,
                recursive=self.args.recursive,
                all=self.args.all,
                ignore=self.ignore,
        )

    def move(self, item, destination):
        if not destination: return

        destination_dir = destination.parent
        destination_dir.mkdir(parents=True, exist_ok=True)

        shutil.move(item, destination)

    # in default mode, skip the file if destination already exists
    def exists(self, item, destination):
        return None

    def run(self):
        for item in self.iterator:
            destination = transfer.destination(item, self.rules)

            if not destination:
                if self.args.show_all:
                    print(f"Skipping {item}, no destination")
                continue

            if destination.exists():
                destination = self.exists(item, destination)

            self.move(item, destination)

class RenameRun(Run):
    # in rename mode, append a number to the filename if destination already exists
    def exists(self, item, destination):
        copy_num = 1
        new_destination = destination.with_name(f"{destination.stem}_{copy_num}{destination.suffix}")
        while new_destination.exists():
            copy_num += 1
            new_destination = destination.with_name(f"{destination.stem}_{copy_num}{destination.suffix}")
        return new_destination

class OverwriteRun(Run):
    # in overwrite mode, replace the existing destination file
    def exists(self, item, destination):
        if destination.is_file():
            destination.unlink()
        return destination

# --dry-run
class Dry:
    def __init__(self, run: Run):
        self._run = run

    # in dry run, no files are actually moved 
    def move(self, item, destination):
        if not destination:
            if self._run.args.show_all:
                print(f"Skipping {item}, no destination")
            return

        print(item)
        print("->", destination)

    def __getattr__(self, name):
        return getattr(self._run, name)
