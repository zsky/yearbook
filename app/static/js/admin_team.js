$(document).ready(function(){
    var div_add_event = $(".add_event_div");
    var div_add_category = $(".add_category_div");
    var div_manage_event = $(".manage_events_div");
    var div_manage_member = $(".manage_member_div");
    
    $(document).ready(function(){
        div_add_event.show();
        div_add_category.hide();
        div_manage_event.hide();
        div_manage_member.hide();
    })
    $("#btn_add_event").click(function(){
        div_add_event.show();
        div_add_category.hide();
        div_manage_event.hide();
        div_manage_member.hide();
    });
    $("#btn_add_category").on("click", function(){
        div_add_event.hide();
        div_add_category.show();
        div_manage_event.hide();
        div_manage_member.hide();
        
    });
    $("#btn_manage_event").on("click", function(){
        div_add_event.hide();
        div_add_category.hide();
        div_manage_event.show();
        div_manage_member.hide();
        
    });
    $("#btn_manage_member").on("click", function(){
        div_add_event.hide();
        div_add_category.hide();
        div_manage_event.hide();
        div_manage_member.show();
        
    });
    

    $('.form_date').datetimepicker({
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0,
    });

    $(".show_members").on("click", function(){
        var t_id = $(this).attr('value');

        $.ajax({
            type: "POST",
            url: "/show_members",
            data: { t_id: t_id }
        }).done(function(members){
            $("#team_members").html(members);
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".search_user").on("click", function(){
        var search_name = $("#search_username").val();
        console.log(search_name);

        $.ajax({
            type: "POST",
            url: "/search_user",
            data: { search_name: search_name }
        }).done(function(user_info){
                $("#search_user_result").html(user_info);
        }).fail(function(){
            console.log('fail');
        });
    });

    $("#search_user_result").on("click", ".invite_user", function(){
        console.log('hehe');
        var invite_id = $(this).attr('value');
        var team_id = $("#search_user_result").attr('value');

        console.log(invite_id);

        $.ajax({
            type: "POST",
            url: "/send_message",
            data: { m_type: 'invite', 
                t_id: team_id, 
                to_id: invite_id
            }
        }).done(function(user_info){
                $("#search_user_result").html(user_info);
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".del_event").on("click", function(){
        var event_id = $(this).attr('value');
        var event_div = $("#e-" + event_id);

        $.ajax({
            type: "POST",
            url: "/del_events",
            data: { 
                events: event_id 
            }
        }).done(function(res){
            event_div.remove();
        }).fail(function(){
            console.log('fail');
        });
    });

    $(".del_selected_events").on("click", function(){
        var events_array = [];
        $("input[name='select_events']:checked").each(function(){
            events_array.push($(this).val());
        });
        var events_string = events_array.join(",");
        console.log(events_string);

        $.ajax({
            type: "POST",
            url: "/del_events",
            data: { 
                events: events_string 
            }
        }).done(function(res){
            var event_div;
            for(var i=0; i<events_array.length; i++){
                event_div = $("#e-" + events_array[i]);
                event_div.remove();
            }

        }).fail(function(){
            console.log('fail'); 
        }); 
    }); 

    $(".del_category").on("click", function(){
        var c_id = $(this).attr('value');
        var category_p = $("#category-" + c_id);

        $.ajax({
            type: "GET",
            url: "/del_category/" + c_id,
        }).done(function(res){
            category_p.remove();
        }).fail(function(){
            console.log('fail'); 
        }); 
    }); 

    $(".show_category_teams").on("click", function(){
        var c_id = $(this).attr('value');
        var team_id = $("#query_team_id").val();
        var event_results = $("#event_results");
        console.log(c_id);

        $.ajax({
            type: "POST",
            url: "/category_teams",
            data: { 
                t_id: team_id, 
                c_id: c_id
            }
        }).done(function(res){
            console.log('ok');
            event_results.html(res);
        }).fail(function(){
            console.log('fail'); 
        }); 
    }); 

}) 
