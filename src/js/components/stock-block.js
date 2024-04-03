$('.index-row_stock .wrapper').slick({
	infinite: false,
	centerMode: false,
	centerPadding: '0px',
	slidesToShow: 2,
	responsive: [
		{
			breakpoint: 992,
			settings: {
				arrows: false,
				centerMode: true,
				centerPadding: '15%',
				adaptiveHeight: true,
				slidesToShow: 1
			}
		}
	]
});