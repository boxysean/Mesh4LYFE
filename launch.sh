#!/bin/ash

if [[ -e PID ]]; then
	PID=$(cat PID)
	if [[ ${#PID} -gt 0 ]]; then
		kill $PID
	fi
fi

python /root/server.py &

echo $! > PID

