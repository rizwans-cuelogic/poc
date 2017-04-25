
$(document).ready(function() {  
    $('#createform').on('submit', function (e) {
        var file_error_one = 0
        var file_error_two = 0
        var file_error_three = 0
    var file_error_four=0
    var file_error_five=0
    input=$('#id_published').val();
        input=input.split(" ");
        time=input[1].split(":");
    hours=time[0];
    minutes=time[1];
        input_date=input[0].split("-");
        input_date=new Date(input_date[0],input_date[1]-1,input_date[2]);
        now=new Date();
    now1=new Date();
    now1.setHours(0,0,0,0)
    getime=now.toLocaleString('en-GB');
    current_hours=now.getHours();
    current_minutes=now.getMinutes();
    if(input_date.valueOf()==now1.valueOf()){
        if(hours<current_hours){
            if ($("#datetimepicker1").next(".validation").length == 0){
                 $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top: 5px;'>Invalid Date And Time</div>");
        }           
            file_error_four=1;
            $( "#id_published" ).focus();    
        }
        if(hours==current_hours){
            if(minutes<current_minutes){
            if ($("#datetimepicker1").next(".validation").length == 0){
            $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top:5px;'>Invalid Date And Time</div>");
            }               
                file_error_four=1;
                $( "#id_published" ).focus();
            }

        }
    }
    else{
        if(input_date<now ){    
            if ($("#datetimepicker1").next(".validation").length == 0){
                 $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top:5px;'>Invalid Date And Time</div>");
                 
        }
            file_error_four=1;
            $( "#id_published" ).focus();
    }
    }
      
       if ($('#id_attachments').val() && $('#id_attachments')[0].files[0].size>15728640) {
            if ($("#id_attachments").next(".validation").length == 0){
                    $("#id_attachments").after("<div class='validation' style='color:red;margin-top:5px;'>File size should be less than 15MB</div>"); 
            }   
            $( "#id_attachments" ).focus();
            file_error_one = 1
        }

        if($('#id_image1').val() && $('#id_image1')[0].files[0].size>15728640) {
            if ($("#id_image1").next(".validation").length == 0){
                $("#id_image1").after("<div class='validation' style='color:red;margin-top:5px;'>File size should be less than 15MB</div>"); 
            } 
            file_error_two = 1 
            $( "#id_image1" ).focus();
        } 

        if ($('#id_image2').val() && $('#id_image2')[0].files[0].size>15728640) {
            if ($("#id_image2").next(".validation").length == 0){
                $("#id_image2").after("<div class='validation' style='color:red;margin-top:5px;'>File size should be less than 15MB</div>");
            }
            file_error_three = 1
            $( "#id_image2" ).focus();
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
        if(file_error_four==0){
            $("#datetimepicker1").next(".validation").remove();
        }

        if(file_error_one && file_error_two || file_error_one && file_error_two && file_error_three ){
            $( "#id_attachments" ).focus();
        }
        
        if(!file_error_one && file_error_two && file_error_three){
            $( "#id_image1" ).focus()   
        }    

       if (!file_error_one && !file_error_two && !file_error_three && !file_error_four)
        {
            $("#id_image1").next(".validation").remove();
            $("#id_attachments").next(".validation").remove();
            $("#id_image2").next(".validation").remove();
        $("#datetimepicker1").next(".validation").remove();
            return true;     
        }
        return false;

    });

});
    

        
