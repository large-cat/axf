$(function () {

    $("#all_type").click(function () {

        console.log("全部类型");

        $("#all_type_container").show();

        $("#sort_rule_container").hide();

        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        $("#sort_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })


    $("#all_type_container").click(function () {

        $(this).hide();

        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#sort_rule").click(function () {

        console.log("排序规则");

        $("#sort_rule_container").show();

        $("#all_type_container").hide();

        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#sort_rule_container").click(function () {

        $(this).hide();

        $("#sort_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");


    })

//    添加到购物车
    $(".addShopping").click(function () {

        console.log("添加到购物车");

        var $add = $(this);

        var goodsid = $add.attr("goodsid");

        // console.log($(this).prop("goodsid"));

        // 参数可以直接进行拼接
        // 也可以使用第二个参数传递字典的形式进行参数设置  更推荐使用第二种
        $.getJSON("/axf/addtocart/",{"goodsid": goodsid} ,function (data) {
            console.log(data);

            if (data["status"] == "902"){
                window.open('/axf/userlogin/', target="_self");
            }else if (data['status'] == "201"){
                console.log("改变数量");
                $add.prev("span").html(data["cart_goods_num"]);
            }

        //    ajax请求回来之后的操作 写在这

        })

        // ajax 并行操作写在这
        // console.log("哈哈");

    })


})