$(document).ready(function() {
    $('#myform').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                validators: {
                        stringLength: {
                        min: 6,
                        message:'Username must be atleast 6 character long'
                    },
                        notEmpty: {
                        message: 'Please provide username'
                    }
                }
            },
            
            email: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your email address'
                    },
                    emailAddress: {
                        message: 'Please provide a valid email address'
                    }
                }
            },
        
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
                 field:"password1",
                 message:"Confirm your password below"
                 }
             }
         },

       password1: {
            validators: {
                    notEmpty: {
                        message: 'Please Enter password'
                    },
                    identical:{
                         field:"password",
                         message:"The password and confirm are not same"
                     }
                 }
             },

        orglogo: {
            validators: {
                notEmpty: {
                        message: 'Please provide logo'
                    },


                file: {
                    extension: "jpg,png",
                    type: "image/jpeg,image/png",
                    message: 'Please choose a image file(jpg,png)'
                }
            }
        },

        orgname: {
            validators: {
                notEmpty: {
                        message: 'Please provide company name'
                    }
                }
            }
        }
})

    .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
                $('#myform').data('bootstrapValidator').resetForm();

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

   $("#myform").submit(function (event){
           var $form=$(this);
           console.log($form);
           console.log($(this).serialize());
           $.ajax({
              type: "POST",
              url: 'regresult/',
              data: new FormData(this),  
              dataType:"JSON",
              processData: false,
              contentType: false,
              success: function(result){
                if(result['status']=='Error'){
                    $('#validator_message').notify(result['message']);
                }
                else{
                  $.notify(result['message'],"success");
		  $('#myform')[0].reset();
                  $('#myform').bootstrapValidator('resetForm',true);
                }
            }
            });
          return false;
        });

      $('body').on('hidden.bs.modal', '.modal', function () {
        $('#myform')[0].reset();
	$('#myform').bootstrapValidator('resetForm',true);
      });
});


/*
    $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data, status) {
            
                var $feedback=$('<div>').html(data).find("#message-1");
                $form.prepend($feedback);
            }
        });
    return false;
    });




    */
    /*

    $("#myform").submit(function(e) {
        
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data,status) {
                

            },
    });
    event.preventDefault();
});

});
*/
