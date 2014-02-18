$(document).ready(function(){

    $('#register_div').on('focusout', '.email', function(){
        var email = $(this).val();
        if(email == "") return;
        $.ajax({
            type: "POST",
            url: "/check_info",
            data: { info: email }
        }).done(function(res){
            var results = JSON.parse(res);
            console.log(results);
            if(results.succ){
            $('#register_div .show_error').html("");
            }else{
            $('#register_div .show_error').html(results.msg);
            }
        }).fail(function(){
            console.log('fail');
        });
    })

    $('#register_div').on('click', '.register_btn', function(){
        var username = $('#register_div .username').val();
        var email  = $('#register_div .email').val();
        var password = $('#register_div .password').val();

        $.ajax({
            type: "POST",
            url: "/register",
            data: { username: username,
                    email: email,
                    password: password
            }
        }).done(function(res){
            var results = JSON.parse(res);
            console.log(results);
            if(results.succ){
            $('#register_modal').modal('hide');
            window.location.href = "/profile";
            }else{
            $('#register_div .show_error').html(results.msg);
            }
        }).fail(function(){
            console.log('fail');
        });
    })

    $('#login_div').on('click', '.login_btn', function(){
        var email = $('#login_div .email').val();
        var password = $('#login_div .password').val();

        $.ajax({
            type: "POST",
            url: "/login",
            data: { 
                    email: email,
                    password: password
            }
        }).done(function(res){
            var results = JSON.parse(res);
            console.log(results);
            if(results.succ){
            $('#login_modal').modal('hide');
            window.location.href = "/profile";
            }else{
            $('#login_modal .show_error').html(results.msg);
            }
        }).fail(function(){
            console.log('fail');
        });
    })


})
