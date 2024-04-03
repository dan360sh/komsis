/* Открытие другой модалки из модалки */
$(".open_other_modal").click(function (e) {
	e.preventDefault();
	$(this).parents(".custom_modal").toggleClass("opened");
	$($(this).data("target")).toggleClass("opened");
});

$("body").on('click', ".modal_trigger", function (e) {
	e.preventDefault();
	$modal = $(".custom_modal.opened");
	if( $modal.length ){
		resetModal($modal);
	}
	$("body, i.modal_bg").addClass('opened');
	$(".custom_modal.opened").toggleClass('opened');
	$( $(this).data("target") ).addClass("opened");

	
});


$("body").on('click', ".modal_close, i.modal_bg", function(e){
	e.preventDefault();
	if( !$(".mobile-menu").hasClass('opened') ){
		$("body").removeClass('opened');
	}
	resetModal( $(".custom_modal.opened") );
	$("i.modal_bg, .custom_modal.opened").removeClass('opened');
})

function resetModal(modal){
	let form = modal.find('form');
	if(form.length){
		modal.find('form')[0].reset();
		modal.find('form').removeClass('success load')
		modal.find('form').find('.form-control').removeClass('is-valid is-invalid')
	}
}