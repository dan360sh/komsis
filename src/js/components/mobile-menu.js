const button = document.querySelector(".mobile-menu-button")
const opened = false

button.onclick = function(event) {
    if (button.classList.contains("opened")) {
		button.classList.remove("opened")
		document.querySelector("body").classList.remove('opened');
		$(".mobile-menu *.opened").removeClass('opened');
    } else {
		button.classList.add("opened")
		document.querySelector("body").classList.add('opened');
    }

    $(".mobile-menu").toggleClass('opened');
    $(".mobile-search-wrapper, .mobile-search-trigger").removeClass('opened');

    if ($(this).hasClass("opened")){
        $(".mobile-menu .sub-menu.opened").removeClass('opened');
        $(".mobile-menu.no-scroll, .mobile-menu .sub-menu.no-scroll").removeClass('no-scroll');
    }
}


/*	Открытие мобильного подменю
---------------------------------------*/
$("body").on('click', '.mobile-menu .has-children > a', function(e){
	e.preventDefault();
	$(this).closest(".sub-menu, .mobile-menu").toggleClass('no-scroll');
	$(this).closest(".has-children").find("> .sub-menu").toggleClass('opened');
});

/*	Закрытие мобильного подменю
---------------------------------------*/
$("body").on('click', '.mobile-menu .step_back', function (e) {
	e.preventDefault();
	$(this).closest(".sub-menu.no-scroll, .mobile-menu.no-scroll").toggleClass('no-scroll');
	$(this).closest(".sub-menu.opened").toggleClass('opened');
});