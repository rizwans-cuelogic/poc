$(document).ready(function(){
	if($('#file1').text()!=""){
		$('#id_attachments').hide();
	} 
	if($('#file2').text()!=""){
		$('#id_image1').hide();
	}
	if($('#file3').text()!=""){
		$('#id_image2').hide();
	}
	if($('#file3').text()!="" && $('#file1').text()!="" && $('#file2').text()!=""){
		$('#attached').hide();
		$('#attached-row').removeClass('form-group');
	}
	$(document).on('click','#button1',function(){
		var value=$(this).attr('value');
		file1='file1'
		attachments='id_attachments'
		deleteAttachment(value,file1,attachments)
	})
 	$(document).on('click','#button2',function(){
 		var value=$(this).attr('value');
		file1='file2'
		attachments='id_image1'
		deleteAttachment(value,file1,attachments)
 	})
	$(document).on('click','#button3',function(){
		var value=$(this).attr('value');
		file1='file3'
		attachments='id_image2'
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
	        		$('#attached').show()
					$('#'+file1).remove();
					$('#'+attachments).show();
					$('#attached-row').addClass('form-group');
					if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
						$('#label-uploaded').remove();
					}
					if($('#file3').text()=="" && $('#file1').text()=="" && $('#file2').text()==""){
						$('#upload-row').removeClass('form-group');
					}
					swal("Deleted!", "Your file has been deleted.", "success");
	    		}
	    	});
		});		
	}

	if($('#file3').text()=="" && $('#file1').text()=="" && $('#file2').text()==""){
		$('#upload-row').removeClass('form-group');
	}

		input=$('#id_published').val();
        input=input.split(" ");
        time=input[1].split(":");
    	hours=time[0];
    	minutes=time[1];
        input_date=input[0].split("-");
        input_date=new Date(input_date[0],input_date[1]-1,input_date[2]);
        now=new Date();
    	now1=new Date();
    	now1.setHours(0,0,0,0)
    	getime=now.toLocaleString('en-GB');
    	current_hours=now.getHours();
    	current_minutes=now.getMinutes();
    if(input_date.valueOf()==now1.valueOf()){
        if(hours<current_hours){
            $("#id_published").prop("readonly", true);     
        }
        if(hours==current_hours){
            if(minutes<current_minutes){
        		$("#id_published").prop("readonly", true);                   
            }
        }
    }
    else{ 
    	if(input_date<now ){    
            $("#id_published").prop("readonly", true);
    	}
	}

	if(!$('#id_published').is('[readonly]')){
		$('#id_published_state').hide();
		$('#status').hide();
	}
})