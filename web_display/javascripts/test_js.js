$(document).ready(function() {
  
    //Global Variables :
    var capturedResult = []; //This array stores all the captured radio button values, 
    var videoIDs = []; //This array to store all the video ids of the trials
  
                          
    var videoLinks1 = './json_files/chunk_0.json';

    var subject ="random user";
    var blocknumber=1;
    var count=1;
    var res=null;
    var trials=3;

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
        var bn = getQueryVariable("blocknum");
        blocknumber = bn ? bn : 1;
    });

    function showRandomVideos (counter){
        var videoID_triplet = ""; //an empty string to store video ids as pairs
        //retrieve data from JSON file 
        $.getJSON(videoLinks1, function(videos) { 
   
            var rand_num= Math.floor(Math.random()*2);

            var anchr_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Anchor);

            var pos_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Positive);

            var neg_src = './Final_Dataset_6sec_mp4/'.concat(videos[counter].Negative);

            var vid_general = '<video width="320" height="240" controls autoplay loop><source src="{{SRC}}" type="video/mp4"></video>';
            
            videoIDs.push([anchr_src, pos_src, neg_src]);

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
    
    //STORE THE VALUES OF THE RADIO BUTTONS
    function storeValues(){
    //Capture the value of the input [type = radio] 
        var radio_value = $('input[type="radio"]:checked').val();
        if (radio_value != null){
            data.response.push(radio_value);
            capturedResult.push(radio_value);   //Push val to global array (capturedResult) 
            res= radio_value;
        }
    }
    //return capturedResult;  //return the value of the array
   
    
//CALL THE FUNCTIONS TO SHOW THE VIDEOS    
showRandomVideos(count);
    
//NEXT BUTTON FUNCTIONALITY
$("#next").click(function(e) {
        
        //If user forgets to label a video, prompt them to enter one.
    //    if (res==null)
    //      {
    //        //console.log(res);
    //        alert("Please select an option.");
    //      }
    //    else {
          //WHEN THE NEXT BUTTON IS CLICKED, storeValues will execute
            storeValues();
            
            //CHECKING THE QUESTION NUMBER 
            if ($questionNumber.text() <= trials) {
                //If the question number is less than trial num, add one to the span id=questionNum
                $questionNumber.text(+$questionNumber.text() + 1);
                data.trialnumber.push($questionNumber.text());

                //console.log(res);

                // If user forgets to label a video, put its label as 100

                //res=null;
                
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

            //IF THE VIDEOS REACHED THE END -20- THE FRAMES DISAPPEAR AND  THE USER IS MOVED TO "THANK YOU" PAGE
            if ($questionNumber.text() == trials+1) {
                $(".hideVideos").hide(); //HIDE THE VIDEOS
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

                window.open("thanks.html");
            }
            else {
                showRandomVideos($questionNumber.text());
            }
        });
});