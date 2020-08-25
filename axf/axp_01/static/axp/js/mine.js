$(function () {

    $('#pending_payment').click(function () {
        location.href = '/index/order_inquiry/' + '?method=pending_payment'
    })

});