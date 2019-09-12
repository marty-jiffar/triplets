$(document).ready(function() {
  
  //Global Variables :
  var capturedResult = []; //This array stores all the captured radio buttton values, 
  var videoIDs = []; //This arrary to store all the video ids of the trials
  
                          
  var videoLinks1 = ['./json_files/block_1.json'];

  //RANDOMIZE THE JSON FILES
  randomize_jsonFiles1 =0;
  var subject ="random user";
  var blocknumber=1;
  var res=null;
  var count=0

  var const_string ="https://www.youtube.com/embed/"

  //QUESTION NUMBER TO TRACK THE NUMBER OF THE QUESTIONS IN THE TRIAL 
  var $questionNumber = $("#questionNum");
  var data = {
                blocknumber:blocknumber,
                subject: subject,
                examplenumber:[],
                response:[],
                correct_answer:[]
                
            };

  //SHOW THE VIDEO CONTENT DIV TO START THE TRIAL 
  $(".videoContent").show();

    $(function() {
                subject = prompt("Please enter your full name and separate your first and last name by an underscore");
                data.subject=subject;
            });
  //NEW VIDEO FUNCTION
  function showRandomVideos (){
     
     var videoID_triplet = ""; //an empty string to store video ids as pairs
     //retrieve data from JSON file 
     $.getJSON(videoLinks1[randomize_jsonFiles1], function(videos) {
      //VIDEO FRAME


      

      var videoFrame = '<iframe embed-responsive src="{{SRC}}?autoplay=1&loop=1&rel=0&showinfo=0&playlist={{SRC2}}" frameborder="0" allowfullscreen></iframe>';//Video Frame1
      
       //RANDOMIZE VIDEO ORDER
       var num= Math.floor(Math.random()*2);


       var video1 = videoFrame.replace('{{SRC}}', videos[count].positive);

       video1 =video1.replace('{{SRC2}}',videos[count].positive.replace(const_string,''))

       var video2 = videoFrame.replace('{{SRC}}', videos[count].anchor);
       video2 =video2.replace('{{SRC2}}',videos[count].anchor.replace(const_string,''))


       var video3 = videoFrame.replace('{{SRC}}', videos[count].negative);
       video3 =video3.replace('{{SRC2}}',videos[count].negative.replace(const_string,''))


       if (num==0)
       {
          $('.content1').html(video1);
          $('.content').html(video3);
          data.response.push("1")
       }
       else
       {
          $('.content1').html(video3);
          $('.content').html(video1);
          data.response.push("-1")
       }
     
      //SHOW THE RANDOMIZE VIDEO IN THE DIV
          
          $('.content2').html(video2);
          count=count+1;
    
    });
  
}//END OF SHOW RANDOM VIDEOS FUNCTION
  
  
  //STORE THE VALUES OF THE RADIO BUTTONS
  function storeValues(){
    //Capture the value of the input [type = radio] 
    $('input[type="radio"]:checked').each(function() {
        data.response.push($(this).val());
        capturedResult .push($(this).val());       //Push the Value to the global array (capturedResult) 
        res= $(this).val();


   });
    //return capturedResult;  //return the value of the array     
  } //END
 
  
 //NEXT BUTTON FUNCTIONALITY
  $("#next").click(function(e) {
   //WHEN THE NEXT BUTTON IS CLICKED, showRandomVideos will execute
      showRandomVideos ();
      
      data.examplenumber.push($questionNumber.text());
      //CHECKING THE QUESTION NUMBER 
      if ($questionNumber.text() <=100) {
          //If the question number is less than 20 , add one to the span id=questionNum
          $questionNumber.text(+$questionNumber.text() + 1);
          
           //Run the function //storeValues() to capture data from the user and push it to the global array capturedValue
          storeValues();
          //console.log(res);

          // If user forgets to label a video, put its label as 100
          if (res==null)
          {
            //console.log(res);
            alert("You did not select an option. Please make a selection for all following trials.");
            data.response.push("100");
          }

          /*if(res== "")
          {
            alert("Please choose something");
            data.response.push("-100");

          };*/

          //RESET RADIO BUTTON:
          $('input:radio[name="scale"]').attr('checked', false);
          //Show the array of the data (debugging)
           console.log("Video Ids:");
           console.log(videoIDs);
           console.log("user answers");
           console.log(data.response);
           console.log(res);
           res=null
          
      }

      //IF THE VIDEOS REACHED THE END -20- THE FRAMES DISAPPEAR AND  THE USER IS MOVED TO "THANK YOU" PAGE
      if ($questionNumber.text() == 101) {
         $(".hideVideos").hide(); //HIDE THE VIDEOS
         $("#next").hide(); //HIDE NEXT BUTTON 
         //window.open('http://codepen.io/ZeeMax/full/LGajja', '_self', false);//MOVE THE USER TO THE THANK YOU PAGE
         //document.write(data.response,data.examplenumber)
         //window.open("demo_page.html");
          //document.write(JSON.stringify(data));
          //document.write("<p> I am here</p>");
          $.ajax({
                 type: "POST",
                 dataType : 'json',
                 async: false,
                 url: 'javascripts/phpcode/saveresults.php',
                 data: {data: JSON.stringify(data) },
                 success: function (data) {alert(data); },
                 failure: function() {alert("Error!");}
            });

          window.open("proceed_1.html");
        
      }
    
  });//END
  
  
 //CALL THE FUNCTIONS TO SHOW THE VIDEOS 

 showRandomVideos ();
 //storeValues();


    
});