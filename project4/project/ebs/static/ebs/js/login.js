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

    $("#signinform").submit(function (event){
            var username = $('#susername').val();
            var password = $('#spassword').val();

            $.ajax({
            type: "POST",
            url: 'loginresult/',
            data: new FormData(this), 
            dataType:"JSON",
            processData: false,
            contentType: false,
            success: function(result){
                if(result['status']=='Error'){
                    $('#message').notify(result['message']);
                    $('#signinform')[0].reset();

                }
                else{
                     $('#signinmodal').modal('hide');
                     $('#logged-user').text("Welocome "+result['user']);
                     $('#dropdownMenu1').text("Welocome "+result['user']);
                     location.reload();   
                }
              }
                
            });
            
          return false;
        });

        $('#forgotpass').click(function(){
                $('#signinmodal').modal('hide');
                $('#forgotpassmodal').modal('show');

        });

        $('body').on('hidden.bs.modal', '.modal', function () {
                $('#signinform')[0].reset();
         
      });

    /*$('#mustread').on("mouseenter",'#title',function(){
        $(this).parent().find("#title-hd").css("color","#009688");
    }) ;*/    

});


