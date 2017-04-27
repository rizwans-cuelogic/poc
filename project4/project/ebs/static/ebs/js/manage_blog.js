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

  $('#select-all').click(function(event) {
      debugger;   
      if(this.checked) {
          $(':checkbox').each(function() {
              this.checked = true;
      });
      }
      else {
        $(':checkbox').each(function() {
              this.checked = false;
          });
    }
  });
  
  $("#delete-button").click(function () {
    debugger;
    var checkboxes=[]
    $(':checkbox:checked').each(function(i){
      checkboxes[i] = $(this).val();
      blog_id = $(this).val()
      $('#blog_'+blog_id).remove()
    });
    if(checkboxes.length === 0)
   {
    $.notify("please select atleast on checkbox",
    { position:"top center" }
    );

   }
   else{

    $.ajax({	
    	url: '../delete_blog/',
    	data:{'checkboxes':checkboxes},
    	dataType: 'json',
    	type: 'post',
    	success: function (result) {
       debugger ;
       if(result['status']=="Success"){   
          $.notify.defaults({ className: "success" })
            $.notify( 
            "deleted successfully",
            { position:"top center" });
    	 }
      location.reload();
      }
  	});
  }
});

});