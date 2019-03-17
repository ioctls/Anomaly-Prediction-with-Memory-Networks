#!/bin/bash
option="$1"
if [ "$#" -ne 1 ]; then
	echo "[USAGE] ./shetup.sh [mode]"
	exit 1
fi

if [ "$option" -eq 0 ]; then
	echo "Setting up env"
	sudo apt-get update
	echo y | sudo apt-get install python3-pip
	echo y | sudo -H pip3 install virtualenv
	#put everything in a virtualenv
	virtualenv -p python3 anomaly
	source anomaly/bin/activate
	echo y | sudo -H pip3 install tensorflow==1.5
	echo Y | sudo -H pip3 install numpy scipy pandas matplotlib
	echo y | sudo -H pip3 install ipython[all]
	echo y | sudo -H pip3 install jupyter keras
	echo y | sudo apt-get install ipython3
	sudo -H pip3 install -U scikit-learn
	sudo ipython3 kernel install
else
	source anomaly/bin/activate
fi
jupyter notebook
exit 1
