$('.product-slider__container').slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	infinite: false,
	arrows: false,
	asNavFor: '.product-slider__carousel',
	responsive: [
		{
			breakpoint: 768,
			settings: {
				dots: true
			}
		}
	]
});
$('.product-slider__carousel').slick({
	slidesToShow: 4,
	asNavFor: '.product-slider__container',
	arrows: false,
	focusOnSelect: true,
});