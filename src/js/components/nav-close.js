$('body').on('click', '.nav-close', function(e){
	e.preventDefault();
	$(".filters, body, .nav-close").removeClass('opened');
})