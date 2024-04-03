$("body").on('click', '.mobile-search-trigger', function () {
	if (!$(this).hasClass("opened")) {
		if (!$("body").hasClass("opened")) 
			$("body").addClass('opened');
	}
	else
		$("body").removeClass('opened');

	$(this).toggleClass('opened');
	$(".mobile-menu, .mobile-menu-button, .mobile-menu .sub-menu.opened").removeClass('opened');
	$(".mobile-menu.no-scroll, .mobile-menu .sub-menu.no-scroll").removeClass('no-scroll');
	$(".mobile-search-wrapper").toggleClass('opened');
});