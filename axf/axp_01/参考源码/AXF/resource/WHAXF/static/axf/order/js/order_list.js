$(function () {

    $(".order_item").click(function () {

        var order_id = $(this).attr("orderid");

        window.open('/axf/orderdetail/?order_id=' + order_id, target="_self");

    })


})