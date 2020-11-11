<?php	
	require_once("connection_db.php");
	try{
		$dbh=ConnectToDB("spectator","localhost","Test","WebsiteDB");
		if(isset($_GET['request'])){
			if($_GET['request']==="UE"){
				$request=$dbh->prepare('SELECT ue.nom as "UE nom",ue.ects as "Ects",SUM(aa.heure) as "Nbre tot heures" FROM ue INNER JOIN aa ON ue.idUE=aa.idUE GROUP BY ue.idUE');
				if(!$request->execute()){
					echo "Error : fetching table ue inner join aa";
				}else{
					echo "<table>";
					while(($row = $request->fetch(PDO::FETCH_ASSOC))!=null){
						echo "<tr>";
						echo "<td>".$row["UE nom"]."</td>";
						echo "<td>".$row["Ects"]."</td>";
						echo "<td>".$row["Nbre tot heures"]."</td>";
						echo "</tr>";
					}
					echo "</table>";
				}
			}else{ 	echo "Hello ".$_GET['request'];	}
		}else{
			echo "Nothing to say";
		}
	}catch(Exception $e){
		echo "Error";
	}
?>
