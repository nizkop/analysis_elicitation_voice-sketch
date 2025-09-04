

# TODO change when changing participant IDs!!!

# aus Wertung entfernt / missunderstood:
missunderstood = {
    # p_id : [task_ids]
}

# skipped tasks:
skipped = {
    # p_id : [task_ids]
    "0": [20],
}

time_data_error = {
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
