$(document).ready(function(){

    $('.form_date').datetimepicker({
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0,
    });

/*    $('#add_event_button').on('click', function(){
        var event_time = $('.event_time').val();
        var event_title = $('.event_title').val();
        var event_content = $('.event_content').val();
        var team_id = $(this).attr('value');
        var event_photo = $('.event_photo').val();
        console.log(event_photo);
        $.ajax({
            type: "POST",
            url: "/add_event",
            data: {
                time: event_time,
                title: event_title,
                content: event_content,
                team_id: team_id,
                photo: event_photo
            }
        }).done(function(){
            console.log('ok');
        }).fail(function(msg){
            console.log('failed');
        })

    });  */

})
