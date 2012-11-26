<html>
<body style='font-size:30pt'>
<script src="/bbs/js/jquery-1.8.0.min.js"></script>
<script>
function test(arg){
	var url = "delete.php?test="+arg;
	document.getElementById('del').src=url;
}

</script>
<iframe width=0 height=0 name=del id=del></iframe>
<?
$perPage = 200;
$d = dir(".");

$start = $_GET['page'] * $perPage;

echo "<a href=index.php?page=".($_GET['page']-1).">PREV</a>";
echo "<a href=index.php?page=".($_GET['page']+1).">NEXT</a><br>";

$count = 0;
$files = array();

while($entry=$d->read()) {
    if( $entry != '.' && $entry != '..' && $entry != 'index.php' ){
	$files[] = $entry;
    }
}
$d->close();
sort($files);
for($i=$start; $i< $start+$perPage; $i++){
	echo "<img src=".$files[$i]." ondblclick=\"test('".$files[$i]."')\" border=1><br>\n";
}

echo "<a href=index.php?page=".($_GET['page']-1).">PREV</a>";
echo "<a href=index.php?page=".($_GET['page']+1).">NEXT</a><br>";
?>
</body>
</html>
