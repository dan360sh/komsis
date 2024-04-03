$("body").on('click', '.sort-parameters__layout-types button', function(){
	$(".sort-parameters__layout-types button.active").removeClass("active");
	$(this).addClass("active");
});