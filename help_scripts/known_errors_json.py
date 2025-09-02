

# TODO change when changing participant IDs!!!

# aus Wertung entfernt / missunderstood:
missunderstood = {
    # p_id : [task_ids]
    "023": [6],
    "018": [13,10],
    "017": [3],
    "031": [4],
    "032": ["E", 3, 4],
    "009": ["E"],
    "010": [3],
    "014": [20],
    "103": [20],# solved differently
    "104": [18],
    "107": [18]
}

# skipped tasks:
skipped = {
    # p_id : [task_ids]
    "000": [18],
    "001": [18],
    "031": [2,18,20],
    "032": [6],
    "010": [10, "E"],
    "009": [4],
    "020": [18],
}

time_data_error = {
    "104": ["4", "8", "17"],
    "111": ["4"]
}


known_errors_json = []

for p_id, task_ids in missunderstood.items():
    for task_id in task_ids:
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/DATA/Task_{task_id}.json")
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/CODES/coding_task_{task_id}.json")
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/DATA/questionnaire_task_{task_id}.json")

for p_id, task_ids in skipped.items():
    for task_id in task_ids:
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/DATA/Task_{task_id}.json")
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/DATA/questionnaire_task_{task_id}.json")
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/CODES/coding_task_{task_id}.json")
        known_errors_json.append(f"./Participant_data/Participant_{p_id}/CODES_duplicate/coding_task_{task_id}.json")
