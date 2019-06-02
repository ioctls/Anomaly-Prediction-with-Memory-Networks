<?php

$dbname = 'rubis';
$dbuser = 'root';
$dbpass = 'password';
$dbhost = 'localhost';

$link = mysqli_connect($dbhost, $dbuser, $dbpass) or die("Unable to Connect to '$dbhost'");
 echo "jjjj\n";
mysqli_select_db($link, $dbname) or die("Could not open the db '$dbname'");

$test_query = "SHOW TABLES FROM $dbname";
$result = mysqlQuery($link, $test_query);
$tblCnt = 0;

while($tbl = mysqli_fetch_array($result)) {
	  $tblCnt++;
}

if (!$tblCnt) {
	  echo "There are no tables<br />\n";
} else {
	  echo "There are $tblCnt tables<br />\n";
}
