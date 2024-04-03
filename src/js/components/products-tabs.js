$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	$($(e.target).attr('href')).find('.product-card-body').each(function(item, el) {
		cutProductText(el);
	})
})