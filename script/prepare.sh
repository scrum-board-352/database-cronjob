#!/bin/sh

if [ ! -x "~/database-cronjob"]; then
  echo repo not exit.
  git clone https://github.com/scrum-board-352/database-cronjob.git
else
  echo repo exit.
  git pull
fi

cd ~/database-cronjob
pip install -r requirements.txt