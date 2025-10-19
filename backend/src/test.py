import json
import pandas as pd


def main():
    with open("../data/barclays/parsed/Statement_2025_09.json") as data_file:
        data = json.load(data_file)

    df = pd.DataFrame(data).fillna(0)

    money_in_total = df["Money In (£)"].sum()
    money_out_total = df["Money Out (£)"].sum()
    print(f"In: {money_in_total}, out: {money_out_total}, diff: {money_in_total - money_out_total}")


if __name__ == "__main__":
    main()
