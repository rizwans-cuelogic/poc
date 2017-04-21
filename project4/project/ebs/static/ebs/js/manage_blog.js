$(document).ready(function() {    
	if(document.getElementById('message')!==null){
    	$.notify.defaults({ className: "success" })
        $.notify( 
            "Blog details saved successfully",
           { position:"top center" }
        );
    }
});