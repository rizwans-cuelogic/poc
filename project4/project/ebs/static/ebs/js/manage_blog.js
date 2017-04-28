$(document).ready(function() {    
  if(document.getElementById('message')!==null){
    	$.notify.defaults({ className: "success" })
        $.notify( 
            "Blog details saved successfully",
           { position:"top center" }
        );
    }
    $(".search").keyup(function () {
      var searchTerm = $(".search").val();
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
      var checkboxes=[]
      $(':checkbox:checked').each(function(i){
        checkboxes[i] = $(this).val();
        blog_id = $(this).val()
        $('#blog_'+blog_id).remove()
      });
      var message=$('notifyjs-corner').is(":visible")
      if(checkboxes.length === 0 && !message)
      {
         $.notify.defaults({ className: "error" })
        $.notify("please select atleast one checkbox",
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
          if(result['status']=="Success"){   
            location.reload();
            var url=window.location.href;
            url+='?deleted=1'
            window.location.href=url;   
        }
      }
    });
  }
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

if(getParameterByName('deleted')){    
  $.notify.defaults({ className: "success" })
                    $.notify( 
                    "Blog deleted successfully",
                    { position:"top center" }
                  )
  history.pushState(null, null, '/manage_blog/');
}

});


