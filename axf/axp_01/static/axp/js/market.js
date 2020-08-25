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

//添加购物车功能
    $('.good_num').val('0');
//    增肌添加数量
    console.log('loading');
        var $good_button = $(".button_up");
        $good_button.click(function () {
            var good_id = '#num_' + this.id.replace('good_','');
            var good_num = $(good_id);
            var  new_num = good_num.val() - -1;
            good_num.val(new_num);
        });
        //减少添加数量
        var $good_button = $(".button_down");
        $good_button.click(function () {
            var good_id = '#num_' + this.id.replace('good_','');
            var good_num = $(good_id);
            if (good_num.val() == 0 || good_num.val()<0) {
                var new_num = 0;
            }else {
                var  new_num = good_num.val() - 1;
            }
            good_num.val(new_num);
            // console.log(good_num.val());
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


//        提交到购物车
    $('#cart_button').click(function () {
        var msg = $('#ajax_msg_text');
        msg.text('正在加入购物车');
        msg.show();
        // console.log(msg.text(),msg.is(':visible'));
        var $goods_num = $('.good_num');
        // console.log($goods_num);
        var source_data = {operation:'add', data:{}};
        for (var i=0;i<$goods_num.length;i++){
            var num = $goods_num[i].value;
            var id = $goods_num[i].id.replace('num_','');
            source_data['data'][id] = num
        }
        // console.log(source_data);
        var data = JSON.stringify(source_data);
        $.post('/index/order_deal/',data,function (data) {
            var timeoutflag = null;
            // console.log(data['msg']);
            $('.good_num').val('0');
            msg.text(data['msg']);
            msg.show();
            if(timeoutflag != null){
                clearTimeout(timeoutflag);
            }
            timeoutflag = setTimeout(function () {
                msg.hide();
            }, 3000);
            // console.log(msg)
        },
            "json",
            )
    });

//        清除数量
    $('#clear_button').click(function () {
        $('.good_num').val('0');
    })
});