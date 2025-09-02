import copy
import re

from collections import Counter
import matplotlib.patches as mpatches

from scipy.special.cython_special import huber
from upsetplot import from_memberships, UpSet

from src.color_codes import global_colors
from src.get_descriptions import names
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height
import warnings
from src.languages.translation import translation
from src.participants import participants, Language


def get_mother_languages():
    languages = {}
    language_list = []
    for p in participants:
        data = p.get_demographics()["nativeLanguage"].strip()
        language_of_one_participant = re.split(r'[,\s]+', data)
        language_of_one_participant = [lang.lower().strip() for lang in language_of_one_participant
                                       if len(lang) > 0 and lang.strip()]
        language_of_one_participant = [translation(s) for s in language_of_one_participant]
        language_list.append(tuple(language_of_one_participant))
        if p.language == Language.DE:
            if not "german" in language_of_one_participant:
                print("! NICHT MUTTERSPRACHLER", p.id, p.language, language_of_one_participant)
        elif p.language == Language.EN:
            if not "English".lower() in language_of_one_participant and "English" not in language_of_one_participant:
                print("! NO MOTHERLANGUAGE", p.id, p.language, language_of_one_participant)
        elif p.language == Language.IS:
            if not "iceland" in language_of_one_participant:
                print("! NO MOTHERLANGUAGE", p.id, p.language, language_of_one_participant)

        for i in language_of_one_participant:
            if len(i) == 0:
                print("error:", language_of_one_participant, p.id, flush=True)
                raise Exception(f"wth, {language_of_one_participant}, {i}")
            # adapting keys:
            key = i.lower()
            try:
                languages[key] += 1
            except KeyError:
                languages[key] = 1

    return languages, language_list

def change_bar_color(bar, color_code):
    bar.set_facecolor(global_colors[color_code])
    bar.set_edgecolor(global_colors[color_code])

def color(axes, languages, fig):
    # plot on left hand side:
    bars = axes[2].patches
    x_axis_order = copy.deepcopy(sorted(languages.items(), key=lambda item: item[0], reverse=False))

    for key, value in languages.items():
        # print(key, value)
        bar_index = x_axis_order.index((key, value))
        if bar_index != -1:
            if "german" == key:
                change_bar_color(bar=bars[bar_index], color_code="de")
            elif "icelandic" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "english" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "greek" == key:
                change_bar_color(bar=bars[bar_index], color_code="de")
            elif "hindi" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "hungarian" == key:
                change_bar_color(bar=bars[bar_index], color_code="de")
            elif "telugu" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "ukrainian" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "russian" == key:
                change_bar_color(bar=bars[bar_index], color_code="de")
            elif "persian" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            elif "polish" == key:
                change_bar_color(bar=bars[bar_index], color_code="is")
            else:
                print("!! unknown color language ", key)
    # TODO hard gecodet:
    bars = axes[3].patches
    change_bar_color(bar=bars[0], color_code="de")
    change_bar_color(bar=bars[1], color_code="is")
    change_bar_color(bar=bars[2], color_code="de")
    change_bar_color(bar=bars[3], color_code="de")
    change_bar_color(bar=bars[4], color_code="de")
    change_bar_color(bar=bars[5], color_code="is")#ukrainian
    change_bar_color(bar=bars[6], color_code="is")#english
    change_bar_color(bar=bars[7], color_code="is")#teglu+hindi
    change_bar_color(bar=bars[8], color_code="is")#persian
    change_bar_color(bar=bars[9], color_code="is")#polish

    # add legend:
    legend_labels = {
        'Germany': global_colors['de'],
        'Iceland': global_colors['is'],
    }
    patches = [mpatches.Patch(color=color, label=lang) for lang, color in legend_labels.items()]
    return fig.legend(handles=patches, title=names["ort"], loc='upper left', ncol=2, bbox_to_anchor=(0.436, 0.985))


def format_axes(fig):
    # Linien an sinnvollen Stellen:
    axes = fig.get_axes()
    axes[3].grid(False)
    axes[3].xaxis.set_visible(True)
    axes[3].tick_params(axis='x', labelbottom=False, bottom=True)
    axes[3].spines['bottom'].set_visible(True)
    axes[3].spines['top'].set_visible(True)
    axes[3].spines['right'].set_visible(True)
    axes[2].grid(False)
    axes[2].spines['top'].set_visible(True)
    axes[2].spines['left'].set_visible(True)
    axes[2].spines['right'].set_visible(True)
    axes[2].set_xlim(40,0)
    axes[2].yaxis.set_visible(True)
    axes[2].yaxis.set_ticks_position('right')
    axes[2].tick_params(axis='y', which='both', right=True, left=False, labelright=False, labelleft=False)

    #Verhältnis der Graphiken zueinander:
    pos_left = axes[2].get_position()
    new_pos_left = [pos_left.x0-0.16, pos_left.y0, pos_left.width * 2.5, pos_left.height]
    axes[2].set_position(new_pos_left)
    pos_total = axes[0].get_position()
    new_pos_total = [pos_left.x0-0.16, pos_total.y0, pos_total.width + pos_left.width *1.65, pos_total.height]
    axes[0].set_position(new_pos_total)
    return axes


def mother_language():
    languages, language_list = get_mother_languages()
    warnings.simplefilter(action='ignore', category=FutureWarning)

    counts = Counter(language_list)
    series = from_memberships(counts.keys(), data=list(counts.values()))

    # print(languages)
    fig = my_plt.figure(figsize=(figure_width, default_height))
    upset = UpSet(series, show_counts=False, show_percentages=False,
                  sort_by='cardinality', sort_categories_by=None)

    upset.plot(fig=fig)

    axes = format_axes(fig)

    legend = color(axes, languages, fig)

    axes[1].set_ylabel("Native Language [ ]",labelpad=15)
    # axes[1].set_ylabel('mother languages')
    # axes[2].set_ylabel("YY")
    axes[3].set_ylabel("Amount of\nParticipants Having\nIdentical\nNative Languages [ ]",
                       va="center",
                       rotation=0, labelpad=80)#Intersection Size

    # axes[0].set_xlabel("xxx")
    # axes[1].set_xlabel("xxx")
    txt = axes[2].set_xlabel('Amount of Participants\nHaving this Native Language [ ]')
    # axes[3].set_xlabel("X")

    save_my_figures("mother_language", bbox_extra_artists=axes+[txt, legend])
    my_plt.show()

if __name__ == "__main__":
    mother_language()