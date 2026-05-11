import pandas as pd
import os
from datetime import datetime


RANKINGS_FILE = "data/exports/final_rankings.csv"
COMPOUNDERS_FILE = "data/exports/compounders.csv"
INSTITUTIONAL_FILE = "data/exports/institutional_buying.csv"
SECTOR_FILE = "data/exports/sector_rotation.csv"


def export_excel_report():

    print("Generating institutional Excel report...")

    rankings = pd.read_csv(RANKINGS_FILE)

    compounders = pd.read_csv(COMPOUNDERS_FILE)

    institutional = pd.read_csv(INSTITUTIONAL_FILE)

    sectors = pd.read_csv(SECTOR_FILE)

    os.makedirs("data/exports", exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")

    output_file = (
        f"data/exports/"
        f"institutional_report_{date_str}.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        rankings.to_excel(
            writer,
            sheet_name="Institutional Rankings",
            index=False
        )

        compounders.to_excel(
            writer,
            sheet_name="Compounders",
            index=False
        )

        institutional.to_excel(
            writer,
            sheet_name="Institutional Buying",
            index=False
        )

        sectors.to_excel(
            writer,
            sheet_name="Sector Rotation",
            index=False
        )

    print(f"\nExcel report saved to:\n{output_file}")


if __name__ == "__main__":

    export_excel_report()
