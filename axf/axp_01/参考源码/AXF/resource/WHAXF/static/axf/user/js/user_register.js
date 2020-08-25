function check_input() {

    var username_color = $("#usernameInfo").find("span").css("color");

    console.log(username_color);
    // 红色 出现错误提示 ，没必要提交了
    if( username_color == "rgb(255, 0, 0)"){
        return false
    }

    var $password = $("#exampleInputPassword");

    var password =$password.val();

    var password_confirm = $("#exampleInputPasswordConfirm").val();

    if(password.length > 5){

        // return password === password_confirm;

        if (password === password_confirm){
            $password.val(md5(password));
            return true
        }else {
            return false
        }

    }else {
        return false
    }

}


$(function () {

    $("#exampleInputUsername").change(function () {

        var username = $(this).val();

        console.log(username);

        $.getJSON("/axf/checkuser/", {"username": username}, function (data) {

            console.log(data);

            if(data["status"] == "200"){
                $("#usernameInfo").html(data["msg"]);
            }else if(data["status"] == "901"){
                $("#usernameInfo").html(data["msg"]);
            }

        })

    })

})