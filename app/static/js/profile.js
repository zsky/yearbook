$(document).ready(function(){


    function push_message(){

        $.ajax({
            type: "POST",
            url: "/push_message",
            data: { time: '90'}
        }).done(function(res){
            $('#show_messages').html(res);
            push_message();
        }).fail(function(){
            console.log('fail');
        });
    };

    push_message();


    $(".accept_message").on("click", function(){
        var message_div = $(this).parent();
        var message_id = message_div.attr("id");

        $.ajax({
            type: "POST",
            url: "/deal_message",
            data: { m_id: message_id, command: "accept" }
        }).done(function(res){
            console.log(res);
            message_div.hide();
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".reject_message").on("click", function(){
        var message_div = $(this).parent();
        var message_id = message_div.attr("id");

        $.ajax({
            type: "POST",
            url: "/deal_message",
            data: { m_id: message_id, command: "reject" }
        }).done(function(res){
            console.log(res);
            message_div.hide();
        }).fail(function(){
            console.log('fail');
        });
    });

})
