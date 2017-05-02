$(document).ready(function(){

	if($('#file1').text()!=""){
		$('#id_attachments').hide();
	} 
	if($('#file2').text()!=""){
		$('#id_image1').hide();
	}
	$(document).on('click','#button1',function(){
		$(this).parents('span').remove();
		$('#id_attachments').show();
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
		$('#label-uploaded').remove();
	}		
	})
 	$(document).on('click','#button2',function(){
		$(this).parents('span').remove();
		$('#id_image1').show();
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
		$('#label-uploaded').remove();
	}		
	})
	$(document).on('click','#button3',function(){
		$(this).parents('span').remove();
		$('#id_image2').show();
		if(!$('#file1').is(':visible') && !$('#file2').is(':visible') && !$('#file3').is(':visible')){
		$('#label-uploaded').remove();
	}		
	})
	

})