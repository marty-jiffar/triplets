$(document).ready(function() {
  
    //Global Variables :
    var capturedResult = []; //This array stores all the captured radio button values, 
    var videoIDs = []; //This array to store all the video ids of the trials
  
                          
    var videoFileGeneral = './json_files/block_';

    var subject ="random user";
    var blocknumber=1;
    var count=1;
    var res=null;
    var trials = 3;
    var perblock = 3;
    var display_trials = '/ '.concat(perblock.toString());
    $('.totaltrials').html(display_trials);
    $('.trialtype').html("Practice");
    var vid_dimension = resize();

    //QUESTION NUMBER TO TRACK THE NUMBER OF THE QUESTIONS IN THE TRIAL 
    var $questionNumber = $("#questionNum");
    var data = {
        blocknumber:blocknumber,
        subject: subject,
        trialnumber:["1"],
        response:[],
        correct_answer:[]
        };

    //SHOW THE VIDEO CONTENT DIV TO START THE TRIAL 
    $(".videoContent").show();
    $(function() {
        subject = prompt("Please enter your initials.");
        data.subject=subject;
    });

    function showRandomVideos (counter){
        //retrieve data from JSON file 
        var videosCurrent = videoFileGeneral.concat(blocknumber.toString(), '.json');
        console.log(videosCurrent);
        $.getJSON(videosCurrent, function(videos) { 
            var rand_num= Math.floor(Math.random()*2);
            var anchr_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Anchor);
            var pos_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Positive);
            var neg_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Negative);
            var vid_general = '<video width={{W}} height={{H}} controls autoplay loop><source src="{{SRC}}" type="video/mp4"></video>';
            
            videoIDs.push([anchr_src, pos_src, neg_src]);
            vid_general = vid_general.replace('{{W}}', vid_dimension[1]);
            vid_general = vid_general.replace('{{H}}', vid_dimension[0]);

            var anchor = vid_general.replace('{{SRC}}', anchr_src);
            var positive = vid_general.replace('{{SRC}}', pos_src);
            var negative = vid_general.replace('{{SRC}}', neg_src);
        
            if (rand_num==0)
            {
                $('.contentA').html(positive);
                $('.contentB').html(negative);
                data.correct_answer.push("1")
            }
            else
            {
                $('.contentA').html(negative);
                $('.contentB').html(positive);
                data.correct_answer.push("-1")
            }
     
            //SHOW THE RANDOMIZE VIDEO IN THE DIV
          
            $('.content').html(anchor);
        });
  
    }//END OF SHOW RANDOM VIDEOS FUNCTION
    
    function resize() {
        var w = window.innerWidth;
        var h = window.innerHeight;
        
        var ideal_height = h * 4 / 12;
        var ideal_width = ideal_height * 16 / 9;
        var info = [ideal_height, ideal_width];
        console.log([h, w])
        console.log(info);
        return info;
    }
    
    //STORE THE VALUES OF THE RADIO BUTTONS
    function storeValues(){
    //Capture the value of the input [type = radio] 
        var radio_value = $('input[type="radio"]:checked').val();
        if (radio_value != null){
            data.response.push(radio_value);
            capturedResult.push(radio_value);   //Push val to global array (capturedResult) 
            res= radio_value;
        }
        else {
            res = null;
        }
    }
    //return capturedResult;  //return the value of the array 
    showRandomVideos(count);
    
    // Next button functionality
    $("#next").click(function() {
        // When the 'next' button is clicked, storeValues will execute
        storeValues();
        
        //If user forgets to label a video, prompt them to enter one.
        if (res==null)
        {
            alert('Please select an option.')
            showRandomVideos($questionNumber.text())
        }
        else {
            // checking question number
            if ($questionNumber.text() <= perblock) {
                $questionNumber.text(+$questionNumber.text() + 1);

                //RESET RADIO BUTTON:
                $('input:radio[name="scale"]').attr('checked', false);

                //Show the array of the data (debugging)
                console.log("Video Ids:");
                console.log(videoIDs);
                console.log("user answers");
                console.log(data.response);
                console.log(res);
                console.log($questionNumber.text())
                res=null;
            }

            // When the videos reach the end of the practice block, user is moved to the real trials
            if ($questionNumber.text() == perblock+1) {
                console.log('block over, moving...');
                $(".videos").hide(); //HIDE THE VIDEOS
                $("#next").hide(); //HIDE NEXT BUTTON 
                window.open("quiz_cloth_1.html?blocknumber=1");
            }
            else {
                console.log("block not over, next videos...");
                data.trialnumber.push($questionNumber.text());
                showRandomVideos($questionNumber.text());
            }
        }
    });
    
    // If user hits 'enter' key, go to next trial
    window.addEventListener('keypress', function(e) {
        if (e.keyCode === 13) {
            $("#next").click();
        }
    });
});