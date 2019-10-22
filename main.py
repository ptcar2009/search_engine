import argparse
import logging

from search_engine.inverted_index import inverted_index
from search_engine.input import get_file_paths


def main():
    parser = argparse.ArgumentParser(
        description="Python script for search querys in documents.\nBased on TF-IDF."
    )

    parser.add_argument(
        "--query",
        '-q',
        help='Provide the string search query for the parsed documents.',
        type=str
    )

    parser.add_argument(
        '-f',
        '--file',
        help='File path containing the query.',
        type=str
    )

    parser.add_argument(
        '--folder',
        help='Folder that contains the documents that you want to add to the back end.',
        default='data',
        type=str
    )

    parser.add_argument(
        '-n',
        '--number',
        type=int,
        help='Number of results in the query.',
        default=10
    )
    args = parser.parse_args()

    index = inverted_index(get_file_paths(args.folder))

    if args.file and args.query:
        raise SyntaxError("Should not make CLI and file query")
        return
    
    if args.query:
        for f in index.query(args.query, args.number):
            print(f)

        

if __name__ == "__main__":
    main()
