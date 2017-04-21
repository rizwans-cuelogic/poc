$(document).ready(function() {
	$("#myform").submit(function (e){
	var $form=$(this);
   	if(0 < $form.find('.has-error').length){ 
		return false;
	} 
   console.log($form);
   console.log($(this).serialize());
   $.ajax({
      type: "POST",
      url: 'register/',
      data: new FormData(this),  
      dataType:"JSON",
      processData: false,
      contentType: false,
      success: function(result){
        if(result['status']=='Error'){
            $('#validator_message').notify(result['message']);
        }
        else{
          $.notify(result['message'],"success");
          $('#myform')[0].reset();
          $('#myform').bootstrapValidator('resetForm',true);
          $('#bannerformmodal').modal('hide');
          /* this is required for redirceting to home' */
          /*setInterval(function(){ 
                window.location.replace('/');

             }, 4000);*/
          return false;
        }
    }
    });
  return false;
});

$('body').on('hidden.bs.modal', '.modal', function () {
$('#myform')[0].reset();
 $('#myform').bootstrapValidator('resetForm',true);
});
});

