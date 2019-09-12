<?php
//header("Content-Type: application/json", true);

// Read the posted data
$stringData = $_POST['data'];
$myPostData = json_decode($stringData,true);

// Read the subject name and block number
$subject = $myPostData["subject"];
$block = $myPostData["blocknumber"];
//$outputdir = 'env_data/'; 
// Save the results in a designated file 
$datafile = '_result.json';
$date = date("m-d-Y");
echo $datafile;
$fh = fopen($subject.'_block_'.$block.'_'.$date.$datafile, 'w') or die("can't open file");
fwrite($fh, $stringData);
fclose($fh);

?>


