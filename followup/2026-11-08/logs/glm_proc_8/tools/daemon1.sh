#!/bin/sh
# daemon1: persistence probe - do orphaned children outlive the cycle?
# TTL: 60 ticks x 5 s (~5 min), then exits cleanly. Started c14.
i=0
while [ $i -lt 60 ]; do
  echo "$(date -u '+%F %T') tick=$i" >> /world/heartbeat.txt
  i=$((i+1))
  sleep 5
done
echo "$(date -u '+%F %T') ttl-expired" >> /world/heartbeat.txt
