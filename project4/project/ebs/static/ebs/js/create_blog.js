
$(document).ready(function() {    
    $('#createform').on('submit', function (e) {
        debugger;
        if ($('#id_attachments').val() && $('#id_attachments')[0].files[0].size>2048) {
            if ($("#id_attachments").next(".validation").length == 0){
                    $("#id_attachments").after("<div class='validation' style='color:red;margin-top: 10px;'>File size should be less than 15MB</div>"); // remove it
                    return false;
                }   
                     
                         
            }
           
        else if($('#id_image1').val() && $('#id_image1')[0].files[0].size>2048) {
            if ($("#id_image1").next(".validation").length == 0){
                    $("#id_image1").after("<div class='validation' style='color:red;margin-top: 10px;'>Please enter email address</div>"); // remove it
                    return false;     
                } 
                
                           
        }
        else if ($('#id_image2').val() && $('#id_image2')[0].files[0].size>2048) {
            if ($("#id_image2").next(".validation").length == 0){
                    $("#id_image2").parent().after("<div class='validation' style='color:red;margin-top:10px;'>Please enter email address</div>"); // remove it
                            
                        return false;                                 
                }
        }
        else {
            
            $("#id_attachments").next(".validation").remove();
            $("#id_image1").next(".validation").remove();
            $("#id_image2").next(".validation").remove();
            return true;     
        }
    });
});
