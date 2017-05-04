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
		$('#attached').show()
		$('#file1').remove();
		$('#id_attachments').show();
		$('#attached-row').addClass('form-group');
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
			$('#label-uploaded').remove();
		}
		if($('#file3').text()=="" && $('#file1').text()=="" && $('#file2').text()==""){
			$('#upload-row').removeClass('form-group');
		}
		var value=$(this).attr('value');
		$.ajax({
			url: '../../update_delete_blog/',
	        data:{'value':value},
	        dataType: 'json',
	        type: 'post',
	        success: function (result) {
	    	}
	    });
	})
 	$(document).on('click','#button2',function(){
 		$('#attached').show()
		$('#file2').remove();
		$('#id_image1').show();
		$('#attached-row').addClass('form-group');
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
			$('#label-uploaded').remove();
		}
		if($('#file3').text()=="" && $('#file1').text()=="" && $('#file2').text()==""){
			$('#upload-row').removeClass('form-group');
		}
		var value=$(this).attr('value');
		$.ajax({
			url: '../../update_delete_blog/',
	        data:{'value':value},
	        dataType: 'json',
	        type: 'post',
	        success: function (result) {
	    	}
	    });		
	})
	$(document).on('click','#button3',function(){
		$('#attached').show()
		$('#file3').remove();
		$('#id_image2').show();
		$('#attached-row').addClass('form-group');
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
			$('#label-uploaded').remove();
		}
		if($('#file3').text()=="" && $('#file1').text()=="" && $('#file2').text()==""){
			$('#upload-row').removeClass('form-group');
		}
		var value=$(this).attr('value');
		$.ajax({
			url: '../../update_delete_blog/',
	        data:{'value':value},
	        dataType: 'json',
	        type: 'post',
	        success: function (result) {
	    		 	
	    	}
	    });
	})
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