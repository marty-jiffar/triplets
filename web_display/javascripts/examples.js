$(document).ready(function() {
    
    //Global Variables :
    var capturedResult = []; //This array stores all the captured radio button values, 
    var videoIDs = []; //This array to store all the video ids of the trials
                          
    var videoFileGeneral = './json_files/examples/';

    var subject ="random user";
    var pctnum=getQueryVariable("pctnum");
    console.log('percent num')
    console.log(pctnum)
    var count=1;
    var res=null;
    var trials = 500;
    var perblock = 5;
    var display_trials = '/ '.concat(perblock.toString());
    $('.totaltrials').html(display_trials);
    $('.trialtype').html("");
    var vid_dimension = resize();
    var start_time;
    var end_time;
    $('.pct_display').html(pctnum)

    //QUESTION NUMBER TO TRACK THE NUMBER OF THE QUESTIONS IN THE TRIAL 
    var $questionNumber = $("#questionNum");
    var data = {
        pctnum:pctnum,
        subject: subject,
        trialnumber:["1"],
        response:[],
        hardness_score:[],
        correct_answer:[],
        time_per_trial:[],
        videoIDs: videoIDs
        };

    //SHOW THE VIDEO CONTENT DIV TO START THE TRIAL 
    $(".videoContent").show();
    
    
    function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i ++){
            var pair = vars[i].split("=");
            if (pair[0] == variable){
                return pair[1];
            }
        }
        return 1;
    }

    function showRandomVideos (counter){
        //retrieve data from JSON file 
        var videosCurrent = videoFileGeneral.concat(data.pctnum, '_pct.json');
        console.log(videosCurrent);
        $.getJSON(videosCurrent, function(videos) { 
            var rand_num= Math.floor(Math.random()*2);
            console.log(videos[counter].Anchor);
            var anchr_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Anchor);
            var pos_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Positive);
            var neg_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Negative);
            var vid_general = '<video width={{W}} height={{H}} controls autoplay loop><source src="{{SRC}}" type="video/mp4"></video>';
            
            console.log(anchr_src);
            console.log(pos_src);
            console.log(neg_src);
            
            data.videoIDs.push([anchr_src, pos_src, neg_src]);
            vid_general = vid_general.replace('{{W}}', vid_dimension[1]);
            vid_general = vid_general.replace('{{H}}', vid_dimension[0]);

            var anchor = vid_general.replace('{{SRC}}', anchr_src);
            var positive = vid_general.replace('{{SRC}}', pos_src);
            var negative = vid_general.replace('{{SRC}}', neg_src);
            
            $('.contentA').html(positive);
            $('.contentB').html(negative);
     
            //SHOW THE RANDOMIZE VIDEO IN THE DIV
          
            $('.content').html(anchor);
            
            start_time = new Date().getTime(); // time when videos have been loaded
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
    //Capture the value of the input [name = clothchoice] 
        var response = $('input[name="clothchoice"]:checked').val();
        var hardness_score = $('input[name="hardness_score"]:checked').val();
        if (response != null && hardness_score != null){
            data.response.push(response);
            data.hardness_score.push(hardness_score);
            capturedResult.push(response);   //Push val to global array (capturedResult) 
            res= response;
        }
        else {
            res = null;
        }
    }
    console.log('show random vids called...');
    showRandomVideos(count);
    
    console.log('show random vids over...');
    
    // Next button functionality
    $("#next").click(function() {
        // When the 'next' button is clicked, storeValues will execute
        storeValues();
        // checking question number
        end_time = new Date().getTime(); // time when user submits their selection
        console.log("start time: ", start_time);
        console.log("end time: ", end_time);
        data.time_per_trial.push(end_time - start_time);
        console.log("res not null...");
        if ($questionNumber.text() <= perblock) {
            $questionNumber.text(+$questionNumber.text() + 1);

            //RESET RADIO BUTTONS:
            $('input:radio[name="clothchoice"]').attr('checked', false);
            $('input:radio[name="hardness_score"]').attr('checked', false);

            //Show the array of the data (debugging)
            console.log("Video Ids:");
            console.log(videoIDs);
            console.log("user answers:");
            console.log(data.cloth_choice);
            console.log(data.hardness_score);
            console.log($questionNumber.text())
            res=null;
        }

        // When the videos reach the end of the block, data is saved
        if ($questionNumber.text() == perblock+1) {
            console.log('block over, data saving...');
            $(".videos").hide(); //HIDE THE VIDEOS
            $("#next").hide(); //HIDE NEXT BUTTON 
            $.ajax({
                type: "POST",
                dataType : 'json',
                async: false,
                url: 'javascripts/phpcode/saveresults.php',
                data: {data: JSON.stringify(data) },
                success: function (data) {alert(data); },
                failure: function() {alert("Error!");}
            });
            console.log('data saved');
            // When the last block is over, user is moved to 'thank you' page
            if (data.blocknumber == trials / perblock) {
                window.open("thanks.html");
            }
            else {
                next_pct = (parseInt(data.pctnum) + 25).toString();
                next_window = "quiz_cloth_1.html?pctnum=".concat(next_pct);
                window.open(next_window);
            }
        }
        else {
            console.log("block not over, next videos...");
            data.trialnumber.push($questionNumber.text());
            showRandomVideos($questionNumber.text());
        }
    });
    
    // If user hits 'enter' key, go to next trial
    window.addEventListener('keypress', function(e) {
        if (e.keyCode === 13) {
            $("#next").click();
        }
    });
});