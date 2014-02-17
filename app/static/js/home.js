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

    $(".tag_teams").on("click", function(){
        var tag_id = $(this).attr('value');
        console.log(tag_id);

        $.ajax({
            type: "POST",
            url: "tag_teams",
            data: { tag_id: tag_id }
        }).done(function(entries){
            $("#search_results").html(entries);
        }).fail(function(){
            console.log('fail');
        });
    });

})
