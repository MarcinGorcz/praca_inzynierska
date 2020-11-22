#!/bin/bash

TARGET=/home/$1/
PROCESSED=/home/$1/
inotifywait -m -e create -e moved_to --format "%f" $TARGET \
	| inotifywait -m -e close_write --format "%f" $TARGET \
        	| while read FILENAME
                	do
                	        echo Detected $FILENAME, unzipping and running script
				gzip -d "$TARGET/$FILENAME"
                	        python /home/marcin_tomasz_stanislaw_gorczyca/Scripts/watcher.py
                	        #python /home/marcin_tomasz_stanislaw_gorczyca/Scripts/make_backup_and_create_image.py $1
                	done
