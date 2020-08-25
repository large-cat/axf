$(function () {

    $(".confirm").click(function () {

        var $confirm = $(this);

        // 查找父级元素
        var cartid = $confirm.parents("div").attr("cartid");

        console.log(cartid);

        $.getJSON("/axf/changecartstatus/", {"cartid": cartid}, function (data) {
            console.log(data);

            if(data["status"] == "200"){
                if(data["is_select"]){
                    $confirm.find("span").find("span").html("√");
                //    全选按钮可能变成选中，  前置条件 全选状态是未选中
                    if(data["all_select"]){
                        $(".all_select span span").html("√");
                    }
                }else{
                    $confirm.find("span").find("span").html("");
                // 全选按钮需要变成未选中
                    $(".all_select span span").html("");
                }
                $("#total_price").html(data["total_price"]);
            }

        })

    })


    $(".all_select").click(function () {

        var select_list = [];
        var un_select_list = [];

        $(".menuList").each(function () {

            var $menuList = $(this);

            var cartid = $menuList.attr("cartid");

            var content = $menuList.find(".confirm span span").html();

            // trim  去掉内容两端的空格
            if(content.trim().length){
                select_list.push(cartid);
            }else{
                un_select_list.push(cartid);
            }

        })

        console.log(select_list);

        console.log(un_select_list);

        if(un_select_list.length){
        //    未选中的发送给服务器
            $.getJSON("/axf/changecartliststatus/", {"action": "select", "cartlist": un_select_list.join("#")}, function (data) {
                console.log(data);

                if(data["status"] == "200"){
                    $(".confirm span span").html("√");
                    $(".all_select span span").html("√");
                    $("#total_price").html(data["total_price"]);
                }

            })
        }else{
        //    选中的发送给服务器
            $.getJSON("/axf/changecartliststatus/", {"action": "unselect", "cartlist": select_list.join("#")}, function (data) {
                console.log(data);
                if (data["status"] == "200"){
                    $(".confirm span span").html("");
                    $(".all_select span span").html("");
                    $("#total_price").html(data["total_price"]);
                }
            })
        }



    })


    //   sublime   atom   notepade++ ue   ed

    $(".subShopping").click(function () {

        var $subShopping = $(this);

        var cartid = $subShopping.parents(".menuList").attr("cartid");

        console.log(cartid);

        $.getJSON("/axf/subtocart/", {"cartid": cartid}, function (data) {
            console.log(data);

            if(data["status"] == "200"){

                if(data["c_goods_num"] > 0){

                    $subShopping.next("span").html(data["c_goods_num"]);
                }else{
                    $subShopping.parents(".menuList").remove();
                }

                $("#total_price").html(data["total_price"]);

            }

        })

    })


    $("#gen_order").click(function () {

        var selects = [];


        $(".menuList ").each(function () {

            var $menuList = $(this);

            var cartid = $menuList.attr("cartid");

            // console.log($menuList.find(".confirm span span").html());

            if($menuList.find(".confirm span span").html().trim().length){
                selects.push(cartid);
            }

        })

        console.log(selects);

        if (selects.length){
            $.getJSON("/axf/makeorder/",{"cartlist": selects.join("#")},function (data) {

                console.log(data);
                
                if (data["status"] == "200"){
                    
                    window.open("/axf/orderdetail/?order_id=" + data["orderid"], target="_self");
                    
                }

            })
        }else{
            alert("请选择商品再下单");
        }

    })




})