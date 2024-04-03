$("body").on('click', '.sidebar-helper', function(){
	$("body, i.modal_bg").addClass('opened');
	$($(this).attr('href')).addClass('opened');
});