$(document).ready(function(){

    $('.form_datetime').datetimepicker({
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: 1
    });

    $('#add_event_button').on('click', function(){
        var event_time = $('.event_time').val();
        var event_title = $('.event_title').val();
        var event_content = $('.event_content').val();
        var team_id = $(this).attr('value');
        console.log(event_time);
        $.ajax({
            type: "POST",
            url: "/add_event",
            data: {
                time: event_time,
                title: event_title,
                content: event_content,
                team_id: team_id
            }
        }).done(function(){
            console.log('ok');
        }).fail(function(msg){
            console.log('failed');
        })

    });

})
