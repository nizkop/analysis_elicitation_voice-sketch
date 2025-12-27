import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import scikit_posthocs as sp
import pandas as pd
import networkx as nx

from src.coding.modalities.modality_per_task import modality_choice_per_task
from src.plt_settings import save_my_figures
from src.statistical_settings import alpha
from src.task_evaluation.median_watching_time_tasks import get_box_task


def anova(data_tbl, spalte, alpha, group_col="TaskID"):
    formula = f'{spalte} ~ C({group_col})'
    time_fit = smf.ols(formula, data=data_tbl).fit()
    anova_results = anova_lm(time_fit)

    # Display ANOVA table
    print(anova_results)

    p_value = anova_results.loc[f'C({group_col})', 'PR(>F)']
    if p_value < alpha:
        print("\t-", "signifikante Unterschiede zwischen mindestens zwei Gruppen")
    # print("p-Wert für Faktor C(TaskID):", p_value)

    adj_r_squared = time_fit.rsquared_adj
    print("\t-", adj_r_squared*100, "% der Varianz in", spalte, f"wird durch {group_col} erklärt")

    p_values = time_fit.pvalues
    group_p_values = p_values.drop("Intercept", errors='ignore')
    num_significant = (group_p_values < alpha).sum()
    print("\t-", f"Anzahl signifikante Gruppen: {num_significant}")







def post_hoc(data_tbl: pd.DataFrame,
             spalte: str,
             group_col="TaskID"):
    # Post-hoc Tukey HSD mit scikit-posthocs
    tukey_df = sp.posthoc_tukey(data_tbl, val_col=spalte, group_col=group_col)

    print("\nTukey HSD p-Werte (matrix):")
    print(tukey_df)

    # Signifikanzmatrix: True wenn p > alpha (keine signifikante Differenz)
    sig_matrix = tukey_df.values > alpha
    n = len(tukey_df)
    groups = tukey_df.index.tolist()
    return sig_matrix, groups, n


def compact_letter_display(groups, n, sig_matrix, print_info:bool=True):
    # Graph bauen: Kante = keine signifikante Differenz
    if groups is None:
        return None
    G = nx.Graph()
    G.add_nodes_from(groups)
    for i in range(n):
        for j in range(i + 1, n):
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

    if print_info:
        print("\nCompact Letter Display:")
        for g in sorted(cld_strings):
            print(f"{g}: {cld_strings[g]}")
    return cld_strings


def update_xtick_labels_with_cld(ax, ax2, fig, legend, spalte, cld_strings):
    """
    Ergänzt x-Achsenbeschriftungen um die CLD-Buchstaben.

    :param ax: matplotlib.axes.Axes
    :param cld_strings: dict mit TaskID als key und Buchstaben als value
    """
    new_labels = []
    ticks = ax.get_xticks()
    for label in ax.get_xticklabels():
        text = label.get_text()
        letters = cld_strings.get(text, '')
        # new_label = f"{text}\n{letters}" if letters else text#TODO: Kontrolle, dass x auf beiden Achsen gleich
        new_label = f"{letters}" if letters else text
        new_labels.append(new_label)
    ax2.set_xticklabels(new_labels, rotation=45)
    ax2.xaxis.set_label_position('top')
    ax2.set_xlabel("Significance Group [Compact Letter Display]")
    if legend is None:
        return save_my_figures(f"boxplot_watching_{spalte}_tasks", fig=fig, bbox_extra_artists=[])
    save_my_figures(f"boxplot_watching_{spalte}_tasks", fig=fig, bbox_extra_artists=[legend])


def get_statistik(x_name:str, alpha:float):
    if x_name == "times":
        spalte = "Time"
    elif x_name == "switch_amount":
        spalte = "Switches"
    else:
        raise Exception("unknown x_name", x_name)
    data_tbl, fig, ax, ax2, legend = get_box_task(x_name=x_name, break_axis=True)
    data_tbl[spalte] = pd.to_numeric(data_tbl[spalte], errors='raise')

    anova(data_tbl, spalte, alpha=alpha)

    sig_matrix, groups, n = post_hoc(data_tbl, spalte=spalte)

    cld_strings = compact_letter_display(groups, n, sig_matrix)

    update_xtick_labels_with_cld(ax2=ax2, ax=ax, fig=fig, legend=legend, spalte=spalte, cld_strings=cld_strings)

if __name__ == "__main__":
    get_statistik("switch_amount", alpha=alpha)
    get_statistik("times", alpha=alpha)
