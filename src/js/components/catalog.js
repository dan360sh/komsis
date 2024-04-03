import "overlayscrollbars"

function showProductsPreloader(){
	$("body").addClass('loading-blocks');
}

function hideProductsPreloader(){
	$("body").removeClass('loading-blocks');
}

function replaceCatalogData(event, data, more) {
	more = more || false;
	$('.filter-counter').fadeOut(200);  
	
	if(data['products'].length != 0) {
		var html_products = data['products'];
		if (more)
			$('.sn-products-container').append(html_products);
		else
            $('.sn-products-container').html(html_products);
        $('.paginationBlock').html(data['pagination']);
        
		$('.filterBlock').replaceWith(data['template_filters']);
		
		// $('.filter-block__scroll-content').overlayScrollbars({
		// 	overflowBehavior: {
		// 		x: "hidden" 
		// 	}
		// });

		OverlayScrollbars(document.querySelectorAll(".filter-block__scroll-content"), {
			autoUpdate: true,
			overflowBehavior: {
				x: "hidden",
				y: "scroll"
			}
		})

		// Init range slider
		$(".range-slider-field").each(function(index, elem) {
			new RangeSliderField( elem );
		});
	} 
	else {	
		$('.paginationBlock').html("");
		$('.sn-products-container').html('<div class="products-container">\
            <div class="row sn-products-container">\
                <div class="col-12">\
                <p class="empty-category__title">По данному запросу товаров не найдено.</p>\
                </div>\
            	</div>\
    		</div>');
	}


	// lazy load
	// $('img.lazy').each(function (index, el) {
	// 	$(el).parent().addClass('lazy_wrap');
	// 	$(el).lazy({
	// 		afterLoad: function (element) {
	// 			$(el).parent().removeClass('lazy_wrap');
	// 		}
	// 	});
	// });

	$(".product-card-body").each(function(index, item) {
		cutProductText(item);
	})

	sort_filter();

	toggleCatalogPreloader();
	hideProductsPreloader();
}

function toggleCatalogPreloader(){
	$(".products-container").toggleClass('loading');
}

window.showProductsPreloader = showProductsPreloader;
window.hideProductsPreloader = hideProductsPreloader;
window.replaceCatalogData = replaceCatalogData;
window.toggleCatalogPreloader = toggleCatalogPreloader;