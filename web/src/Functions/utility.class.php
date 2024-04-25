<?php

class UtilityClass
{
    public function sanitizeParam($param) {
        $param = strip_tags(htmlspecialchars(trim($param)));
        return $param;
    }

    public function addNotification($title, $text, $type) {
        ?><script>addNotification("<?=$title;?>", "<?=$text;?>", "<?=$type;?>");</script><?
    }

    public function addJavaScript($param) {
        ?><script><?=$param;?></script><?
    }

    public function addCSS($param) {
        ?><style><?=$param;?></style><?
    }

    public function changeLocationViaHTML($time, $link) {
        ?>
        <script>
        setTimeout(function() {
          window.location.href = "<?=$link;?>";
        }, <?=$time;?>);
        </script>
        <meta http-equiv="refresh" content="<?=$time;?>;URL=<?=$link;?>" />
        <?
    }

    public function checkSessions($permissions, $database, $uuid = null) {

        if($permissions == "defaultAccess") {
            if(!empty($_SESSION['id'])) {
                exit($this->changeLocationViaHTML('0', './dashboard'));
            }
        }

        if($permissions == "dashboardAccess") {
            if(empty($_SESSION['id'])) {
                exit($this->changeLocationViaHTML('0', './logout'));
            }

            $databaseCallback = $database->get("gb_users", "login", ["id" => $this->id()]);

            if(empty($databaseCallback)) {
                exit;
            }
        }

        if($permissions == "adminAccess") {

            if($this->getUsersAccessType() == "admin") {
                return;
            }

            exit($this->changeLocationViaHTML('0', './sessions'));

        }

    }

    public function id() {
        return $_SESSION['id'];
    }

    public function getUsersAccessType() {
        return $_SESSION["role"];
    }

    public function getCurrentDateTime() {
        return date('d.m.Y H:i:s');
    }

    public function getCurrentTimeStamp() {
        return time();
    }

    public function getFullServerUrl() {
        $connectionType = 'http';
        if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') {
            $connectionType = 'https';
        }

        $serverName = $_SERVER['SERVER_NAME'];

        $port = $_SERVER['SERVER_PORT'];
        $portPart = '';
        if (($connectionType === 'http' && $port != 80) || ($connectionType === 'https' && $port != 443)) {
            $portPart = ':' . $port;
        }

        return $connectionType . '://' . $serverName . $portPart;
    }

}