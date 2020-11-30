#!/bin/bash

TARGET=/home/$1/image
DESTINATION=/home/$1/unziped_image/
inotifywait -m -e close_write --format "%f" $TARGET \
  | while read FILENAME
    do
      echo Detected $FILENAME - waiting, gunzipping and running script.
			mv "$TARGET/$FILENAME" "$DESTINATION/$FILENAME"
			gzip -d "$DESTINATION/$FILENAME"
      python /home/marcin_tomasz_stanislaw_gorczyca/Scripts/make_backup_and_create_image.py $1
    done
