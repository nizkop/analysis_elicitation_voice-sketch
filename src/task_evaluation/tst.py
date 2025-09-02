# https://pypi.org/project/compactletterdisplay/

import pandas as pd
import compactletterdisplay

from src.task_evaluation.median_watching_time_tasks import get_box_task

# Create your DataFrame:
df = pd.DataFrame({
'control': [1.2, 3.6, 4.2, 2.9, 3.5],
'treatment1': [33.4, 53.7, 23.8, 43.9, 33.7],
'treatment2': [4.2, 2.7, 3.5, 4.1, 3.3],
'treatment3': [33.3, 51.7, 22.5, 43.0, 32.6]
})

# Define columns to perform comparison test on.
columns = ['control', 'treatment1', 'treatment2', 'treatment3']

# Perform ANOVA, pairwise comparison, get compact letter displays
alpha = 0.05
# result_df = compactletterdisplay.anova_cld(data=df, columns=["control", "treatment1"], alpha=0.05, method="TukeyHSD")
#
# print(result_df)



if __name__ == "__main__":
    # Daten im long format:
    data_tbl = get_box_task("switch_amount", True)
    spalte = "Switches"
    data_tbl[spalte] = pd.to_numeric(data_tbl[spalte], errors='raise')

    # Daten umsortieren, Liste je gleicher Id (gleicher x-Wert im Box-plot)
    df_new = {}
    for x,y in data_tbl.values:
        if x not in df_new.keys():
            df_new[x] = [y]
        else:
            df_new[x].append( y )
    # Daten zu dataframe:
    max_len = max([len(x) for x in df_new.values()])
    for i in df_new.keys():
        while len(df_new[i]) < max_len:
            df_new[i].append(None)
    df_new = pd.DataFrame(df_new)
    # statistische signifikanz prüfen:
    print(df_new)
    result_df = compactletterdisplay.anova_cld(data=df_new, alpha=0.05, method="TukeyHSD")
    print(result_df)

