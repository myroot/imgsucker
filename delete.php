<?
header("Cache-Control: no-cache, must-revalidate");
unlink($_GET['test']);
?>
<script>
//alert('<?=$_GET['test']?>');
</script>
