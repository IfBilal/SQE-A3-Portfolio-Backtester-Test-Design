#!/bin/bash
# copy new session-2 screenshots into shots/ as s2_<N>.jpg
for f in /tmp/claude-chrome-screenshots-6VjOR5/*.jpg; do
  n=$(basename "$f" .jpg | sed 's/.*-//')
  [ -f "/home/bilaltahir/Desktop/SQE-A3/shots/s2_$n.jpg" ] || cp "$f" "/home/bilaltahir/Desktop/SQE-A3/shots/s2_$n.jpg"
done
ls /home/bilaltahir/Desktop/SQE-A3/shots | wc -l
