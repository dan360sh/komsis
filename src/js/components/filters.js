"use strict"

$("body").on('click', '.filters__mobile-submit', function(){
	updateCatalog(event);
	showProductsPreloader();
	closeMobileFilters();
	catalogScrollTop();
})
$("body").on('click', '.filters__mobile-reset, #reset_filter', function(){
	let form = $(".filtering")[0];
	form.reset();
	updateCatalog(event, false, true)
	showProductsPreloader();
	closeMobileFilters();
	catalogScrollTop();
})

function openMobileFilters(){
	$(".filters, body, .nav-close").addClass('opened');
}

function closeMobileFilters(){
	$(".filters, body, .nav-close").removeClass('opened');
}

function catalogScrollTop(){
	$('html, body').animate({scrollTop: 0},500);
}

$('body').on('submit', 'form.filtering', catalogScrollTop);

$('body').on('click', '.filter-category[data-category]', function (event){
	const category = event.target.closest('.filter-category').dataset.category;
	const input = $('input[name="category"]');
	console.log('category', category);
	if (category){
		input.val(category);
	} else {
		input.val('');
	}
	updateCatalog(event);
})
window.openMobileFilters = openMobileFilters;
window.closeMobileFilters = closeMobileFilters;