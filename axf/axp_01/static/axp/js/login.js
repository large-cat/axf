$(function () {
    var button = $("#btn_login");
    var $name = $("#id_username");//获取输入框1的值
    var $pwd = $("#password");
    button.attr("disabled", true);

    //监测是否未输入用户名
    $name.on("input propertychange", function () {//监控输入框的变化
    if ($name.val().trim() === '' || $pwd.val().trim() === ''){
        button.attr("disabled", true);
    } else {
        button.attr("disabled", false);
    }
    });

    //监测是否未输入密码
    $pwd.on("input propertychange", function () {//监控输入框的变化
    if ($name.val().trim() === '' || $pwd.val().trim() === ''){
        button.attr("disabled", true);
    } else {
        button.attr("disabled", false);
    }
    });

});
