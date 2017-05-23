$(document).ready(function(){
	if($('#preview').is(":visible")){
		$('#id_attachments').hide();
		$('#attached-row').removeClass('form-group');
	}
	$(document).on('click','#button1',function(){
		var value=$(this).attr('value');
		file1='file1'
		attachments='id_attachments'
		deleteAttachment(value,file1,attachments)
	})
	deleteAttachment=function(value,file1,attachments){
			swal({
  			title: "Are you sure?",
  			text: "You will not be able to recover this file!",
  			type: "warning",
  			showCancelButton: true,
  			confirmButtonColor: "#DD6B55",
  			confirmButtonText: "Yes, delete it!",
  			closeOnConfirm: false
		},
		function(){
			$.ajax({
				url: '../../update_delete_blog/',
	        	data:{'value':value},
	        	dataType: 'json',
	        	type: 'post',
	        	success: function (result) {
					$('#'+attachments).show();
					$('#preview').remove();
					swal("Deleted!", "Your file has been deleted.", "success");
	    		}
	    	});
		});		
	}
	var status=$('#date_status').val()
	if (status=='True'){
		$("#id_published").prop("readonly", true);
	}
})