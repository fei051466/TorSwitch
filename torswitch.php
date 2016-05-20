<?php
/**
 * Switch TOR to a new identity.
 **/
set_time_limit(0);
function tor_new_identity($tor_ip='127.0.0.1', $control_port='9151', $auth_code=''){
    $fp = fsockopen($tor_ip, $control_port, $errno, $errstr, 50);
    if (!$fp) return false; //can't connect to the control port
    
    fputs($fp, "AUTHENTICATE $auth_code\r\n");
    $response = fread($fp, 1024);
    list($code, $text) = explode(' ', $response, 2);
    if ($code != '250') return false; //authentication failed
    
    //send the request to for new identity
    fputs($fp, "signal NEWNYM\r\n");
    $response = fread($fp, 1024);
    list($code, $text) = explode(' ', $response, 2);
    if ($code != '250') return false; //signal failed
    
    fclose($fp);
    return true;
}
 
/**
 * Load the TOR's "magic cookie" from a file and encode it in hexadecimal.
 **/
function tor_get_cookie($filename){
    $cookie = file_get_contents($filename);
    //convert the cookie to hexadecimal
    $hex = '';
    for ($i=0;$i<strlen($cookie);$i++){
        $h = dechex(ord($cookie[$i]));
        $hex .= str_pad($h, 2, '0', STR_PAD_LEFT);
    }
    return strtoupper($hex);
}


$cookie = tor_get_cookie('C:\Users\admin\Desktop\Tor Browser\Browser\TorBrowser\Data\Tor\control_auth_cookie');
if (tor_new_identity('127.0.0.1', '9151', $cookie))
    echo "Identity switched!";
else
    echo "Identity switched failed! Maybe the tor.exe not run……";

?>