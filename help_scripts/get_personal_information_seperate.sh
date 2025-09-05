#!/bin/bash

SOURCE_BASE="../Participant_data"
TARGET_DIR="./videos/"
mkdir -p "$TARGET_DIR"

for participant_dir in "$SOURCE_BASE"/Participant_*; do
  [ -d "$participant_dir" ] || continue
  participant_name=$(basename "$participant_dir")

  # Finde alle passenden MP4-Dateien im Teilnehmerverzeichnis
  mp4_files=("$participant_dir"/Screen_Recording*.mp4)

  # Wenn genau eine MP4-Datei vorhanden ist
  if [ "${#mp4_files[@]}" -eq 1 ] && [ -f "${mp4_files[0]}" ]; then
    src_file="${mp4_files[0]}"
    base_file=$(basename "$src_file")
    target_file="${TARGET_DIR}Screen_Recording_${participant_name}.mp4"

    mv "$src_file" "$target_file"
    echo "Kopiert: $src_file -> $target_file"
  else
    echo "Übersprungen: $participant_name (gefunden: ${#mp4_files[@]} passende MP4-Dateien)"
  fi
done
