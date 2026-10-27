import argparse
import sys

from extractor import extract_movie_info


def main() -> int:
    arg_parser = argparse.ArgumentParser(
        description="Extract structured movie information from a paragraph."
    )
    arg_parser.add_argument(
        "-f", "--file", help="Read the paragraph from a text file instead of prompting."
    )
    args = arg_parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            paragraph = f.read()
    else:
        paragraph = input("Enter a movie paragraph: ")

    try:
        info = extract_movie_info(paragraph)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(info.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
