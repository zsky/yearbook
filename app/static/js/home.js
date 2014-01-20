$(document).ready(function(){
    $(".login").on("click", function(){
        $(".registerDiv").hide();
        $(".loginDiv").toggle();
    });
    $(".register").on("click", function(){
        $(".loginDiv").hide();
        $(".registerDiv").toggle();
    });

})
