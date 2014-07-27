/**
 * Created by sam.royston on 3/28/14.
 */
$(document).ready(function(){
    $("#new_game_nocomp").click(function(){
        $.get("/new_game?ai=0", function(data){
            console.log(data);
            window.location = "/gameview?game_id=" + data;
        });
    });
    $("#new_game_comp").click(function(){
         $.get("/new_game?ai=1", function(data){
            console.log(data);
            window.location = "/gameview?game_id=" + data;
        });
    });
});