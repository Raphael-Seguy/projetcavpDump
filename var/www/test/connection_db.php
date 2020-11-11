<?php

	function ConnectToDB($user,$host,$pass,$db){
		$host = $host;
		$db = $db;
		$user = $user;
		$pass=$pass;
	
		$dsn = "mysql:host=$host;dbname=$db";
		$dbh = null;

		try{
			$dbh = new PDO($dsn,$user,$pass);
		}catch(PDOException $e){
			die("Erreur ! : " . $e->getMessage());
		}
		return $dbh;
	}
?>
