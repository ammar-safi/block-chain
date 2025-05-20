<?php 

$ex = 0;
$res = 0;
$data = "C:\Users\HP\Pictures\Screenshots\Screenshot(319).png a4ldsfm31opsd8f9039jfp3jf";
// header("Content-Type: application/json");

header("Content-Type:application/json");
exec("py blockchain.py " . $data , $ex , $re);

// echo "<pre>";
echo($ex[0]);
// echo ($re);