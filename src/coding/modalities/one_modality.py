from src.color_codes import global_colors
from src.get_descriptions import names
from src.participants import participants
from src.Tasks.Task import tasks
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height

import numpy as np



def one_modality():
    data = []
    participant_labels = []
    for p in participants:
        participant_labels.append(p.id)
        used_modalities_amounts = {
            "GUI": 0,
            "sketch": 0,
            "voice": 0,
            "voice+sketch": 0,
        }
        for task in tasks:
            if task.coded(p=p) and not task.missunderstood(p) and not task.skipped(p):
                category_array = task.get_category(p=p)
                category_array = [i.lower() for i in category_array if i is not None]
                if category_array is not None and len(category_array) > 0:
                    if "gui" in "".join(category_array).lower():
                        used_modalities_amounts["GUI"] += 1
                    if "sketch" in "".join(category_array) and "voice" in "".join(category_array):
                        used_modalities_amounts["voice+sketch"] += 1
                    elif "sketch" in "".join(category_array):
                        used_modalities_amounts["sketch"] += 1
                    elif "voice" in "".join(category_array):
                        used_modalities_amounts["voice"] += 1


        used_modalities = [key for (key, value) in used_modalities_amounts.items() if value > 0]
        used_modalities = list(set(used_modalities))
        if len(used_modalities) == 0:
            raise Exception(f"No modalities found for participant: {p.id}")
        if len(used_modalities) == 1:
            print("participant", p.id, "used only", used_modalities[0])
        if len(used_modalities) == 2 and "GUI" in used_modalities:
            print("participant", p.id, "uses GUI and only 1 modality:", used_modalities)
        # if "GUI" in used_modalities:
        #     print(f"\'p{p.id}\'", end=", ")
        # else:
        #     print("participant", p.id, "used", used_modalities, used_modalities_amounts)
        data.append(used_modalities_amounts)
    return used_modalities_amounts, data, participant_labels



def plot_one_modality():
    used_modalities_amounts_of_last_p, data, participant_labels = one_modality()

    modalities = used_modalities_amounts_of_last_p.keys()

    percentual_values = []
    for participant_data in data:
        percentual_values.append([participant_data.get(mod, 0) for mod in modalities])
    percentual_values = np.array(percentual_values)

    # calculate percent values:
    zeilen_summen = percentual_values.sum(axis=1, keepdims=True)
    zeilen_summen[zeilen_summen == 0] = 1
    werte_norm = percentual_values / zeilen_summen * 100

    # bar chart:
    fig, ax = my_plt.subplots(figsize=(figure_width, default_height))

    x = np.arange(len(data))
    colors = [global_colors[mod] for mod in modalities]
    unten = np.zeros(len(data))
    for i, mod in reversed(list(enumerate(modalities))):  # GUI hinten
        ax.bar(x, werte_norm[:, i], bottom=unten, label=mod, color=colors[i])
        unten += werte_norm[:, i]
    # format:
    step = 2
    ax.set_xticks(x[::step])
    ax.set_xticklabels([f"p{participant_labels[i]}" for i in range(0, len(participant_labels), step)], rotation=45)
    ax.set_xlabel(names["participants"])
    ax.set_ylabel(r'Amount of solved tasks [\%]')
    ax.set_ylim(0, 100)  # 0-100 %
    legend = ax.legend(loc='upper center',
              bbox_to_anchor=(0.5518, 1.15),
              borderaxespad=0,
              title=names["modality"],
              ncol=4)
    # plt.title("Choosen Modalities per participant")
    save_my_figures("preferred_modality_per_participant", fig=fig, bbox_extra_artists = [legend])
    my_plt.show()
    my_plt.close()


if __name__ == "__main__":
    plot_one_modality()




