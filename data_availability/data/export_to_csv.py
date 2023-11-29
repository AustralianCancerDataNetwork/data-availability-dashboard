import pandas as pd

excel_file = pd.ExcelFile("data_availability_data.xlsx")
centres = ["CHUM", "CHUS", "HMR", "HGJ"]
columns = [
    "Patient #",
    "Age",
    "Sex",
    "Primary Site",
    "T-stage",
    "N-stage",
    "M-stage",
    "TNM group stage",
    "HPV status",
]
cols = [
    "pat_id1",
    "age_diag",
    "sex",
    "category",
    "t_stage",
    "n_stage",
    "m_stage",
    "stage_group",
    "hpv_status",
]


def export_medical_csv():
    df_results = pd.DataFrame(columns=cols)
    for centre in centres:
        df_centre = excel_file.parse(centre)[columns]
        df_centre = df_centre.dropna(how="all")
        df_centre = df_centre[:-1]
        df_centre.columns = cols
        df_centre["stage_group"] = df_centre["stage_group"].apply(
            lambda x: str(x).split(" ")[-1] if isinstance(x, str) else x
        )
        df_results = pd.concat([df_results, df_centre])
    df_results["med_id"] = range(len(df_results))
    df_results.to_csv(f"medical.csv", index=False)


def main():
    export_medical_csv()


main()
