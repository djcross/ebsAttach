#!/usr/bin/env bash

# Mount a volume as a postfix spool directory

vol='/dev/xvdg'

mount_stat=$(mount | grep postfix | wc -l)

if [ $mount_stat -eq 0 ]; then
  echo "Mounting postfix spool"
  /etc/init.d/postfix stop
  if [ ! -d /var/spool/postfix ]; then
    mkdir /var/spool/postfix
  fi
  mount $vol /var/spool/postfix
  /etc/init.d/postfix start
  exit 0
elif [ $mount_stat -eq 1 ]; then
  echo "Postfix spool already mounted"
  exit 0
else
  echo "Uh-oh. Something is wrong with mounting the postfix spool"
  exit 1
fi
