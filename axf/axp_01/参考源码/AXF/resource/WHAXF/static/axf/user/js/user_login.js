function password_hash() {

    var $password = $("#exampleInputPassword");

    var password = $password.val();

    $password.val(md5(password));

    return true

}