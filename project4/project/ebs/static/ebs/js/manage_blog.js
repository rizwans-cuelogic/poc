$(document).ready(function() {    
	$("#success-alert").hide();
    $("#success-alert").alert();
    $("#success-alert").fadeTo(1000, 300).slideUp(500, function(){
    $("#success-alert").slideUp(500);});

});