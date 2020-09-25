#!/bin/sh

if [ ! -x "~/database-cronjob"]; then
  echo repo not exit.
  git clone https://github.com/scrum-board-352/database-cronjob.git
  cd ~/database-cronjob/script
  sh prepare.sh
else
  echo repo exit.
  git pull
  cd ~/database-cronjob/script
  sh prepare.sh
fi