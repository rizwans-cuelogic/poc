$(document).ready(function() {
        jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
        });
    $( "#createform" ).validate({
        rules: {
            attachments: {
                required: false,
                accept: "image/jpeg,image/png,application/msword,application/pdf,application/vnd.ms-excel"
            },

            image1: {
                required: false,
                accept: "image/jpeg,image/png,application/msword,application/pdf,application/vnd.ms-excel"
            },

            image2: {
                required: false,
                accept: "image/jpeg,image/png,application/msword,application/pdf,application/vnd.ms-excel"
            }

        }
    });       

        
    });
