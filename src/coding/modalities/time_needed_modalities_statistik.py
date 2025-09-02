import pandas as pd
from statsmodels.stats.anova import AnovaRM
import itertools
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

from src.Tasks.task_topic import TaskTopic
from src.statistical_settings import alpha
from src.task_evaluation.statistic_box_plot import compact_letter_display
from src.coding.modalities.time_needed_modalities import time_needed_modalities


def within_subjects_anova(df, alpha):
    df_agg = (
        df.groupby(["id", "modality"], as_index=False)["time"]
          .mean()
    )
    aov = AnovaRM(df_agg, depvar="time", subject="id", within=["modality"])
    res = aov.fit()
    print("\n=== Repeated‑Measures ANOVA ===")
    print(res)

    p_val = res.anova_table["Pr > F"][0]
    if p_val < alpha:
        result = f"→ signifikanter Unterschied zwischen sketch & voice (p = {p_val:.4g})"
    else:
        result = f"→ kein signifikanter Unterschied (p = {p_val:.4g})"
    return df_agg, result



def post_hoc_within(data_tbl: pd.DataFrame,
                    alpha: float,
                    value_col: str ="time",
                    group_col: str = "modality",
                    subject_col: str = "id"
                    ):
    """
    Pairwise, dependent (paired) t‑tests for a within‑subjects design.
    Returns a significance matrix (True = no significant difference),
    the list of group names and the number of groups (n).
    """
    groups = data_tbl[group_col].unique()
    n_groups = len(groups)

    p_matrix = np.ones((n_groups, n_groups))

    # für jedes Paar (i,j) gepaarten t‑Test durchführen:
    for (i, g1), (j, g2) in itertools.combinations(enumerate(groups), 2):
        d1 = data_tbl.loc[data_tbl[group_col] == g1].set_index(subject_col)[value_col]
        d2 = data_tbl.loc[data_tbl[group_col] == g2].set_index(subject_col)[value_col]
        common = d1.index.intersection(d2.index)
        d1, d2 = d1.loc[common], d2.loc[common]

        # gepaarter t‑Test
        tstat, p = stats.ttest_rel(d1, d2)
        p_matrix[i, j] = p
        p_matrix[j, i] = p

    triu_idx = np.triu_indices(n_groups, k=1)
    p_vals = p_matrix[triu_idx]

    reject, p_corr, _, _ = multipletests(p_vals, alpha=alpha, method="holm")
    p_matrix[triu_idx] = p_corr
    p_matrix[(triu_idx[1], triu_idx[0])] = p_corr   # spiegeln
    sig_matrix = p_matrix > alpha

    return sig_matrix, list(groups), n_groups



def time_needed_modalities_statistik():
    data_table, fig, ax, ax2 = time_needed_modalities() #update csv
    df = pd.read_csv("boxplot_time_needed.csv")   # id, modality, time

    # gesamt:
    df_agg, result_total = within_subjects_anova(alpha=alpha, df = df)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_total = compact_letter_display(groups, n, sig_matrix)

    # group A:
    df_A = df[df['group'] == 'A']
    df_agg, result_A = within_subjects_anova(alpha=alpha, df = df_A)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_A = compact_letter_display(groups, n, sig_matrix)

    # group B:
    df_B = df[df['group'] == 'B']
    df_agg, result_B = within_subjects_anova(alpha=alpha, df = df_B)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_B = compact_letter_display(groups, n, sig_matrix)

    # group C:
    df_C = df[df['group'] == 'C']
    df_agg, result_C = within_subjects_anova(alpha=alpha, df = df_C)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_C = compact_letter_display(groups, n, sig_matrix)

    # Task Topic Editing:
    df_edit = df[df['topic'] == TaskTopic.EDITING.name]
    df_agg, result_edit = within_subjects_anova(alpha=alpha, df = df_edit)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_edit = compact_letter_display(groups, n, sig_matrix)

    # FORMATTING:
    df_format = df[df['topic'] == TaskTopic.FORMATTING.name]
    df_agg, result_edit = within_subjects_anova(alpha=alpha, df = df_format)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_format = compact_letter_display(groups, n, sig_matrix)

    # CALCULATION:
    df_calc = df[df['topic'] == TaskTopic.CALCULATION.name]
    df_agg, result_edit = within_subjects_anova(alpha=alpha, df = df_calc)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_calc = compact_letter_display(groups, n, sig_matrix)

    # STRUCTURECHANGE
    df_struc = df[df['topic'] == TaskTopic.STRUCTURECHANGE.name]
    df_agg, result_edit = within_subjects_anova(alpha=alpha, df=df_struc)
    sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
    cld_strings_struc = compact_letter_display(groups, n, sig_matrix)

    print()
    print("gesamt", result_total, "->", cld_strings_total)
    print("group A", result_A, "->", cld_strings_A)
    print("group B", result_B, "->", cld_strings_B)
    print("group C", result_C, "->", cld_strings_C)
    print("topic Editing", result_edit, "->", cld_strings_edit)
    print("topic Formatting", result_edit, "->", cld_strings_format)
    print("topic Calculation", result_edit, "->", cld_strings_calc)
    print("topic StructureChange", result_edit, "->", cld_strings_struc)







if __name__ == "__main__":
    time_needed_modalities_statistik()
