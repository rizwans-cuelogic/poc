$(document).ready(function() {    
	if(document.getElementById('message')!==null){
    	$.notify.defaults({ className: "success" })
        $.notify( 
            "Blog details saved successfully",
           { position:"top center" }
        );
    }

    $(".search1").keyup(function () {
	    var searchTerm = $(".search1").val();
	    var listItem = $('.results tbody').children('tr');
	    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
	    
  		$.extend($.expr[':'], {'containsi': function(elem, i, match, array){
        	return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
    	}
  	});
    
	$(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','false');
	});

	$(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','true');
	});

	var jobCount = $('.results tbody tr[visible="true"]').length;
		$('.counter').text(jobCount + ' item');

	if(jobCount == '0') {$('.no-result').show();}
	else {$('.no-result').hide();}
		  });

    var checkboxes=[]
    $('#select-all').click(function(event) {
    	debugger;   
    	if(this.checked) {
        	$(':checkbox').each(function() {
            	this.checked = true;
            	checkboxes.push($(this).val()) 
			});
    	}
    	else {
    		$(':checkbox').each(function() {
          		this.checked = false;
      		});
 		}
	});
	
	var checkboxobject=$.extend({},checkboxes)
	var checkboxJSON=JSON.stringify(checkboxobject)

	$("#delete-button").click(function () {
  		$.ajax({	
    	url: '../delete_blog/',
    	data: {'checkbox':checkboxJSON},
    	dataType: 'json',
    	type: 'post',
    	success: function (data) {

    	}
  	});
	});

});