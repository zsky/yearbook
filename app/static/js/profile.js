$(document).ready(function(){

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
