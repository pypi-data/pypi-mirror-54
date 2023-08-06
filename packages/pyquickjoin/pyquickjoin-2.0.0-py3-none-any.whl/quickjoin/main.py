import sys
import argparse

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Join two files quickly')

    parser.add_argument('-1', metavar='FIELD', dest="file1_key_column", type=int, default=1, help='join on this FIELD of the data file. Defaults to 1.')
    parser.add_argument('-2', metavar='FIELD', dest="file2_key_column", type=int, default=1, help='join on this FIELD of the lookup file. Defaults to 1.')
    parser.add_argument('-t', metavar='CHAR', dest="separator", default="\t", help='use CHAR as input and output field separator. Defaults to tab.')
    parser.add_argument('-d', '--disk', action='store_true', help='use an on-disk db as the lookup source rather than an in-memory dict (requires bsddb3 or bsddb to be installed)')
    parser.add_argument('data_file', metavar='DATA_FILE', nargs='?', default="-", help="Large file to be streamed. Defaults to stdin.")
    parser.add_argument('lookup_file', metavar='LOOKUP_FILE', help="Smaller file to be read in fully at the start.")

    parsed_args = parser.parse_args(args)

    if len(parsed_args.separator) != 1:
        parser.error("separator CHAR must be exactly 1 character")

    if parsed_args.data_file == "-" and parsed_args.lookup_file == "-" :
        parser.error("both files cannot be standard input")

    data_file = argparse.FileType('r')(parsed_args.data_file)
    lookup_file = argparse.FileType('r')(parsed_args.lookup_file)

    if parsed_args.disk:
        try:
            import bsddb3 as bsddb
        except ImportError:
            pass

        if 'bsddb' not in locals():
            try:
                import bsddb
            except ImportError:
                pass

        if 'bsddb' not in locals():
            parser.error('The -d/--disk option requires bsddb3 or bsddb to be installed. Try: "pip install bsddb3"')

        from . import join_bsddb as join_method
    else:
        from . import join_dict as join_method

    joined = join_method(
        data_file,
        parsed_args.file1_key_column - 1,
        lookup_file,
        parsed_args.file2_key_column - 1,
        parsed_args.separator)

    for line in joined:
        print(line)

if __name__ == "__main__":
    main()
