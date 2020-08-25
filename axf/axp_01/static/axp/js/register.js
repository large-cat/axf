$(function () {

    var btn_register = $("#btn_register");
    var $pwd1_input = $('#password1');
    var $pwd2_input = $('#password2');
    var user_input = $("#id_username");
    var vanity_msg = $('#pd_msg');

    btn_register.attr("disabled", true);

    //绑定输入改变事件
    $pwd1_input.change( function () {
        vanity_input()
    });

    $pwd2_input.on("input propertychange",function () {
        vanity_input()
    });

    user_input.change(function () {//监控输入框的变化
        vanity_input()
        var username = user_input.val().trim();
        if (username.length) {
            $.getJSON('/index/check_user/',{'username':username}, function (data){
            // console.log(data);
                var $username_ifo = $('#username_ifo')
            if (data['status'] === 902){
                $username_ifo.text('用户已存在').css('color','red');
            } else if (data['status'] === 200){
                $username_ifo.text('用户名可以使用').css('color','green');
            }
        })
        }
    });

    //定义输入验证函数
    function vanity_input(){
        var pwd1 = $pwd1_input.val().trim();
        var pwd2 = $pwd2_input.val().trim();
        var username = user_input.val().trim();
        if (username !== ''){
            if (pwd1 !== '' && pwd2 !==''){
                if (pwd2 === pwd1) {
                    vanity_msg.text('OK').css('color','green');
                    btn_register.attr("disabled", false);
                } else {
                    vanity_msg.text('两次密码输入不一致').css('color','red');
                    btn_register.attr("disabled", true);
                }
            }else {
                if (pwd1 ==='' && pwd2 === '') {
                    vanity_msg.text('密码不能为空').css('color','red');
                    btn_register.attr("disabled", true);
                } else {
                    vanity_msg.text('两次密码输入不一致').css('color','red');
                    btn_register.attr("disabled", true);
                }
            }
        } else {
            vanity_msg.text('用户名不能为空').css('color','red');
            btn_register.attr("disabled", true);
        }

    }
});
