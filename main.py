import argparse
import logging

from search_engine.tf_idf_ranking import tf_idf_ranking
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

    index = tf_idf_ranking(get_file_paths(args.folder))

    if  args.query:
        raise SyntaxError("Should not make CLI and file query")
        return
    
    if args.query:
        for i, f in enumerate(index.query(args.query, args.number)):
            print(f'{i + 1}: {f}')

        

if __name__ == "__main__":
    main()
