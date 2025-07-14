#!/bin/bash

# move to source directory
cd /app/src

# run backup handler(in background)
python manage.py run-backup &  

# run django server
python manage.py runserver 0.0.0.0:8000

