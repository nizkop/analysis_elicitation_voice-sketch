import pandas as pd


def convert_table_into_relative_values(file_name:str):
    """
    converts absolute values into percentage values per task
    :return:
    """
    df = pd.read_csv(file_name+".csv", sep=';')
    numeric_cols = df.select_dtypes(include='number').columns
    row_sums = df[numeric_cols].sum(axis=1)
    df_percent = df.copy()
    df_percent[numeric_cols] = round( df[numeric_cols].div(row_sums, axis=0) * 100, 1)

    df_percent.to_csv(file_name+".csv", mode="w", sep=";",
                         header=True, index=False)

    return df_percent
