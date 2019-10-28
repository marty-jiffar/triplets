$(document).ready(function() {
    
    //Global Variables :
                          
    var videoFileGeneral = './json_files/examples/';
    var pctnum=getQueryVariable("pctnum");
    console.log('percent num')
    console.log(pctnum)
    
    var count=1;
    
    var total_examples = 25;
    var perblock = 5;
    var display_trials = '/ '.concat(perblock.toString());
    $('.totaltrials').html(display_trials);
    $('.trialtype').html("");
    var vid_dimension = resize();
    
    $('.pct_display').html(pctnum)

    //QUESTION NUMBER TO TRACK THE NUMBER OF THE QUESTIONS IN THE TRIAL 
    var $exampleNumber = $("#exampleNum");
    /*
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
        
    */

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

    function showVideos (counter){
        //retrieve data from JSON file 
        var videosCurrent = videoFileGeneral.concat(data.pctnum, '_pct.json');
        console.log(videosCurrent);
        $.getJSON(videosCurrent, function(videos) { 
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
            $('.content').html(anchor);
            $('.contentB').html(negative);
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
    
    console.log('show vids called...');
    showVideos(count);
    
    console.log('show vids over...');
    
    // Next button functionality
    $("#next").click(function() {
        // checking question number
        if ($exampleNumber.text() <= perblock) {
            $examleNumber.text(+$exampleNumber.text() + 1);

            //Show the array of the data (debugging)
            console.log($questionNumber.text())
        }

        // When the videos reach the end of the block, go to next block
        if ($questionNumber.text() == perblock+1) {
            // When the last block is over, user is moved to 'thank you' page
            if (pct_num == "100") {
                window.open("thanks.html");
            }
            else {
                next_pct = (parseInt(data.pctnum) + 25).toString();
                next_window = "triplet_examples.html?pctnum=".concat(next_pct);
                window.open(next_window);
            }
        }
        // if block not over, go to next example in block
        else {
            console.log("example block not over, next videos...");
            showRandomVideos($questionNumber.text());
        }
    });
    
    // If user hits 'enter' key, go to next example
    window.addEventListener('keypress', function(e) {
        if (e.keyCode === 13) {
            $("#next").click();
        }
    });
});