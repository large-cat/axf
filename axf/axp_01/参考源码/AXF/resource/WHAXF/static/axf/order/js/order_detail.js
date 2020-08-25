$(function () {


    $("#alipay").click(function () {

    //    假装支付成功
    //    修改订单状态
        $.getJSON("/axf/alipay/", {"orderid": $(this).attr("orderid")}, function (data) {
            console.log(data);

            if (data["status"] == "200"){

                window.open('/axf/mine/', target="_self");
            }

        })

    })

})