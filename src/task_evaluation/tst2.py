import scikit_posthocs as sp
import pandas as pd
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.sandbox.stats.multicomp import multipletests
import networkx as nx

from src.task_evaluation.median_watching_time_tasks import get_box_task


def anova_with_posthoc_cld(data_tbl, spalte):
    # ANOVA
    formula = f'{spalte} ~ C(TaskID)'
    model = ols(formula, data=data_tbl).fit()
    anova_results = sm.stats.anova_lm(model)
    print(anova_results)



    # Compact Letter Display erstellen

    # Signifikanzmatrix: True wenn p > 0.05 (keine signifikante Differenz)
    sig_matrix = tukey_df.values > 0.05
    n = len(tukey_df)
    groups = tukey_df.index.tolist()

    # Graph bauen: Kante = keine signifikante Differenz
    G = nx.Graph()
    G.add_nodes_from(groups)
    for i in range(n):
        for j in range(i+1, n):
            if sig_matrix[i, j]:
                G.add_edge(groups[i], groups[j])

    # Cliques als Gruppen gleicher Buchstaben
    cliques = list(nx.find_cliques(G))

    # Buchstaben zuteilen (einfach a,b,c,...)
    letters = []
    from string import ascii_lowercase
    letter_dict = dict()
    used = set()
    for i, group in enumerate(groups):
        letter_dict[group] = set()
    for i, clique in enumerate(cliques):
        letter = ascii_lowercase[i]
        for g in clique:
            letter_dict[g].add(letter)

    # Ausgabe als String mit zusammengefassten Buchstaben pro Gruppe
    cld_strings = {g: ''.join(sorted(letters)) for g, letters in letter_dict.items()}

    print("\nCompact Letter Display:")
    for g in sorted(cld_strings):
        print(f"{g}: {cld_strings[g]}")

    return anova_results, tukey_df, cld_strings
# Beispielaufruf:
data_tbl = get_box_task("switch_amount", True)
spalte = "Switches"

data_tbl[spalte] = pd.to_numeric(data_tbl[spalte], errors='raise')
anova_with_posthoc_cld(data_tbl, spalte)