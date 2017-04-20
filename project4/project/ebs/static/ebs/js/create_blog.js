
$(document).ready(function() {    
    $('#createform').on('submit', function (e) {
        debugger;
        var file_error_one = 0
        var file_error_two = 0
        var file_error_three = 0
        if ($('#id_attachments').val() && $('#id_attachments')[0].files[0].size>2048) {
            if ($("#id_attachments").next(".validation").length == 0){
                    $("#id_attachments").after("<div class='validation' style='color:red;margin-top: 10px;'>File size should be less than 15MB</div>"); // remove it
            }   

            file_error_one = 1
        }

        if($('#id_image1').val() && $('#id_image1')[0].files[0].size>2048) {
            if ($("#id_image1").next(".validation").length == 0){
                $("#id_image1").after("<div class='validation' style='color:red;margin-top: 10px;'>File size should be less than 15MB</div>"); // remove it
            } 
            file_error_two = 1  
        } 

        if ($('#id_image2').val() && $('#id_image2')[0].files[0].size>2048) {
            if ($("#id_image2").next(".validation").length == 0){
                $("#id_image2").after("<div class='validation' style='color:red;margin-top:10px;'>File size should be less than 15MB</div>"); // remove it
            }
            file_error_three = 1
        }
        if(file_error_one==0){
            $("#id_attachments").next(".validation").remove();
        }
        if(file_error_two==0){
            $("#id_image1").next(".validation").remove();
        }
        if(file_error_three==0){
            $("#id_image2").next(".validation").remove();
        }
        
        if (!file_error_one && !file_error_two && !file_error_three)
        {
            $("#id_image1").next(".validation").remove();
            $("#id_attachments").next(".validation").remove();
            $("#id_image2").next(".validation").remove();
            return true;     
        }
        return false;

    });
});
