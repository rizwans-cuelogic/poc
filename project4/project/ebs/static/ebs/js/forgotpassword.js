function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') 
    { 
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function() {
        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    $("#forgotform").submit(function (event){       
            var email1 = $('#email1').val();
            $.ajax({
            type: "POST",
            url: 'forgotpass/',
            data:JSON.stringify(
                {'email':email1}
            ),
            dataType:"JSON",
            processData: false,
            contentType: false,
            success: function(result){
                if(result['status']=='Error'){
                    $('#forgotmessage').notify(result['message']);
                    $('#forgotform')[0].reset();
                }
                else{
                    $.notify(result['message'],"success");
                  $('#forgotform')[0].reset();
                  $('#forgotform').bootstrapValidator('resetForm',true);
                  $('#forgotpassmodal').modal('toggle');
                  return false;                                    
                    return false;      
                }
              }
                
            });
          return false;
        });

      $('body').on('hidden.bs.modal', '.modal', function () {
                $('#forgotform')[0].reset();
         
      });

    if (window.location.href.indexOf("?uid=") > -1) {
        if ($('#hashval').attr('value')==""){
            $.notify("invalid link or token has been expired.");
            /*var data = {};
            data.putYour = "data here";
            History.pushState(data, document.title, window.location.host);*/
            // $('#recoverform')[0].reset();
            // $('#recoverform').bootstrapValidator('resetForm',true);
        } else{   
        $('#recoverformmodal').modal('show');
        }
    }
});



