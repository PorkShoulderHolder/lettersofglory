/**
 * Created by sam.royston on 4/7/14.
 */
var GAME_STATE;

$("#flip").click(function(){
    var i = Math.floor(Math.random() * GAME_STATE.hidden_letters.length);
    var letter = GAME_STATE.hidden_letters[i];
    $("#letters").append(letter + ", ");

    $.get("/api/letter?new_letter=" + letter + "&id=" + GAME_STATE.id, function(data){
        handleAnswer(data)
    })
})

$("#new_word").click(function(){
    var word = prompt('Enter Word:');
    var datum = validateLocally(word);
    if(datum){
         $.get("/api/validate?new_word=" + datum.new_word + "&old_word=" + datum.old_word + "&letters_used=" + datum.letters_used + "&id=" + GAME_STATE.id,
         function(state){
             updateGameState(state);
         });
    }
})

function validateLocally(word){
    var output = false;



    GAME_STATE.words.forEach(function(existing_word){
        existing_word_copy = existing_word.split('').sort().join('');
        new_word_copy = word.split('').sort().join('');
        var new_letters = [];
        var i = 0;
        var j = 0;
        while(i < new_word_copy.length){

            var letter1 = new_word_copy[i];
            var letter2 = existing_word_copy[j];
            console.log(letter1,letter2);
            if((letter1 != letter2 || typeof letter2 == 'undefined') && GAME_STATE.exposed_letters.indexOf(letter1) != -1){
                console.log(letter1,letter2);
                new_letters.push(letter1);
                i++;
            }
            else if( letter1 != letter2 ){
                i++;
            }
            else{
                i++;
                j++;
            }
        }
        existing_word_copy = (word.length - existing_word.length) == new_letters.length ? existing_word : '';
        if(new_letters.length + existing_word_copy.length == word.length && new_letters.length > 0){
            output = {"old_word": existing_word, "new_word":word, "letters_used":new_letters}
        }
    });
    return output;
}


function handleAnswer(data){
      data = JSON.parse(data);
      if(data.length > 0){
          var datum = data[0];
          console.log(datum);
          var accept = false;
          if( datum.old_word.length > 0 ){
              accept = confirm('I want to snatch "' + datum.old_word + '" to make "' + datum.new_word);
          }
          else{
              accept = confirm(datum.new_word + "!");
          }
          if(accept){
              $.get("/api/validate?new_word=" + datum.new_word + "&old_word=" + datum.old_word + "&letters_used=" + datum.letters_used + "&id=" + GAME_STATE.id,
              function(state){
                  updateGameState(state);
              });
          }
          else{
              $.get("/api/get_game?id=" + GAME_STATE.id,
              function(state){
                  updateGameState(state);
              });
          }
      }
}

$(window).keypress(function(e) {
  var letter = String.fromCharCode(e.which);
  $("#letters").append(letter + ", ");
  $.get("/api/letter?new_letter=" + letter + "&id=" + GAME_STATE.id, function(data){
      handleAnswer(data)
    })
});

function updateGameState(state){
    console.log(state);
    GAME_STATE = JSON.parse(state);
    $("#words").html("");
    $("#letters").html("");
    console.log(GAME_STATE)
    GAME_STATE.words.forEach(function(word){
        $("#words").append(word + " ")
    })
    GAME_STATE.exposed_letters.forEach(function(letter){
        $("#letters").append(letter)
    })
}