#!/usr/bin/env bash
# Run badwordcheck in all subfolders of the current directory

BADWORDCHECK=~/Development/AI-tests/BadWordsChecker/badwordcheck
DICT_FILE="$(pwd)/badwords-it.txt"

for dir in */ ; do
  if [ -d "$dir" ]; then
    echo "Processing $dir with dict $DICT_FILE"
    "$BADWORDCHECK" --dict "$DICT_FILE" "$dir"
  fi
done
