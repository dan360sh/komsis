$("body").on('click', '.select-tabs__list-trigger', function(){
	$(this).toggleClass('focused');
	$(this).closest('.select-tabs').find('.select-tabs__list').stop(false).slideToggle();
});

$('.select-tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	$(".contacts-block__map-container.active").removeClass('active');
	$( $(this).data('map') ).addClass('active');

	$(this).closest('.select-tabs').find('.select-tabs__list a.active').removeClass('active');
	$(this).addClass('active');

	$(this).closest('.select-tabs').find('.select-tabs__list-trigger').text( $(this).text() );
})

$(document).on('focusout', ".select-tabs__list-trigger", function () {
	$(this).closest('.select-tabs').find('.select-tabs__list').slideUp();
	$(this).removeClass('focused');
});


