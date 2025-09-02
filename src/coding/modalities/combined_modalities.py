from datetime import datetime
import matplotlib.patches as mpatches

from help_scripts.known_errors_json import time_data_error
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height, size_2
from src.Tasks.Task import tasks
from src.TaskJsonKind import TaskJsonKind
from src.color_codes import global_colors, get_mischfarbe
from src.get_descriptions import names
from src.participants import participants


def get_data_combined_modalities():
    sketch_and_voice = {}
    total_number_of_categoried_tasks = 0
    task_data_in_combined_modality = []
    participant_labels = []
    for p in participants:
        participant_labels.append(p.id)
        for task in tasks:
            if task.coded(p=p) and not task.missunderstood(p) and not task.skipped(p):
                    category_array = task.get_category(p=p)
                    category_array = [i.lower() for i in category_array if i is not None]
                    for category in category_array:
                        total_number_of_categoried_tasks += 1
                        if "voice" in "".join(category) and "sketch" in "".join(category):
                            if f"p{p.id}" in sketch_and_voice.keys():
                                sketch_and_voice[f"p{p.id}"].append(task.identifier)
                            else:
                                sketch_and_voice[f"p{p.id}"] = [task.identifier]
                            # try:
                            data = task.get_dictionary(p=p, infokind=TaskJsonKind.INFO)
                            if data is not None and data["taskData"] is not None:
                                data = data["taskData"]
                                if not ( p.id in time_data_error.keys() and task.identifier in time_data_error[p.id]):
                                    print(task.identifier, p.id, ":", ",".join(category_array))
                                    time_start_voice = datetime.strptime(data["startTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                    time_end_voice = datetime.strptime(data["endTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                    time_start_sketch = datetime.strptime(data["startTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")
                                    time_end_sketch = datetime.strptime(data["endTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")

                                    start_point = min(time_start_sketch, time_start_voice)
                                    total_creation_time = max(time_end_voice, time_end_sketch) - start_point
                                    time_start_sketch -= start_point
                                    time_start_voice -= start_point
                                    time_end_sketch -= start_point
                                    time_end_voice -= start_point

                                    # relative durations:
                                    task_data = {
                                        "task": task.identifier,
                                        "p": p.id,
                                        "relative_sketch_start": time_start_sketch.total_seconds() / total_creation_time.total_seconds(),
                                        "relative_sketch_end": time_end_sketch.total_seconds() / total_creation_time.total_seconds(),
                                        "relative_voice_start": time_start_voice.total_seconds() / total_creation_time.total_seconds(),
                                        "relative_voice_end": time_end_voice.total_seconds() / total_creation_time.total_seconds(),
                                    }
                                    task_data_in_combined_modality.append(task_data)
                                    # print("starts talking after", time_start_voice.total_seconds() / total_creation_time.total_seconds())
                                    # print("starts sketching after", time_start_sketch.total_seconds() / total_creation_time.total_seconds())
                                # except Exception as e:
                                #     if
                                #     print(task.identifier, p.id, ":", ",".join(category_array), "->", e)
                                #     raise Exception(e)

    return sketch_and_voice, sketch_and_voice, total_number_of_categoried_tasks, task_data_in_combined_modality





def sort(task_data_in_combined_modality):
    for i in range(len(task_data_in_combined_modality)):
        item = task_data_in_combined_modality[i]
        s_start = item["relative_sketch_start"]
        s_end = item["relative_sketch_end"]
        v_start = item["relative_voice_start"]
        v_end = item["relative_voice_end"]
        task_data_in_combined_modality[i]["overlaps?"] = (( v_start < s_start and v_end > s_start)#voice startet zuerst, endet aber später als sketch beginnt
                                                        or
                                                        ( s_start < v_start and s_end > v_start)#sketch startet zuerst, endet aber später als voice beginnt
                                                        )
        if v_start < s_start:#voice startet zuerst
            task_data_in_combined_modality[i]["overlap"] = v_end - s_start
            task_data_in_combined_modality[i]["zuerstBeginnendes"] = v_end - v_start
        elif s_start < v_start:#sketch startet zuerst
            task_data_in_combined_modality[i]["overlap"] = s_end - v_start
            task_data_in_combined_modality[i]["zuerstBeginnendes"] = s_end - s_start
        else:
            task_data_in_combined_modality[i]["overlap"] = 0

    # sort:
    return sorted(
            task_data_in_combined_modality,
            key=lambda x: (x["p"], x["overlaps?"], x["zuerstBeginnendes"])
        )



def plot(task_data_in_combined_modality):
    fig, ax = my_plt.subplots(figsize=(figure_width, default_height*2))

    yticks = []
    y_pos = 0
    height = 0.6  # Höhe des Balkens
    participant = None
    participants_range = 0
    for index in range(len(task_data_in_combined_modality)+1):
        data = task_data_in_combined_modality[index]
        label = f"Task {data['task']} - P{data['p']}"
        if data["p"] != participant or index == len(task_data_in_combined_modality)-1:
            if participant is not None or index == len(task_data_in_combined_modality)-1:# Ende eines Participants:
                if participants_range > height:
                    x = -3
                elif participant == "109":
                    x = -4*2
                else:
                    x =-2.3*2
                factor = 1.3 if participants_range > height else 1.1
                ax.text(x, -participants_range / 2 + y_pos -height/factor, f"p{participant}",
                        va='center', ha='center', fontsize=size_2, color='black', fontweight='bold')
                ax.axhline(y= y_pos - height/2, color='black', linestyle='-', linewidth=1)
                if index == len(task_data_in_combined_modality)-1:
                    break
            # start eines (neuen) participants:
            participant = data["p"]
            participants_range = 0
            yticks.append(y_pos-height/2)

        sketch_start = data["relative_sketch_start"]
        sketch_width = data["relative_sketch_end"]- sketch_start
        ax.barh(y_pos, sketch_width*100, left=sketch_start*100, height=height,
                color=global_colors["sketch"], alpha=1)

        voice_start = data["relative_voice_start"]
        voice_width = data["relative_voice_end"] - voice_start
        ax.barh(y_pos, voice_width*100, left=voice_start*100, height=height,
                color=global_colors["voice"], alpha=1)

        # Zeichne overlap of sketch+voice:
        if data["overlaps?"]:
            if data["relative_voice_start"] < data["relative_sketch_start"]:
                # voice startet -> Überlapp beginnt ab sketch
                overlap_start = data["relative_sketch_start"]
            elif data["relative_voice_start"] > data["relative_sketch_start"]:
                overlap_start = data["relative_voice_start"]
            else:
                raise Exception("strange")
            if data["relative_voice_end"] < data["relative_sketch_end"]:
                # voice endet zuerst -> Überlapp endet mit voice
                overlap_end = data["relative_voice_end"]
            elif data["relative_voice_end"] > data["relative_sketch_end"]:
                overlap_start = data["relative_sketch_end"]
            else:
                raise Exception("strange")
            overlap_width = overlap_end - overlap_start
            ax.barh(y_pos, overlap_width * 100, left=overlap_start * 100, height=height,
                    color=get_mischfarbe(), alpha=1)

        y_pos += height # Abstand zum nächsten Balken
        participants_range += height

    ax.set_yticks(yticks)
    ax.tick_params(axis='y', length=10)
    ax.set_yticklabels([])
    ax.set_xlabel('Relative Time of Command Creation [\%]')
    percentage_values_for_axis = [0, 25, 50, 75, 100]
    ax.set_xticks(percentage_values_for_axis)
    ax.set_xticklabels([str(s) for s in percentage_values_for_axis], rotation=45)
    ax.set_ylabel(names["participants"], labelpad=35)
    ax.set_xlim(0, 100)
    ax.set_ylim(min(yticks), y_pos + height/2 - height)

    legend = get_legend(ax)
    save_my_figures(name= "verzahnung-sketch-voice", fig=fig, bbox_extra_artists=[legend])
    my_plt.show()




def get_legend(ax):
    mischfarbe = get_mischfarbe()

    patch_sketch = mpatches.Patch(color=global_colors["sketch"], label='sketch')
    patch_voice = mpatches.Patch(color=global_colors["voice"], label='voice')
    patch_overlap = mpatches.Patch(color=mischfarbe, label='voice+sketch')

    handles, labels = ax.get_legend_handles_labels()
    handles.extend([patch_sketch, patch_voice, patch_overlap])
    labels.extend(['Sketching', 'Vocalizing', 'Sketch+Voice'])

    return ax.legend(handles, labels, loc='upper left', ncol=3, bbox_to_anchor=(0.2978, 1.08),#0.2978, 1.16),
                     title="Active Process of:")


def run_combined_modalities():
    sketch_and_voice, sketch_and_voice, total_number_of_categoried_tasks, task_data_in_combined_modality = get_data_combined_modalities()
    print()
    print("sketch and voice simultaneosly used by:\t", sketch_and_voice.keys(), "=", len(sketch_and_voice.keys()),
          "participants")
    print("in", sum([len(i) for i in sketch_and_voice.values()]), "tasks of", total_number_of_categoried_tasks)

    task_data_in_combined_modality = sort(task_data_in_combined_modality)
    plot(task_data_in_combined_modality)


if __name__ == '__main__':
    run_combined_modalities()