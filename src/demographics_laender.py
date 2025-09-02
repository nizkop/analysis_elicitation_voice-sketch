from typing import List
import numpy as np

from src.get_descriptions import names
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height
from src.color_codes import global_colors
from src.languages.translation import translation
from src.participants import participants, Language

topics = ["anyExperienceVoice", "anyExperiencePen", "anyExperienceTablet", "anyExperienceSpreadsheet"]

def get_amounts_of_experience_language(l: Language):
    DE = {}  # List of topics results
    for topic in topics:
        results = {"none": 0, "a little": 0, "a lot": 0}
        for p in participants:
            if p.living_in.value == l.value:
                data = p.get_demographics()
                answer = translation(data[topic])
                results[answer] += 1

        # Calculate percentages
        total_answers = sum(results.values())
        if total_answers != 0:
            # results_percentage = {key: (value / total_answers) * 100 for key, value in results.items()}
            results_percentage = {key: value for key, value in results.items()}

            # Save the percentage results
            DE[topic] = results_percentage
    return DE, total_answers


def get_bar(ax, language:Language, x, topic, added_labels:List[str], width, skip, max_y):
    data, total_answers = get_amounts_of_experience_language(language)# ist etwas ungünstig hier, weil data mit ALLEN topics hier erstellt wird
    label_language = (f"{topic.replace('any', '').replace('Experience', '')}", f"{language.value.upper()}")
    if len(data.items()) == 0:
        return x, label_language, []
    values = [data[topic]["none"], data[topic]["a little"], data[topic]["a lot"]]
    max_y = max(max_y, sum(values))
    if values[0]+values[1]+values[2] != total_answers:
        raise Exception("wth?")
    ax.bar(x=x, height=values[0], bottom=0,         width=width - skip, label="none" if "none" not in added_labels else "", color=global_colors["none"])
    ax.bar(x=x, height=values[1], bottom=values[0], width=width - skip, label="a little" if "a little" not in added_labels else "", color=global_colors["a little"])
    ax.bar(x=x, height=values[2], bottom=values[0]+values[1], width=width - skip, label="a lot" if "a lot" not in added_labels else "", color=global_colors["a lot"])
    added_labels += ["none", "a little", "a lot"]
    return x, label_language, list(set(added_labels)), max_y




def add_group_secondary_xaxis(ax, topics, languages, width=0.35, x_positions=None):
    """
    Fügt dem Diagramm eine zweite x-Achse oben hinzu, die die Sprachunterteilung (IS, DE) anzeigt.

    :param ax: Das matplotlib-Achsenobjekt mit dem Hauptplot.
    :param topics: Liste der Themen (z.B. ["anyExperienceVoice", ...])
    :param languages: Liste der Language-Werte bzw. deren Labels in der Reihenfolge des Plots (z.B. ["IS","DE"])
    :param width: Balkenbreite, für korrekte Positionierung der Gruppen.
    :param x_positions: Positionsliste (NumPy-Array) der Themen, wichtig für Mittelpunkte der Gruppen.
                        Falls None, wird automatisch berechnet (2 Balken pro Thema, gestaffelt)
    """

    # Erzeuge Basis-Positionsarray, wenn nicht angegeben
    import numpy as np
    if x_positions is None:
        x = np.arange(len(topics))
        x_positions = []
        for pos in x:
            for i in range(len(languages)):
                x_positions.append(pos + (i - (len(languages) - 1) / 2) * width)

    group_indices = {lang: idx for idx, lang in enumerate(languages)}

    # Bestimme Start-Ende der x-Positionen für jede Gruppe
    group_positions = {lang: [] for lang in languages}
    n_topics = len(topics)
    for topic_i, topic in enumerate(topics):
        for lang in languages:
            idx = topic_i * len(languages) + group_indices[lang]
            group_positions[lang].append(x_positions[idx])

    # Berechne Mittelpunkte für jede Gruppe über alle Themen
    group_centers = {lang: (min(pos_list) + max(pos_list)) / 2 for lang, pos_list in group_positions.items()}

    # Erstelle sekundäre x-Achse
    secax = ax.secondary_xaxis('top')
    secax.set_xticks(list(group_centers.values()))
    secax.set_xticklabels(list(group_centers.keys()))
    secax.set_xlabel("Language")


def demographics_laender():
    width = 0.4  # Breite eines einzelnen Balkens
    skip = width / 10  # Kleinere Lücke zwischen den Balken


    max_y_DE, max_y_IS = 0, 0
    x = np.arange(len(topics))  # Positionen für die Balken (eine für jedes Thema)
    fig, ax = my_plt.subplots(figsize=(figure_width, default_height))
    second_ax = ax.twinx()
    secax = ax.secondary_xaxis('top')
    ticks = []
    mean_ticks = []
    labels = []
    sec_labels = []
    add_labels = []
    for i, topic in enumerate(topics):
        tick1, label_language1, add_labels, max_y_IS = get_bar(ax=ax, language=Language.IS, x=x[i] - width / 2, topic=topic,
                                                     max_y=max_y_IS, added_labels=add_labels, width=width, skip=skip)
        ticks.append(tick1)
        # labels.append(label_language1[0])
        sec_labels.append(names[label_language1[1].lower()])

        tick2, label_language2, add_labels, max_y_DE = get_bar(ax=ax, language=Language.DE, x=x[i] + width / 2, topic=topic,
                                                            max_y=max_y_DE, added_labels=add_labels, width=width, skip=skip)
        ticks.append(tick2)
        sec_labels.append(names[label_language2[1].lower()])

        if label_language1[0] != label_language2[0]:
            raise Exception(f"should not happen: {label_language1} vs. {label_language2}")
        labels.append(label_language2[0])
        mean_ticks.append(x[i])

    ax.set_xlabel(names["experience"]+":")
    ax.set_ylabel(names["answers%"].replace(r"[\%]", r"of Participants in Iceland [\%]"))
    second_ax.set_ylabel(names["answers%"].replace(r"[\%]", r"of Participants in Germany [\%]"))
    secax.set_xlabel(names["ort"])

    ax.set_xticks(mean_ticks)
    ax.set_xticklabels(labels, rotation=45, ha="center")
    secax.set_xticks(ticks)
    secax.set_xticklabels(sec_labels, rotation=45, ha="left")

    global_max = max(max_y_DE, max_y_IS)
    second_ax.set_ylim(0, global_max)
    ax.set_ylim(0, global_max)
    percentage_values_for_axis = [0, 25, 50, 75, 100]
    second_ax.set_yticks([i * max_y_DE / (100) for i in percentage_values_for_axis])
    ax.set_yticks([i * max_y_IS / (100) for i in percentage_values_for_axis])
    second_ax.set_yticklabels([str(s) for s in percentage_values_for_axis])
    ax.set_yticklabels([str(s) for s in percentage_values_for_axis])

    legend = ax.legend(loc="upper left", title=names["option"], bbox_to_anchor=(0.495, 1.38), ncol = 3)
    save_my_figures("experience_demographics",fig=fig, bbox_extra_artists=[legend])
    my_plt.show()
    my_plt.close()

if __name__ == "__main__":
    demographics_laender()