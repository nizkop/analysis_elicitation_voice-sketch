import numpy as np
from datetime import datetime
import pandas as pd
from matplotlib.patches import Patch
import statistics

from src.Tasks.task_topic import TaskTopic
from src.coding.modalities.time_needed_modalities.PureModalityTiming import PureModalityTiming
from src.Tasks.Task import tasks, Task
from src.TaskJsonKind import TaskJsonKind
from src.coding.modalities.time_needed_modalities_statistik import post_hoc_within, \
    within_subjects_anova_modality, within_subjects_anova_language
from src.color_codes import global_colors
from src.get_descriptions import names
from src.participants import participants, Language
from src.plt_settings import my_plt, figure_width, default_height, save_my_figures
from src.statistical_settings import alpha
from src.task_evaluation.statistic_box_plot import compact_letter_display

exceptions_in_language = {
# voice always German for German participants, English for Icelandic participants
#     (task, p)
    ("2", 2): Language.EN,
    ("2", 18): [Language.EN, Language.DE], # EN & DE
    ("3", 2): Language.EN,
    ("3", 18): Language.EN,
    ("4", 26): Language.EN,
    ("6", 2): Language.EN,
    ("8", 2): Language.EN,
    ("9", 2): Language.EN,
    ("9", 26): Language.EN,
    ("14", 2): Language.EN,
    ("15", 2): Language.EN,
    ("16", 26): Language.EN,
    ("20", 2): Language.EN,
}

