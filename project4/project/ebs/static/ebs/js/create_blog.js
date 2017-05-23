$(document).ready(function() {
    // function readURL(input) {
    //     if (input.files && input.files[0]) {
    //     var reader = new FileReader();
    //     reader.onload = function(e) {
    //         $('#previewHolder').attr('src', e.target.result);
    //     }
    //     reader.readAsDataURL(input.files[0]);
    //     }
    // } 
    // $("#id_attachments").change(function() {
    //     readURL(this);
    // });
    $( "#save" ).click(function() {
            $('#id_published').prop('required',true);
    });
    $( "#draft" ).click(function() {
            $('#id_published').prop('required',false);
    });
    $('#createform').on('submit', function (e) {
        var file_error_one = 0
        var file_error_four=0
        if ($('#id_attachments').val() && $('#id_attachments')[0].files[0].size>15728640) {
            if ($("#id_attachments").next(".validation").length == 0){
                    $("#id_attachments").after("<div class='validation' style='color:red;margin-top:5px;'>File Size Should Be Less Than 15MB</div>"); 
            }   
            $( "#id_attachments" ).focus();
            file_error_one = 1
        }
        input=$('#id_published').val();
        if (input !=""){
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
        if(!$('#id_published').is('[readonly]') && input_date.valueOf()==now1.valueOf()){
            if(hours<current_hours){
                if ($("#datetimepicker1").next(".validation").length == 0){
                     $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top: 5px;'>Please Select Future Date And Time</div>");
                }           
            file_error_four=1;
            $( "#id_published" ).focus();    
            }
            if(hours==current_hours){
                if(minutes<current_minutes){
                    if ($("#datetimepicker1").next(".validation").length == 0){
                $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top:5px;'>Please Select Future Date And Time</div>");
                }               
                file_error_four=1;
                $( "#id_published" ).focus();
                }
            }
        }
        else{
            if( !$('#id_published').is('[readonly]') && input_date<now ){    
                if ($("#datetimepicker1").next(".validation").length == 0){
                    $("#datetimepicker1").after("<div class='validation' style='color:red;margin-top:5px;'>Please Select Future Date And Time</div>");
            }
            file_error_four=1;
            $( "#id_published" ).focus();
            }
        }
        }
        if(file_error_one==0){
            $("#id_attachments").next(".validation").remove();
        }
        if(file_error_four==0){
            $("#datetimepicker1").next(".validation").remove();
        }
        if(file_error_one){
            $( "#id_attachments" ).focus();
        }
        if (!file_error_one && !file_error_four)
        {
            $("#id_attachments").next(".validation").remove();
            $("#datetimepicker1").next(".validation").remove();
            return true;     
        }
        return false;

    });

});
    

        
