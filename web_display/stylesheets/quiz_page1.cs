@import url("https://fonts.googleapis.com/css?family=Raleway:300,400");
@import url("https://fonts.googleapis.com/css?family=Montserrat:700");
* {
  -webkit-transition: 0.4s ease;
  transition: 0.4s ease;
}
body {
  // background-color: #161717;
 background:url("http://img2.goodfon.su/wallpaper/big/f/b7/fon-tekstura-tkan-dzhins.jpg") fixed;
 background-size:cover;
  font-size: 22px;
  line-height: 28px;
  letter-spacing: 4px;
  font-family: "Raleway";
  font-weight: 400;
}
.fixed-nav-bar {
  // background-color: #161717;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  min-height: 100px;
  padding: 0 25px;
  box-sizing: border-box;
    background-color: #5F6E76;
  // background-color: rgba(255,255,255,0.02);
  box-shadow: 0 0 15px 2px rgba(0,0,0,0.5);
  z-index: 100;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  -webkit-transition: 0.35s ease;
  transition: 0.35s ease;
}
.fixed-nav-bar .logo {
  
  position: absolute;
  left: 35%;
   top: 50%;
   text-align:center;
  -webkit-transform: translateY(-50%);
          transform: translateY(-50%);
  text-transform: uppercase;
  color: white;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
}
.fixed-nav-bar .logo span {
  color:#1104E3;
  
}

.fixed-nav-bar.scrolled {
  min-height: 60px;
  background-color: #fdfdfd;
  box-shadow: 0 0 30px 3px rgba(0,0,0,0.6);
}
.fixed-nav-bar.scrolled .logo {
  color: #000;
}
.fixed-nav-bar.scrolled .menu-button-label .white-bar {
  background-color: #000;
}

//Drop menu
.drop-down-container {
  height: 15%;
  width: 90%;
  left: 160%;
  margin-top: 5px;
  -webkit-transform: translateX(-50%);
          transform: translateX(-50%);
  -webkit-transition: 0.3s ease;
  transition: 0.3s ease;
}



.videos{
 width:100%;
 height:100%;
 /*width:660px;
 height:500px;*/
padding-top: 10%;
 text-align:center;
 font-weight:bold;
}

#materialA{
  padding-right:30%;
}
#materialB{
   padding-left:30%;
}
#materialC{
  text-align:center;
}

label{
  color:black;
  font-size:19px;
  padding: 1% 10% 5% 10%;
  /*padding:1%;*/
  font-family: "Raleway";
  font-weight:bold;
}


.textLabel{
  margin-left:10px;
}

 iframe{
  /*width:490px;
  height:470px;*/
  width:32%;
  height:65%;
  padding:10px;
  margin-left:5px;
  // margin-top:30px;
  border-radius:20px;
} 

button{
 position: fixed;
    bottom: 30px;
    right: 30px; 
   background-color: #161717;
   border:none;
   border-radius:50px;
   width:100px;
   height:100px;
   
}

  
/* Modal Header */

#myModal{
  text-align:center;
  margin:100px auto;
  width:750px;
}
.modal-header {
     padding: 10px;
    background-color: #195E19;
    color: white;
}

/* Modal Body */
.modal-body {
  
  padding: 30px;
  
  height:100px;
  }

/* Modal Content */
.modal-content {
    position: relative;
    background-color: #fefefe;
    margin: auto;
    padding: 0;
    border: 1px solid #888;
    width: 80%;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
    -webkit-animation-name: animatetop;
    -webkit-animation-duration: 0.4s;
    animation-name: animatetop;
    animation-duration: 0.4s
}

/* Add Animation */
@-webkit-keyframes animatetop {
    from {top: -300px; opacity: 0} 
    to {top: 0; opacity: 1}
}

@keyframes animatetop {
    from {top: -300px; opacity: 0}
    to {top: 0; opacity: 1}
}

/* The Close Button */
.close {
    color: black;
    float: right;
    font-size: 45px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
}