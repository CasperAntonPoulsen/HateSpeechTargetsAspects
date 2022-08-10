import json
import pandas as pd
import os
import argparse
import sys

class ParserWithUsage(argparse.ArgumentParser):
    """ A custom parser that writes error messages followed by command line usage documentation."""

    def error(self, message) -> None:
        """
        Prints error message and help.
        :param message: error message to print
        """
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = ParserWithUsage()
parser.description = "Displays translated text entry with their english annotations"
parser.add_argument("--data_set", help="Which dataset to be displayed, dev or test", required=True, type=str)

args = parser.parse_args()

data_set = args.data_set



dev_set_ids = json.load(open("data/post_ids_dev.json", "r"))
test_set_ids = json.load(open("data/post_ids_test.json", "r"))
main_df = pd.read_csv("data/all_data_waseem_da.csv")
annotation_dev_df = pd.read_csv("data/annotation_dev.tsv", sep="\t")
annotation_test_df = pd.read_csv("data/annotation_test.tsv", sep="\t")

annotation_dev_df["id"] = dev_set_ids
annotation_test_df["id"] =  test_set_ids

dev_df = annotation_dev_df.set_index("id").join(main_df.set_index("id"), on="id", how="inner")
test_df = annotation_test_df.set_index("id").join(main_df.set_index("id"), on="id", how="inner")

targetAspectAnnotationsDanish = []


if data_set == "dev":
    working_df = dev_df
elif data_set == "test":
    working_df = test_df
else:
    print("Error, not a valid data set")
    working_df = []

for i in range(len(working_df)):
    
    row = working_df.iloc[i]

    print(row["text"], "\n", row[["Target1", "Aspect1","Target2", "Aspect2", "Target3", "Aspect3"]],sep="" , end ="\r")

    print()
    print("Press any key to continue (this will clear the terminal)")
    print("Type in 'exit' to quit the program")
    x = input()
    if x == "exit":
        break

    os.system('cls' if os.name == 'nt' else "printf '\033c'")