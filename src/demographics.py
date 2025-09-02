import numpy as np

from src.plt_settings import my_plt, save_my_figures, size_2, figure_width, default_height
from participants import participants, demographic_options, Language
from src.color_codes import global_colors
from src.get_descriptions import names
from src.languages.translation import translation


def get_demographic_distribution(property_key: str, translation_active: bool = True, ax=None):
    living_in_options = [Language.DE, Language.IS]
    property = {}
    groups = []
    for j in living_in_options:
        property[j.value] = {}
        for i in demographic_options[property_key]:
            property[j.value][i] = 0
        groups.append(j.value)

    for p in participants:
        data = p.get_demographics()
        if translation_active:
            key = translation(data[property_key])
        else:
            key = data[property_key]
        property[p.living_in.value][key] += 1

    categories = list(demographic_options[property_key])
    x = np.arange(len(categories))
    values_per_group = []
    for group in groups:
        values_per_group.append([property[group][cat] for cat in categories])

    colors = [global_colors[i.value] for i in living_in_options]
    bottom = np.zeros(len(categories))

    if ax is None:
        height = default_height
        bbox_to_anchor = (0.613, 1.16)
        if property_key == 'age':
            height /= 2
            bbox_to_anchor = (0.613, 1.31)
        fig, ax = my_plt.subplots(figsize=(figure_width,height))
        own_figure = True
    else:
        own_figure = False

    for idx, group_values in enumerate(values_per_group):
        bars = ax.bar(x, group_values, bottom=bottom, color=colors[idx], label=names[groups[idx]])
        bottom += np.array(group_values)
    total_heights = np.sum(values_per_group, axis=0)

    for i, total in enumerate(total_heights):
        ax.text(x[i],total*1.006, str(int(total)),
                ha='center', va='bottom',fontsize=size_2, fontweight='bold'
        )
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace("<", r"$<$").replace(">", r"$>$") for c in categories])
    ax.set_xlabel(names[property_key])
    ax.set_ylabel(names["participantNO"])
    if property_key == 'age':
        ax.set_ylim(bottom=0, top=np.max(total_heights)+2)#damit Schrift über Balken passt
    legend=ax.legend(title=names["ort"]+":", bbox_to_anchor=bbox_to_anchor, ncol=2, loc='upper left')

    if own_figure:
        save_my_figures(f"{property_key}", fig=fig, bbox_extra_artists=[legend])
        my_plt.show()
        my_plt.close()
        return None
    else:
        return ax, legend


if __name__ == '__main__':
    get_demographic_distribution("gender")
    get_demographic_distribution("leftHandedOrRightHanded")
    get_demographic_distribution("age", False)


    # get_demographic_distribution("anyExperienceVoice")
    # get_demographic_distribution("anyExperiencePen")
    # get_demographic_distribution("anyExperienceTablet")
    # get_demographic_distribution("anyExperienceSpreadsheet")





# # experience plots:
# keys_to_plot = [
#     "anyExperienceVoice",
#     "anyExperiencePen",
#     "anyExperienceTablet",
#     "anyExperienceSpreadsheet"
# ]
#
# fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# axes = axes.flatten()
#
# for ax, key in zip(axes, keys_to_plot):
#     get_demographic_distribution(key, ax=ax)
#
# plt.tight_layout()
# plt.savefig("combined_demographics.pdf", bbox_inches='tight')
# plt.show()
# plt.close()