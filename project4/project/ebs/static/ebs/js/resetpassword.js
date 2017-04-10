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
    $('#recoverform').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
        password: {
           validators:{ 
            notEmpty: {
                        message: 'Please Enter password'
                    },
            stringLength: {
                     min: 8,
                     max: 16,
                     message:'password must be more than 8 character and less than 16 character long'
                
             },

             regexp:{    
                     regexp:/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[a-zA-z\d]+$/,
                     message:"Password must contain atleast 1 number and 1 uppercase letter 1 lowercase letter"
             },
            
             identical:{
                 field:"confirmpassword",
                 message:"Confirm your password below"
                 }
             }
         },

       confirmpassword: {
            validators: {
                    notEmpty: {
                        message: 'Please Enter password'
                    },
                    identical:{
                         field:"password",
                         message:"The password and confirm are not same"
                     }
                 }
             }
        }
})

    .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
                $('#recoverform').data('bootstrapValidator').resetForm();

            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serialize(), function(result) {
                console.log(result);
            }, 'json');
        });

    $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    $("#recoverform").submit(function (event){
            event.preventDefault();
            var password1 = $('#password1').val();
            var password2=$('#password2').val();
            var url=window.location.href;
            var hash=url.split('=');
            var home=url.split('/')
            var hash1=hash[1];
            $.ajax({
            type: "POST",
            url: 'recover_password/',
            data:JSON.stringify(
                {'password':password1,
                 'hash':hash1}
            ),
            dataType:"JSON",
            processData: false,
            contentType: false,
            success: function(result){
                if(result['status']=='Error'){
                    $('#recovermessage').notify(result['message']);
              
                }
                else if(result['status']=='success'){ 
                    $.notify(
                        "password updated successfully","success"    
                    );     
                    $('#recoverform')[0].reset();
                    $('#recoverform').bootstrapValidator('resetForm',true);
                    $('#recoverformmodal').modal('hide');
                    setInterval(function(){ 
                        window.location.replace('/');

                     }, 5000);
                    /*var data = {};
                    data.putYour = "data here";
                    History.pushState(data, document.title, window.location.host);
                    */

                    return false;
                }
              }
                
            });
          return false;
        });



});