url1="http://gwa.ewi.tudelft.nl/fileadmin/pds/trace-archives/grid-workloads-archive/datasets/gwa-t-12/fastStorage.zip"
url2="https://www.google.com/url?q=http://clusterdata-us.oss-us-west-1.aliyuncs.com/trace_201708.tgz&sa=D&ust=1552860435273000&usg=AFQjCNGbULIEzisR1qX_Q_E9TeSC1ddBPA"
url3="http://weixin.qq.com/r/dilgeAHE5lyZrUUb93xk"

wget=/usr/bin/wget
option=$1

if [ "$#" -ne 1 ]; then
        echo "[USAGE] ./dataset.sh [count]"
        exit 1
fi

if [ "$option" -eq 3 ]; then
	$wget "$url1"
	$wget "$url2"
	$wget "$url3"
elif [ "$option" -eq 2 ]; then
	$wget "$url1"
	$wget "$url2"
else
	$wget "$url1"
fi
unzip fastStorage.zip -d fastStorage
exit 1

