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
                    $.notify(result['message']);
                }
                else{
                     $('#signinmodal').modal('hide');
                     $('#logged-user').text("Welocome "+result['user']);
                     location.reload();   
                }
              }
                
            });
          return false;
        }); 

});


/*data:{
                username: username,
                password: password

            },*/