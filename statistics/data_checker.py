import pandas as pd


def analyze_dataset(file):

    if file.name.endswith(".csv"):

        df = pd.read_csv(file)

    else:

        df = pd.read_excel(file)


    report = {

        "rows": len(df),

        "columns": len(df.columns),

        "missing_values":
            df.isnull().sum().to_dict(),

        "data_types":
            df.dtypes.astype(str).to_dict(),

        "summary":
            df.describe().to_dict()

    }


    return df, report
