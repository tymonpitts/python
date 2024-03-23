""" Script to fix ofx transaction files downloaded from ANZ to have the payee in the <NAME> field and the card number
in the <MEMO> field since ANZ is not consistent and sometimes does the right thing but other times not.

This operates on the latest downloaded transactions file
"""
import argparse
import pathlib
import re
import shutil


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.parse_args(argv)

    downloads_dir = pathlib.Path.home() / "Downloads"
    transaction_files = [f for f in downloads_dir.glob("01-0504-0302539-00_Transactions_*.ofx") if ".original." not in f.name]
    if not transaction_files:
        print("No downloaded transactions found")
        return

    transaction_files.sort(key=lambda f: f.stat().st_mtime)
    transaction_file = transaction_files[0]
    original_file = downloads_dir / (transaction_file.name.replace(".ofx", "") + ".original.ofx")
    if original_file.exists():
        with original_file.open("r") as f:
            contents = f.read()
    else:
        shutil.copy(transaction_file, original_file)
        with transaction_file.open("r") as f:
            contents = f.read()
    new_contents = re.sub(
        r"<NAME>(?P<card>4835 \*\*\*\* \*\*\*\* (7572|7549) (Df|If))\n<MEMO>(?P<payee>.+)",
        r"<NAME>\g<payee>\n<MEMO>\g<card>",
        contents
    )
    with transaction_file.open("w") as f:
        f.write(new_contents)


if __name__ == "__main__":
    main()
