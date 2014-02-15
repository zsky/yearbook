$(document).ready(function(){

    $(".load_comments").on("click", function(){
        var event_id = $(this).attr('value');

        $.ajax({
            type: "POST",
            url: "/load_comments",
            data: { e_id: event_id }
        }).done(function(comments){
            $("#event-" + event_id).html(comments);
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".add_comment").on("click", function(){
        var event_id = $(this).attr('value');
        var c_body = $(this).parent().find('.c_body').val();
        console.log(c_body);

        $.ajax({
            type: "POST",
            url: "/add_comment",
            data: { e_id: event_id,
                c_body: c_body }
        }).done(function(comments){
            $("#event-" + event_id).prepend(comments);
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".send_message").on("click", function(){
        var t_id = $(this).attr('value');
        var m_body = $(this).parent().find('.m_body').val();

        $.ajax({
            type: "POST",
            url: "/send_message",
            data: { m_type: 'join_team',
                t_id: t_id,
                m_body: m_body }
        }).done(function(res){
            console.log(res);
        }).fail(function(){
            console.log('fail');
        });
    });

})
