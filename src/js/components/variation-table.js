$("body").on('change', '.variation-table .product-counter__original-input', function(){
	var sum = 0;
	console.log('sum', Number($(el).find('.variations-table-col_price.price-c').data('price')))
	$(".variation-table .variations-table-row").each(function(i, el){
		let count = Number($(el).find('.product-counter__fake-input').text());
		count = count ? count : 0;
		let price = Number($(el).find('.variations-table-col_price.price-c').data('price'));
		sum += count * price;
	});
	
	$(".variation-table .variations-table_price-value").text( sum.toLocaleString() );
});