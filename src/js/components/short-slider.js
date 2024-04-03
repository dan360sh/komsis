$(".short-slider").slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	infinite: true,
	arrows: true,
	dots: true,
	prevArrow: '<span class="short-slider__arrow short-slider__arrow_prev"><svg role="img" width="9" height="11"><use xlink:href="/static/images/sprite.svg#slider-arr"></use></svg></span>',
	nextArrow: '<span class="short-slider__arrow short-slider__arrow_next"><svg role="img" width="9" height="11"><use xlink:href="/static/images/sprite.svg#slider-arr"></use></svg></span>',
})