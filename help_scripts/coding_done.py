from src.Tasks.Task import tasks
from src.TaskJsonKind import TaskJsonKind
from src.participants import participants


for t in tasks:
    if t.identifier in ["C", "G"]:
        continue
    for p in participants:
        if not t.coded(p) and not t.skipped(p) and not t.missunderstood(p):
            print("Task", t.identifier, "from", p.id ,"is missing")




# Check Coding Plausability:
for p in participants:
    print("\n")
    for t in tasks:
        if t.coded(p) and t.get_group() != "P":
            coded = t.get_coding(p=p, infokind=TaskJsonKind.CODES)
            cat = t.get_category(p, infokind=TaskJsonKind.CODES)
            coded2 = t.get_coding(p=p, infokind=TaskJsonKind.CODESconsistency)
            cat2 = t.get_category(p, infokind=TaskJsonKind.CODESconsistency)
            if not t.missunderstood(p) and not t.skipped(p):
                if coded is None or cat is None or len(coded) == 0 or len(cat) == 0:
                    print(f"Participant {p.id} CODING MISSING for task {t.identifier}")
                elif coded2 is None or len(coded2) == 0 or len(cat2) == 0:
                    print(f"Participant {p.id} CODING CHECK MISSING for task {t.identifier}")
                else:
                    if coded == coded2 and cat == cat2:
                        print(f"\033[32mParticipant {p.id} fully coded for task {t.identifier}\033[0m")
                    elif coded != coded2 and cat != cat2:
                        print(f"\033[31mParticipant {p.id} differently coded for task {t.identifier}\033[0m")
                    else:
                        keys = list(set([key for i in coded for key in i.keys()]))
                        keys2 = list(set([key for i in coded2 for key in i.keys()]))
                        if len(coded) != len(coded2) or len(keys) != len(keys2) or len(coded[0]) != len(coded2[0]):
                            print("! Participant", p.id, "task", t.identifier, "uses different coding metrices")
                        else:
                            print("! Participant", p.id, "strangely coded for task", t.identifier)#, ":", coded==coded2, cat==cat2, ["\t".join(difflib.ndiff(cat, cat2))])
                            print("\t", coded, cat)
                            print("\t", coded2, cat2)
                            print()
        elif t.get_group() != "P" and not t.missunderstood(p):
            print(f"Participant {p.id} CODING MISSING for task {t.identifier}")

