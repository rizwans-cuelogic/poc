$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}
  var param=$.urlParam('filterbox');
  if(param==null){
     sessionStorage.setItem("SelItem", 'al')
}
window.onload = function() {
var selItem = sessionStorage.getItem("SelItem");
$('#filter').val(selItem);
}
$(document).ready(function() {
  if(document.getElementById('message')!==null){
    	$.notify.defaults({ className: "success" })
        $.notify( 
            "Blog details saved successfully",
           { position:"top center" }
        );
    }

  $(document).ready(function(){
    $('.table > tbody > tr > td >.blog-text > p > img').remove();
  })
      
  $('#filter').change(function() {
        var filter_val
        filter_val = $(this).val();
        sessionStorage.setItem("SelItem", filter_val);
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
      });
      var message=$('notifyjs-corner').is(":visible")
      if(checkboxes.length === 0 && !message)
      {
        $.notify.defaults({ className: "error" })
        $.notify("please select atleast one checkbox",
          { position:"top center" }
        );
      }
      else if(checkboxes.length==1 && checkboxes[0]=='on' && !message){
        $.notify.defaults({ className: "error" })
            $.notify( 
                    "please add blogs",
                    { position:"top center" }
                  )
        $(':checkbox').each(function() {
        this.checked = false;
        });
      }
    else{
      swal({
        title: "Are you sure?",
        text: "You will not be able to recover this blog!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel",
        closeOnConfirm: false,
        closeOnCancel: true
    },
    function(isConfirm){
      if (isConfirm) {
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
  else {
      $(':checkbox').each(function() {
         this.checked = false;
       });    
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


