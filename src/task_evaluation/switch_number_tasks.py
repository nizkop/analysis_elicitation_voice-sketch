#
#
# from matplotlib.patches import Patch
#
# from src.plt_settings import my_plt
# from src.Task import tasks
# from src.participants import participants
# from src.color_codes import global_colors
# from src.get_descriptions import names
#
# collected_data = []
# for task_idx, task in enumerate(tasks):
#     if task.identifier.lower() not in ["c", "g"]:
#         median, schwankung = task.get_switch_median(participants)
#         collection = {
#             "switch_amount": median,
#             "schwankung": schwankung,
#             "id": task.identifier,
#             "group": task.get_group(),
#             "color": global_colors["group"+task.get_group() if task.get_group() else None ]
#         }
#         collected_data.append(collection)
#
# # data extraction:
# ids = [i["id"] for i in collected_data]
# switch_amounts = [i["switch_amount"] for i in collected_data]
# colors = [i["color"] for i in collected_data]
# groups = [i["group"] for i in collected_data]
# schwankungen =[i["schwankung"] for i in collected_data]
# # synchron sortieren nach switch_amounts:
# combined = list(zip(switch_amounts, ids, colors, groups, schwankungen))
# combined.sort(key=lambda x: (x[0], x[3]))
# switch_amounts, ids, colors, groups, schwankungen = zip(*combined)
# # plot:
# my_plt.bar(ids, switch_amounts, color=colors, yerr=schwankungen, capsize=5)
# ax = my_plt.gca()
# ax.yaxis.set_label_position("right")  # Y-Achsen-Beschriftung rechts
# ax.yaxis.tick_right()                  # Y-Ticklabels rechts
# my_plt.xlabel(names["taskid"])
# my_plt.ylabel("Median of Switch Number [ ]")
# my_plt.xticks(rotation=45)
# legend_elements = [Patch(facecolor=color, label=group.replace("group","")) for group, color in global_colors.items()
#                    if group is not None and "group" in group and group != "groupP"]
# my_plt.legend(handles=legend_elements, title=names["group"]+":")
# my_plt.ylim(bottom=0)
# my_plt.tight_layout()
# my_plt.savefig("switch_number_tasks.pdf", bbox_inches="tight")
# my_plt.show()
# my_plt.close()



from src.task_evaluation.median_watching_time_tasks import get_box_task

get_box_task("switch_amount", break_axis=True)


