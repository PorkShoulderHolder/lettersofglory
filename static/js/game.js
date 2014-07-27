/**
 * Created by sam.royston on 4/7/14.
 */
var GAME_STATE;
var SUBMISSION = '';

$("#flip").click(function(){
    var i = Math.floor(Math.random() * GAME_STATE.hidden_letters.length);
    var letter = GAME_STATE.hidden_letters[i];
    $("#letters").append(letter + ", ");

    $.get("/api/letter?new_letter=" + letter + "&id=" + GAME_STATE.id, function(data){
        handleAnswer(data)
    });
});

$("#new_word").click(function(){
    var word = prompt('Enter Word:');
    submitNewWord(word);
});

function submitNewWord(word){
    var datum = validateLocally(word);
    console.log(datum);
    if(datum){
         $.get("/api/validate?new_word=" + datum.new_word + "&old_word=" + datum.old_word + "&letters_used=" + datum.letters_used + "&id=" + GAME_STATE.id,
         function(state){
             updateGameState(state);
         });
    }
}

String.prototype.containsChars = function(string){
    var copy = this.split('');
    var copy2 = string.split('');
    copy = copy.sort().join('');
    copy2 = copy2.sort().join('');
    var containsSubstring =  copy.indexOf(copy2) != -1;
    if(containsSubstring){
        return true;
    }
    else{
        for(var i = 0; i < copy2.length; i++){
            var l = copy2[i];
            if(copy.indexOf(l) != -1){
                return true
            }
        }
        return false;
    }
};

function validateLocally(word){
    var output = false;
    GAME_STATE.words.forEach(function(existing_word){
        existing_word_copy = existing_word.split('').sort().join('');
        new_word_copy = word.split('').sort().join('');

        var new_letters = [];
        var i = 0;
        var j = 0;
        while(i < new_word_copy.length){
            var letter = new_word_copy[i];
            if(GAME_STATE.exposed_letters.indexOf(letter) != -1 && existing_word.indexOf(letter) == -1){
                new_letters.push(letter);
            }
            i ++;
        }
        existing_word_copy = (word.length - existing_word.length) == new_letters.length ? existing_word : '';
        if(new_letters.length + existing_word_copy.length == word.length && new_letters.length > 0 && word.containsChars(existing_word) && existing_word != ''){
            output = {"old_word": existing_word, "new_word":word, "letters_used":new_letters}
        }
        else if(new_letters.length == word.length && new_letters.length > 0 && word.containsChars(new_letters.join(''))){
            output = {"old_word": '', "new_word":word, "letters_used":word.split('')}
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
          if(data != '0'){
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
                  $.get("/api/rejected?id=" + GAME_STATE.id + "&word=" + datum.new_word);

                  $.get("/api/get_game?id=" + GAME_STATE.id,
                  function(state){
                      updateGameState(state);
                  });
              }
          }
          else{
              $.get("/api/get_game?id=" + GAME_STATE.id,
                  function(state){
                      updateGameState(state);
                  });
          }
      }
}

function updateSubmissionText(){
    $("#display").html(SUBMISSION);
}


$(document).keydown(function(e) {
    var charCode = e.keyCode;
    var letter = String.fromCharCode(charCode);
    if(GAME_STATE.ai){
        // if computer is playing then use key inputs to signify new flipped letters
        $("#letters").append(letter + ", ");
        $.get("/api/letter?new_letter=" + letter + "&id=" + GAME_STATE.id, function(data){
          handleAnswer(data)
        })
    }
    else if(charCode == 13){
        // return key
        submitNewWord(SUBMISSION);
        SUBMISSION = '';
        updateSubmissionText();
    }
    else if(charCode == 46 || charCode == 8){
        // delete key
        e.preventDefault();
        console.log(SUBMISSION);
        SUBMISSION = SUBMISSION.substring(0,SUBMISSION.length - 1);
        updateSubmissionText();
    }
    else if('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(letter) != -1){
        // any other key
        SUBMISSION += letter.toLowerCase();
        updateSubmissionText();
    }
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