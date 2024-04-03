function open(event){
	const search = document.querySelectorAll('.search-form')[1];
	search.classList.add('active');
}

function close(event){

	const search = document.querySelectorAll('.search-form')[1];
	search.classList.remove('active');
}

function check(event){
	const target = event.target.closest('.search-form');
	console.log(target);
	if (!target){
		close()
		window.removeEventListener('click', check);
	}

}

$('body').on('focusin', '.search-form__label input', function (event) {
	// $('.search-form__ajax-search ul').stop().slideDown();
	hideText( $(this).closest('.search-form') );
	open();
	window.addEventListener('click', check)
});

$('body').on('mouseleave', '.search-form', function (event) {
	// $('.search-form__ajax-search ul').stop().slideUp();

	showText( $(this).closest('.search-form') );
});

$('body').on('click', '.search-form__label-text', function(event) {
	hideText( $(this).closest('.search-form') );
	$(this).closest('.search-form').find('input').focus();
	// $('.search-form__ajax-search ul').slideDown();
});

function showText(searchForm){
	if( $(searchForm).find('input').val().length < 1 ){
		$(searchForm).find('.search-form__label-text').css('display', 'flex');
	}
		
}
function hideText(searchForm){
	$(searchForm).find('.search-form__label-text').css('display', 'none');
}