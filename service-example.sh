#!/bin/bash
 
ENV=production
BASE=/home/rita/${ENV}
 
cd ${BASE}
 
# Activate the virtual environment.
source ${BASE}/bin/activate
 
function shard() {
	start-stop-daemon
	paster serve etc/shard-${2}.ini --pid-file var/run/${ENV}-${2}.pid --log-file var/log/${ENV}-${2}.log --daemon "${1}"
}
 
function start() {
	for i in 1 2 3; do
		shard start $i
	done
}
 
function stop() {
	for i in 1 2 3; do
		shard stop $i
	done
}
 
case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	*)
		echo "Usage: $0 {start|stop|restart}"
		exit 1
esac
