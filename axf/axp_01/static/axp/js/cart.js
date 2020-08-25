$(function () {
    //分类筛选折叠
    var all_types = $('#all_types'), all_sorts = $('#all_sorts');
    var all_type_span = all_types.find('span');
    var all_sorts_span =all_sorts.find('span');
    var $all_types_container = $('#topsection');
    var $all_sorts_container = $('#sort_list');

    all_types.click(function () {
        // console.log("全部分类");
        if ($all_types_container.is(':visible')) {
            $all_types_container.hide();
            all_type_span.removeClass('glyphicon-chevron-up');
            all_type_span.addClass('glyphicon-chevron-down');
            // console.log(name)
        } else {
            //如果另一个标签正在显示，则关闭它
            if ($all_sorts_container.is(':visible')) {
                $all_sorts_container.hide();
                // console.log(name)
                all_sorts_span.removeClass('glyphicon-chevron-up');
                all_sorts_span.addClass('glyphicon-chevron-down');
            }

            $all_types_container.show();
            all_type_span.removeClass('glyphicon-chevron-down');
            all_type_span.addClass('glyphicon-chevron-up');
            // console.log(name)
        }
        // console.log(name);
    });

    $all_types_container.click(function () {
        $all_types_container.hide();
    });


    all_sorts.click(function () {
        // console.log("全部分类");
        if ($all_sorts_container.is(':visible')) {
            $all_sorts_container.hide();
            // console.log(name)
            all_sorts_span.removeClass('glyphicon-chevron-up');
            all_sorts_span.addClass('glyphicon-chevron-down');
        } else {
            $all_sorts_container.show();
            // console.log(name);
            all_sorts_span.removeClass('glyphicon-chevron-down');
            all_sorts_span.addClass('glyphicon-chevron-up');

            //如果另一个标签正在显示，则关闭它
            if ($all_types_container.is(':visible')) {
                $all_types_container.hide();
                all_type_span.removeClass('glyphicon-chevron-up');
                all_type_span.addClass('glyphicon-chevron-down');
            }
        }
        // console.log(name);
    });

    $all_sorts_container.click(function () {
        $all_sorts_container.hide();
    });
//    购物车修改
//    增加购物车内数量
//     console.log('loading');
        var $good_button = $(".button_up");
        $good_button.click(function () {
            var good_id = this.id.replace('good_','');
            var good_num = $('#num_' + good_id);
            var  new_num = good_num.val() - -1;
            good_num.val(new_num);

            update_good_num(good_id, new_num);
        });
        //减少购物车内数量
        var $good_button = $(".button_down");
        $good_button.click(function () {
            var good_id = this.id.replace('good_','');
            var good_num = $('#num_' + good_id);
            if (good_num.val() == 0 || good_num.val()<0) {
                var new_num = 0;
            }else {
                var  new_num = good_num.val() - 1;
            }
            good_num.val(new_num);
            // console.log(good_num.val());

            update_good_num(good_id, new_num);
        });

        // console.log('load_end')

    //设置ajax crsf_token
    jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


    //手动输入数量
    $('.good_num').change(function (){

        var good_id = this.id.replace('num_','');

        // console.log(good_id);

        // console.log(this);

        var value = this.value;

        update_good_num(good_id, value);

    });


    //更新修改
    function update_good_num(good_id, value) {

        var source_data = {operation:'update', data:{}};

        source_data['data'][good_id] = value;

        // console.log(source_data);
        send_data(source_data);

    }
    //全选或全不选
    $('#chose_all_button').click(function () {
        var all_selected = 0;
        var $chekboxs = $('.checkbox');

        for (var i=0;i<$chekboxs.not("input:checked").length;i++){
            // if (!$chekboxs[i].is(':checked')){
            //     all_selected++;
            // }
            all_selected++;
        }

        if (all_selected){
            // console.log('全选');
            $chekboxs.prop("checked",true);
        } else {
            // console.log('全不选');
            $chekboxs.prop("checked",false);
        }
    });

//    delete动作
    $('#delete_button').click(function () {
        var delete_goods_list = $('input:checkbox:checked');

        if (delete_goods_list){

        }

        var delete_id_list = [];

        for (var i=0;i<delete_goods_list.length;i++){
            delete_id_list.push(delete_goods_list[i].value);
        }

        // console.log(delete_id_list);

        delete_goods(delete_id_list);

    });

//    从购物车删除所选商品
    function delete_goods(good_list) {

        var data = {operation:'delete', data:good_list};
        send_data(data);
    }

    //结算
    $('#pay_button').click(function () {
        var delete_goods_list = $('input:checkbox:checked');

        var data_source = {operation:'pay', data:[]};

        for(var i=0;i<delete_goods_list.length;i++){

            var record_id = delete_goods_list[i].value;
            var good_num = $('#num_' + record_id).val();
            // console.log(good_num, $('#num_' + record_id));

            data_source['data'].push([record_id,good_num])

        }

        var data = JSON.stringify(data_source);

        $.ajax({
            type: "POST",
            url: "/index/pay/",
            data: data,
            dataType: "json",
            success:function (data) {
                var order_num = data['order_num'];
                location.href = '/index/pay/'+ '?order_num=' + order_num
            }
        })

    });

    //向服务器发送数据
    function send_data(source_data) {

        var data = JSON.stringify(source_data);

        $.post('/index/order_deal/',data,function (data) {
            console.log(data['msg']);

            location.reload();

        },
            "json",
            )

    }

});