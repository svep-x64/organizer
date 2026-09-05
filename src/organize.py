from src import parse_config
from src import arguments
from src import modes

def main():
    parser = arguments.Parser()
    args = parser.parse_args()

    config = parse_config.Config(args.config)

    # modes are selected according to their priority
    # priority:
    # overwrite (highest)
    # rename
    # skip (default)
    run = modes.Run(config, args)

    if args.rename:
        run = modes.RenameRun(config, args)

    if args.overwrite:
        run = modes.OverwriteRun(config, args)

    # with dry_run, no real changes are made
    if args.dry_run:
        run = modes.Dry(run)

    run.run()

if __name__ == "__main__":
    main()
