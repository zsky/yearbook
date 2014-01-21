$(document).ready(function(){
    $(".login").on("click", function(){
        $(".registerDiv").hide();
        $(".loginDiv").toggle();
    });
    $(".register").on("click", function(){
        $(".loginDiv").hide();
        $(".registerDiv").toggle();
    });

    $("#search_button").on("click", function(){
        var search_words = $(".search_words").val();

        $.ajax({
            type: "POST",
            url: "search_teams",
            data: { words: search_words }
        }).done(function(entries){
            $("#search_results").html(entries);
        }).fail(function(){
            console.log('fail');
        });
    });


})
