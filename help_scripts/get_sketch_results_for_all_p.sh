#!/bin/bash

task="9"  # Aufgabe auswählen

SOURCE_BASE="../Participant_data"
TARGET_DIR="./evaluation_task_${task}/"
mkdir -p "$TARGET_DIR"
FILENAME_PATTERN="T*_Task_${task}_sheet1.png"

for data_dir in "$SOURCE_BASE"/Participant_*/DATA; do
  [ -d "$data_dir" ] || continue
  participant_name=$(basename "$(dirname "$data_dir")")
  for src_file in "$data_dir"/$FILENAME_PATTERN; do
    [ -f "$src_file" ] || continue
    base_file=$(basename "$src_file")
    target_file="$TARGET_DIR${participant_name}_Task_${task}_sheet1.png"

    cp "$src_file" "$target_file"
#    xdg-open "$data_dir/Task_${task}.json"
    echo "Kopiert: $src_file -> $target_file"
  done
done