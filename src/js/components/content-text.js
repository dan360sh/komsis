function custom_resize(){

	$('.content img').each(function (i, e) {
		var w_post_img = $(e).width();
		var h_post_img = w_post_img * 32 / 87;
		$(e).css('height', h_post_img);
	});

	$('.gallery a').each(function(i, e) {
		var w_gallery_img = $(e).width();
		var h_gallery_img = w_gallery_img / 1.5;
		$(e).css('height', h_gallery_img);
	});

	$('.gallery .item-thumbnail, .certificates .certificate-thumbnail').each(function(i, e) {
		var w_gallery_img = $(e).width();
		var h_gallery_img = w_gallery_img / 1.5;
		$(e).css('height', h_gallery_img);
	});
}
custom_resize();
$(window).resize( function(){ custom_resize(); } );

/*     Обертка таблицы на текстовых    */
$('.content-text > table').prev('h3').addClass('for_table');
$(".content-text > table").wrap("<div class='table'><div class='table-responsive'></div></div>");
$('.content-text > .table').each(function(){
	$(this).prev('h3.for_table').prependTo($(this));
});
