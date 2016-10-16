$(document).ready(function()
{
   //$("#dialogWrapper").draggable();
   
   $("#mainInput").keypress(function(e) {
      if(e.which == 13) {
         var question = $(this).val();
         askQuestion(question);
      }
   });
   
});

function askQuestion(question)
{
   // Insert question into chat.
   var questionDiv = $("<div/>")
      .addClass("resultRow question")
      .appendTo("#resultsList");
      
      $("<div/>")
         .addClass("resultRowIconYou")
         .html("You Asked:")
         .appendTo(questionDiv);
      
      $("<div/>")
         .addClass("resultRowText")
         .html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	"+question)
         .appendTo(questionDiv);
   
   
   // Get the answer.
   $.ajax({
	url: 'http://localhost:888/AskIrina',
	cache: false,
	dataType: 'jsonp',
	data: {
		text: question
	},
	success: function(returnJson) {
		console.log("Ajax success: "+returnJson);
		   
	   var questionDiv = $("<div/>")
		  .addClass("resultRow question")
		  .appendTo("#resultsList");
		  
		  $("<div/>")
			 .addClass("resultRowIconIrina")
			 .html("Irina:")
			 .appendTo(questionDiv);
		  
		  $("<div/>")
			 .addClass("resultRowText")
			 .html("&nbsp;&nbsp; 	"+returnJson.answer)
			 .appendTo(questionDiv);
			 
		 if(returnJson.link)
		 {
			  $("<a/>")
				 .addClass("resultRowLink")
				 .attr('href',returnJson.link)
				 .html(""+returnJson.link)
				 .appendTo(questionDiv);
		 }
		 
		/*
		   For just reference:
		   <div class="resultRow answer">
			  <div class="resultRowIconIrina">Irina:</div>
			  <div class="resultRowText">
				 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	What is database?
			  </div>
		   </div>
*/

		// Scroll the div down to show the answer.
		$("#resultsList").delay(100).animate({scrollTop: $("#resultsList").height()}, 200);
		
		
        $("#mainInput").val("");
	},
	error: function(x, status, error) {
		console.log("Ajax error.");
	}
   });
   
} // --- End askQuestion().