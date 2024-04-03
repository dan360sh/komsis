// $('.filters input[type="checkbox"]').each(function (index, el) {
// 	$(el).click(function (event) {
// 		var current = $('.filters input[type="checkbox"]:checked').length;

// 		if (current > 0) {

// 			showFilterCounter();
// 			clearTimeout(window.labelTimeout);
// 			window.labelTimeout = setTimeout(function () {
// 				hideFilterCounter();
// 			}, 5000);
// 		} else {

// 			hideFilterCounter();
// 		}
// 		if ($(el).prop('checked')) {
// 			$(el).next('label').find('span').addClass('active');
// 		} else {
// 			$(el).next('label').find('span').removeClass('active');
// 		}
// 	});
// });

// $('.filters label').each(function (index, el) {
// 	$(el).click(function (event) {
// 		var position = $(el).position();
// 		var $filters = $(el).parents(".filters");
// 		filterShowCounter(this);
// 	});
// });

$('body').on('click', '.filters label', function(){
	filterShowCounter(this);
});

$('body').on('hide.bs.collapse', '.filter>div', function () {
	hideFilterCounter();
});

$('body').on('click', '.filter-counter', function (e) {
	$('body,html').animate({
		scrollTop: 0
	}, 400);
});

function filterShowCounter(this_ob, offset = -8) {
	var $filters = $(this_ob).parents(".filters");
	$('.filter-counter').css('top', $(this_ob).offset().top - $filters.offset().top + offset);
	showFilterCounter();
	clearTimeout(window.labelTimeout);
	window.labelTimeout = setTimeout(function () {
		hideFilterCounter();
	}, 5000);
}

function hideFilterCounter(){
	$('.filter-counter').fadeOut(200);
}

function showFilterCounter(){
	$('.filter-counter').fadeIn(200);
}

window.filterShowCounter = filterShowCounter;
window.hideFilterCounter = hideFilterCounter;
window.showFilterCounter = showFilterCounter;