class CollectionOfPureSketchOrVoiceTimings:

    def __init__(self):
        self.data: list[PureModalityTiming] = []
        self.collect_data()

        self.included_task_ids = None
        self._get_included_tasks_sorted()


    def _get_included_tasks_sorted(self):
        """
        sortiert nach Varianz in Daten
        # list(set([i.task_id for i in self.data]))#TODO: ändert sich in der Reihenfolge = instabil!!!
        :return:
        """
        # 1. Daten nach task_id gruppieren
        if self.included_task_ids is not None:
            return # only use this sorting for the first selection!!!
        groups = {}
        for item in self.data:
            groups.setdefault(item.task_id, []).append(item.time_in_s)

        # 2. Varianzen pro task_id berechnen
        variances = {
            task_id: statistics.variance(values) if len(values) > 1 else 0.0
            for task_id, values in groups.items()
        }

        # 3. task_ids nach Varianz sortieren
        self.included_task_ids = sorted(variances, key=variances.get)
        print("SET:", self.included_task_ids)

    def collect_data(self):
        rows = []
        for task in tasks:
            for p in participants:
                category_array = task.get_category(p=p)
                row = {
                    "task": task.identifier,
                    "participant": p.id,
                    "Categories": category_array
                }
                rows.append(row)
                if category_array is not None:
                    category_array = [i.lower() for i in category_array if i is not None]

                for i in range(len(category_array)):
                    # print(f"task {task.identifier},\tPerson {p.id}:\t", category_array[i])
                    if "gui" in "".join(category_array[i]).lower():
                        continue
                    if "skipped" in "".join(category_array[i]).lower():
                        continue
                    if "sketch" in "".join(category_array[i]) and "voice" in "".join(category_array[i]):
                        # mixed not usable to determine length of pure voice & pure sketch part
                        continue
                    info_dict = task.get_dictionary(p=p, infokind=TaskJsonKind.INFO)
                    if info_dict is None:
                        continue
                    info = info_dict["taskData"]
                    if info is None:
                        continue
                    modality = None
                    if "voice" in "".join(category_array[i]) and len(info["startTimeVoice"]) > 0 and len(
                            info["endTimeVoice"]) > 0:
                        start_time = datetime.strptime(info["startTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        end_time = datetime.strptime(info["endTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        modality = "voice"
                    if "sketch" in "".join(category_array[i]) and len(info["startTimeDrawing"]) > 0 and len(
                            info["endTimeDrawing"]) > 0:
                        start_time = datetime.strptime(info["startTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        end_time = datetime.strptime(info["endTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        modality = "sketch"
                    if modality is not None:
                        language = p.language
                        if (task.identifier, int(p.id)) in exceptions_in_language.keys():
                            language = exceptions_in_language[(task.identifier, int(p.id))]
                        if not isinstance(language, Language):
                            if isinstance(language,list):
                                self._add_task(task=task, modality=modality, language=language[i], solution_index=i,
                                           start_time=start_time, end_time=end_time)
                            continue
                        if language.value == Language.IS.value:
                            language = Language.EN
                        self._add_task(task=task, modality=modality, language=language, solution_index=i,
                                       start_time=start_time, end_time=end_time)


        df = pd.DataFrame(rows)
        df_ex = df.explode("Categories")  # Jede Kategorie wird zur neuen Zeile
        df_ex["Category_index"] = df_ex.groupby(["task", "participant"]).cumcount()

        df = df_ex.pivot(
            index=["task", "participant"],
            columns="Category_index",
            values="Categories"
        ).add_prefix("Category_").reset_index()
        df.to_csv("modality_aufteilung_data.csv", sep=";", mode="w")


    def _add_task(self, task:Task, modality:str, start_time, end_time, language:Language, solution_index:int):
        time_in_s = abs(start_time - end_time).total_seconds()
        if time_in_s > 100:
            print("! long task", task.identifier, language, solution_index)
        p = PureModalityTiming(task_id=task.identifier, task_topic=task.topic.name, task_group=task.get_group(),
                                modality=modality, language=language, solution_index=solution_index,
                                time_in_s=time_in_s)
        self.data.append(p)


    def _filter(self, task_restriction:list[str] = None,
                modality_restriction:list[str] = None,
                language_restriction:list[Language] = None,
                topic_restriction:list[TaskTopic] = None,
                group_restriction:list[str] = None):
        if task_restriction is None:
            task_restriction = self.included_task_ids
        if modality_restriction is None:
            modality_restriction = ["sketch", "voice"]
        if language_restriction is None:
            language_restriction = [Language.DE, Language.EN]
        if topic_restriction is None:
            topic_restriction = [t.name for t in TaskTopic]
        if group_restriction is None:
            group_restriction = ["A", "B", "C"]
        filtered = []
        for d in self.data:
            task_ok = d.task_id in task_restriction
            if len(modality_restriction) >= 2:
                modality_ok = True
            else:
                modality_ok = d.modality in modality_restriction
            if len(language_restriction) >= 2:
                language_ok = True
            else:
                language_ok = d.language in language_restriction
            topic_ok = d.task_topic in topic_restriction
            group_ok = d.task_group in group_restriction
            if task_ok and modality_ok and language_ok and topic_ok and group_ok:
                filtered.append(d)
        return filtered

    def get_modality_data(self, modality:str):
        if modality not in ["voice", "sketch"]:
            raise Exception("")
        filtered = self._filter(modality_restriction=[modality])
        return [d.time_in_s for d in filtered]

    def get_task_data(self, task_id:str):
        filtered = self._filter([task_id])
        return [d.time_in_s for d in filtered]

    def get_language_data(self, language_restriction:list[Language],
                          task_restriction:list[str]=None,
                        modality_restriction:list[str]=None):
        filtered = self._filter(task_restriction=task_restriction,
                                modality_restriction=modality_restriction,
                                language_restriction = language_restriction)
        return [d.time_in_s for d in filtered]


    def get_amount_of_data(self, task_restriction:list, modality_restriction:list, language_restriction:list):
        # filter data to restriction -> then len(data)
        data = self._filter(task_restriction=task_restriction,
                            modality_restriction=modality_restriction,
                            language_restriction=language_restriction)
        return len(data)

    def _format(self, label, data):
        if not isinstance(data, list):
            raise Exception(")")
        return f"{label} = {len(data)}" + (f", {np.median(data):.3f} s" if len(data) > 0 else "")

    def print(self):
        print("\033[1mCollection of pure sketch / pure voice timings:\033[0m")
        print(f"\t{self.get_amount_of_data(task_restriction=self.included_task_ids, 
                                           modality_restriction=['sketch', 'voice'], 
                                           language_restriction=[Language.DE, Language.EN]
                                           )} data points in total")
        # Modalities:
        print("\tDistribution of Amounts for the Modalities:")
        for mod in ["sketch", "voice"]:
            mod_data = self.get_modality_data(modality=mod)
            mod_en_data = self.get_language_data(modality_restriction=[mod], language_restriction = [Language.EN])
            mod_de_data = self.get_language_data(modality_restriction=[mod], language_restriction = [Language.DE])
            print(
                f"\t\t* {len(mod_data)} data points for mod {mod}"
                + (f", median = {np.median(mod_data):.3f}s" if len(mod_data) > 0 else "")
                + f"\t({self._format('EN', mod_en_data)}; {self._format('DE', mod_de_data)})"
            )
        # Tasks:
        print("\tDistribution of Amounts in Tasks:")
        for task in tasks:
            task_data = self.get_task_data(task_id=task.identifier)
            task_en_sketch = self.get_language_data(modality_restriction=["sketch"],task_restriction=[task.identifier],
                                                    language_restriction=[Language.EN])
            task_de_sketch = self.get_language_data(modality_restriction=["sketch"],task_restriction=[task.identifier],
                                                    language_restriction=[Language.DE])
            task_en_voice = self.get_language_data(modality_restriction=["voice"], task_restriction=[task.identifier],
                                                    language_restriction=[Language.EN])
            task_de_voice = self.get_language_data(modality_restriction=["voice"], task_restriction=[task.identifier],
                                                    language_restriction=[Language.DE])
            print(
                f"\t\t* {len(task_data)} data points for task {task.identifier}, "
                f"median = {np.median(task_data):.3f}s\t\t"
                f"({self._format('EN sketch', task_en_sketch)}; "
                f"{self._format('EN voice', task_en_voice)};  \t"
                f"{self._format('DE sketch', task_de_sketch)}; "
                f"{self._format('DE voice', task_de_voice)})"
            )
        print()

    def set_up(self, top_ax, main_ax, max_outlier, highest_wisker):
        highest_wisker = 65 #TODO hard gecodet, damit EN und IS gleich
        top_ax.set_ylim(max_outlier - max_outlier / 100, max_outlier + max_outlier / 100)  # outliers only
        main_ax.set_ylim(0, highest_wisker)

        top_ax.set_yticks([max_outlier])
        top_ax.set_yticklabels([f"{max_outlier:.0f}"])

        # hide the spines between ax and ax2
        top_ax.spines.bottom.set_visible(False)
        main_ax.spines.top.set_visible(False)
        top_ax.xaxis.tick_top()
        # top_ax.tick_params(labeltop=False)  # don't put tick labels at the top
        main_ax.xaxis.tick_bottom()

        d = .5  # Schrägheitsmaß der Unterbrechungslinie
        kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                      linestyle="none", color='k', mec='k', mew=1, clip_on=False)
        top_ax.plot([0, 1], [0, 0], transform=top_ax.transAxes, **kwargs)
        main_ax.plot([0, 1], [1, 1], transform=main_ax.transAxes, **kwargs)

        sorted=False
        if not sorted:
            top_ax.set_xticks([])
        else:
            raise Exception("TODO: impossible until tasks not sorted by group")
            # TODO: impossible until tasks not sorted by group
            unique_groups = []# ['A', 'B', 'C']
            positions = []
            for group in sorted(set(task_group), key=task_group.index):  # Reihenfolge wie im Original
                indices = [i for i, g in enumerate(task_group) if g == group]# [12, 13, 14, 15, 16, 17]
                mean_pos = np.mean(indices)
                unique_groups.append(group)
                positions.append(mean_pos)

            top_ax.set_xticks(positions)
            # [2.5, 8.5, 14.5]
            top_ax.set_xticklabels([names[f"group{i}"] for i in unique_groups], rotation=0)
            top_ax.tick_params(axis='x', width=len(self.included_task_ids) * 28.5 / len(unique_groups))
            top_ax.xaxis.set_label_position('top')
            top_ax.set_xlabel(names["group"])



    def _format_in_loop_time_needed_modalities(self, y_voice_sorted:list[float], y_sketch_sorted:list[float],
                                               box_voice, box_sketch,
                                               max_outlier, highest_whisker):
        if len(y_voice_sorted) == 0 and len(y_sketch_sorted) == 0:
            return max_outlier, highest_whisker
        max_outlier_task = max([i for i in y_voice_sorted + y_sketch_sorted])
        if max_outlier is None or max([max_outlier_task, max_outlier]) != max_outlier:
            max_outlier = max_outlier_task
        q1 = np.percentile(y_voice_sorted + y_sketch_sorted, 25)
        q3 = np.percentile(y_voice_sorted + y_sketch_sorted, 75)
        whisker_top = q3 + 1.5 * (q3 - q1)
        highest_whisker = max(highest_whisker, whisker_top)
        for patch in box_voice['boxes']:
            patch.set_facecolor(global_colors['voice'])
        for patch in box_sketch['boxes']:
            patch.set_facecolor(global_colors['sketch'])
        for flier in box_voice['fliers']:
            flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['voice'], alpha=1,
                      markersize=6)
        for flier in box_sketch['fliers']:
            flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['sketch'], alpha=1,
                      markersize=6)
        return max_outlier, highest_whisker

    def time_needed_modalities_plot(self, languages:list[Language], tasks:list[str] = [],
                                    break_axis:bool = False, info:str = None):
        offset = 0.175
        if not break_axis:
            fig, main_ax = my_plt.subplots(figsize=(figure_width, default_height))
            bbox_to_anchor = (0.65, 1.17)# top right (outside)
            bbox_to_anchor = (0.01, 1)  # top left (Inside)
        else:
            bbox_to_anchor = (0.65, 1.31)# top right (outside)
            bbox_to_anchor = (0.01, 1.14) # top left (inside)
            fig, (top_ax, main_ax) = my_plt.subplots(2, 1, sharex=False, figsize=(figure_width, 6),
                                             gridspec_kw={'height_ratios': [1, 10], "hspace": 0.05})

        max_outlier, q1, q3 = None, None, None
        highest_whisker = 0
        if len(tasks) == 0:
            loopover = self.included_task_ids
            x_axis_key = "taskid"
            x_tick_values = self.included_task_ids
        else:
            loopover = languages
            x_axis_key = "language"
            x_tick_values = [l.value for l in languages]

        total_sketch = []
        total_voice = []
        t_total = len(loopover)
        extra_offset = 0.6
        for t in range(len(loopover)):
            if len(tasks) == 0:
                task_restriction = [self.included_task_ids[t]]
                # print("Restricted to", task_restriction)
                language_restriction = languages
            else:
                task_restriction = tasks
                language_restriction = [languages[t]]
            y_voice_sorted = [i.time_in_s for i in self._filter(task_restriction=task_restriction,
                                                                 modality_restriction=["voice"],
                                                                 language_restriction=language_restriction)]
            box_voice = main_ax.boxplot(y_voice_sorted,
                                            positions=[t - offset],
                                            widths=0.25, patch_artist=True,
                                            showfliers=True)
            total_voice.extend(y_voice_sorted)

            y_sketch_sorted = [i.time_in_s for i in self._filter(task_restriction=task_restriction,
                                                                    modality_restriction=["sketch"],
                                                                    language_restriction=language_restriction)]
            box_sketch = main_ax.boxplot(y_sketch_sorted,
                                             positions=[t + offset],
                                             widths=0.25, patch_artist=True,
                                             showfliers=True)
            total_sketch.extend(y_sketch_sorted)


            if break_axis:
                box_voice_top = top_ax.boxplot(y_voice_sorted, positions=[t + offset],
                                                     widths=0.25, patch_artist=True, showfliers=True)
                box_sketch_top = top_ax.boxplot(y_sketch_sorted, positions=[t + offset],
                                                      widths=0.25, patch_artist=True, showfliers=True)
                self._format_in_loop_time_needed_modalities(
                    y_voice_sorted=y_voice_sorted, y_sketch_sorted=y_sketch_sorted, box_voice=box_voice_top,
                    box_sketch=box_sketch_top, max_outlier=max_outlier, highest_whisker=highest_whisker
                )
            max_outlier, highest_whisker = self._format_in_loop_time_needed_modalities(
                    y_voice_sorted=y_voice_sorted,
                    y_sketch_sorted=y_sketch_sorted,
                    box_voice=box_voice,
                    box_sketch=box_sketch,
                    max_outlier=max_outlier,
                    highest_whisker=highest_whisker
            )

        if break_axis:
            self.set_up(top_ax=top_ax, main_ax=main_ax, max_outlier=max_outlier, highest_wisker=highest_whisker)

        # ADD BARS FOR TOTAL DATA OF THIS PLOT:
        box_voice_total = main_ax.boxplot(total_voice, positions=[t_total - offset+extra_offset], widths=0.25,
                                           patch_artist=True, showfliers=True)
        box_sketch_total = main_ax.boxplot(total_sketch, positions=[t_total + offset+extra_offset], widths=0.25,
                                           patch_artist=True, showfliers=True)
        if break_axis:
            box_voice_total_top = top_ax.boxplot(total_voice, positions=[t_total - offset + extra_offset], widths=0.25,
                            patch_artist=True, showfliers=True)
            box_sketch_total_top = top_ax.boxplot(total_sketch, positions=[t_total + offset + extra_offset], widths=0.25,
                            patch_artist=True, showfliers=True)
            self._format_in_loop_time_needed_modalities(
                y_voice_sorted=total_voice, y_sketch_sorted=total_sketch, box_voice=box_voice_total_top,
                box_sketch=box_sketch_total_top, max_outlier=max_outlier, highest_whisker=highest_whisker
            )
            top_ax.set_xticks([])


        max_outlier, highest_whisker = self._format_in_loop_time_needed_modalities(
            y_voice_sorted=total_voice, y_sketch_sorted=total_sketch, box_voice=box_voice_total,
            box_sketch=box_sketch_total, max_outlier=max_outlier, highest_whisker=highest_whisker
        )

        # FORMAT GRAPH:
        x_positions = np.arange(len(loopover))
        total_pos = len(loopover) + extra_offset
        main_ax.set_xticks(list(x_positions) + [total_pos])
        main_ax.set_xticklabels(x_tick_values + ["total"], rotation=45)
        main_ax.tick_params(axis='x', width=offset * 109)
        main_ax.set_xlabel(names[x_axis_key])
        if max_outlier is None:
            return
        main_ax.set_ylabel(names["time"])
        my_plt.ylim(bottom=0, top=None)
        my_plt.ylabel("Time Spend\nCreating a Command [s]")
        legend_elements = [
            Patch(facecolor=global_colors['voice'], label='Voice'),
            Patch(facecolor=global_colors['sketch'], label='Sketch')
        ]
        legend = my_plt.legend(handles=legend_elements, title=names["modality"] + ":",
                               loc='upper left', bbox_to_anchor=bbox_to_anchor, ncol=2)
        title = "time_needed_modalities"
        if info:
            title += "-" + info
        save_my_figures(title, fig=fig, bbox_extra_artists=[legend])
        my_plt.show()
        return



    def get_dataframe(self, task_restriction:list=None, modality_restriction:list=None, language_restriction:list=None,
                      topic_restriction:list=None, group_restriction:list=None):
        data = self._filter(task_restriction=task_restriction,
                            modality_restriction=modality_restriction,
                            language_restriction=language_restriction,
                            topic_restriction=topic_restriction,
                            group_restriction=group_restriction,
                            )
        rows = []
        for i in data:
            rows.append({
                "id": i.task_id,
                "group": i.task_group,
                "modality": i.modality,
                "time": i.time_in_s,
                "topic": i.task_topic,#str
                "language": i.language,
            })
        df = pd.DataFrame(rows)
        return df


    def time_needed_modalities_statistik_total(self, language_restriction=None,
                                               modality_restriction:list=None,
                                               print_info:bool=False):
        if language_restriction is not None and modality_restriction is not None:
            raise Exception("compare EITHER language OR modality")
        if language_restriction is not None:
            df = self.get_dataframe(language_restriction=language_restriction)
            df_agg, result_total = within_subjects_anova_modality(alpha=alpha, df=df, print_info=print_info)
            sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha, group_col="modality")
        else:
            df = self.get_dataframe(modality_restriction=modality_restriction)
            df_agg, result_total = within_subjects_anova_language(alpha=alpha, df=df, print_info=print_info)
            sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha, group_col="language")
        # gesamt:
        cld_strings_total = compact_letter_display(groups, n, sig_matrix, print_info=print_info)

        if language_restriction is not None:
            print(f"\u001b[1mgesamt {[i.value for i in language_restriction]}\u001b[0m", result_total, "->", cld_strings_total)
        else:
            print(f"\u001b[1mgesamt {[i for i in modality_restriction]}\u001b[0m", result_total, "->", cld_strings_total)
        print()

    def time_needed_modalities_statistik_groups(self, language_restriction=[Language.DE, Language.EN]):
        # group A:
        df_A = self.get_dataframe(language_restriction=language_restriction, group_restriction=["A"])
        df_agg, result_A = within_subjects_anova_modality(alpha=alpha, df = df_A)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_A = compact_letter_display(groups, n, sig_matrix)

        # group B:
        df_B = self.get_dataframe(language_restriction=language_restriction, group_restriction=["B"])
        df_agg, result_B = within_subjects_anova_modality(alpha=alpha, df = df_B)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_B = compact_letter_display(groups, n, sig_matrix)

        # group C:
        df_C = self.get_dataframe(language_restriction=language_restriction, group_restriction=["C"])
        df_agg, result_C = within_subjects_anova_modality(alpha=alpha, df = df_C)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_C = compact_letter_display(groups, n, sig_matrix)

        print()
        print("group A", result_A, "->", cld_strings_A)
        print("group B", result_B, "->", cld_strings_B)
        print("group C", result_C, "->", cld_strings_C)

    def time_needed_modalities_statistik_topics(self, language_restriction=[Language.DE, Language.EN]):
        # Task Topic Editing:
        df_edit = self.get_dataframe(language_restriction=language_restriction, topic_restriction=[TaskTopic.EDITING.name])
        df_agg, result_edit = within_subjects_anova_modality(alpha=alpha, df = df_edit)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_edit = compact_letter_display(groups, n, sig_matrix)

        # FORMATTING:
        df_format = self.get_dataframe(language_restriction=language_restriction, topic_restriction=[ TaskTopic.FORMATTING.name])
        df_agg, result_edit = within_subjects_anova_modality(alpha=alpha, df = df_format)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_format = compact_letter_display(groups, n, sig_matrix)

        # CALCULATION:
        df_calc = self.get_dataframe(language_restriction=language_restriction, topic_restriction=[TaskTopic.CALCULATION.name])
        df_agg, result_edit = within_subjects_anova_modality(alpha=alpha, df = df_calc)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_calc = compact_letter_display(groups, n, sig_matrix)

        # STRUCTURECHANGE
        df_struc = self.get_dataframe(language_restriction=language_restriction, topic_restriction=[TaskTopic.STRUCTURECHANGE.name])
        df_agg, result_edit = within_subjects_anova_modality(alpha=alpha, df=df_struc)
        sig_matrix, groups, n = post_hoc_within(df_agg, alpha=alpha)
        cld_strings_struc = compact_letter_display(groups, n, sig_matrix)

        print()
        print("topic Editing", result_edit, "->", cld_strings_edit)
        print("topic Formatting", result_edit, "->", cld_strings_format)
        print("topic Calculation", result_edit, "->", cld_strings_calc)
        print("topic StructureChange", result_edit, "->", cld_strings_struc)



if __name__ == '__main__':
    c = CollectionOfPureSketchOrVoiceTimings()
    c.print()

    break_axis = False

    languages = [Language.DE, Language.EN]
    # c.time_needed_modalities_plot(languages, break_axis=break_axis)
    # c.time_needed_modalities_plot(languages, break_axis=break_axis, tasks = c.included_task_ids, info="alltasks")
    c.time_needed_modalities_statistik_total(language_restriction=[Language.DE, Language.EN])

    break_axis = True

    # languages = [Language.EN]
    # c.time_needed_modalities_plot(languages, break_axis=break_axis, info="EN")
    # languages = [Language.DE]
    # c.time_needed_modalities_plot(languages, break_axis=break_axis, info="DE")


    for language in [Language.DE, Language.EN]:
        c.time_needed_modalities_statistik_total(language_restriction=[language])
    #     # c.time_needed_modalities_statistik_groups(language_restriction=[language])
    #     # c.time_needed_modalities_statistik_topics(language_restriction=[language])
    #

    c.time_needed_modalities_statistik_total(modality_restriction=["sketch"])
    c.time_needed_modalities_statistik_total(modality_restriction=["voice"])