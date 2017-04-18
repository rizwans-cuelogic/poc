$(document).ready(function() {
    $('#createform').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            attachements: {
                validators: {
                    notEmpty: {
                        message: 'Please select an file'
                    },
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxSize: 2097152,   // 2048 * 1024
                        message: 'you can select jpeg,png,doc,pdf,xls file'
                    }
                }
            }
            image1: {
                validators: {
                    notEmpty: {
                        message: 'Please select an file'
                    },
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxSize: 2097152,   // 2048 * 1024
                        message: 'you can select jpeg,png,doc,pdf,xls file'
                    }
                }
            }
            image2: {
                validators: {
                    notEmpty: {
                        message: 'Please select an file'
                    },
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxSize: 2097152,   // 2048 * 1024
                        message: 'you can select jpeg,png,doc,pdf,xls file'
                    }
                }
            }



        }
    });
});