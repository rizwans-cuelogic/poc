$(document).ready(function(){
	$('.blog-img a').attr('target', '_blank');
	$('.blog-thumbnail a').attr('target', '_blank');
	$('.blog-attachments a').attr('target', '_blank');
	$('.blog-content > p > img').addClass('img-responsive');
	$( "hr").last().remove();
	$('[data-toggle="tooltip"]').tooltip();
	$('.tags > span:not(:last-child)').each(function () {
        $(this).append(',');
    });
})