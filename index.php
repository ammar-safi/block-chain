<?php



if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    
    if (isset($_POST["verify"]) && $_POST["verify"]) {
        $ex = 0;
        $res = 0;
       
        exec("py blockchain.py block_chain_check ", $ex, $re);
        $response = json_decode($ex[0], true);
        
        if ($response['status'] == 200) {
            $res = 1;
            $data = $response['data'];
            echo "Blockchain is valid!<br>";

        } else {
            echo "Error: " . $response['message'];
        }
    } else {   
        $ex = 0;
        $res = 0;
        $data = $_FILES["block"]["tmp_name"];
        exec("py blockchain.py block_chain_file " . $data . " 1", $ex, $re);
        $response = json_decode($ex[0], true);
        
        if ($response['status'] == 200) {
            $res = 1;
            $data = $response['data'];
            echo "Block added successfully!<br>";
            echo "Hash: " . $data['hash'] . "<br>";
            echo "Index: " . $data['index'] . "<br>";
            echo "File path: " . $data['file_path'] . "<br>";
            echo "Stored hash: " . $data['stored_hash'];
        } else {
            echo "Error: " . $response['message'];
        }
    }
    
}



?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form action="#" method="post" enctype="multipart/form-data">
        
        <input type="file" name="block" id="">
        <input type="submit" value="submit">
        
      
    </form>

    <form method="post">
        <input type="hidden" name="verify" value="1">
        <input type="submit" value="verify">
    </form>
    
</body>

</html>