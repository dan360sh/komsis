$('body').on('click', '.mobile-filters-trigger', function(e){
	e.preventDefault();
	if( !$("body").hasClass('loading-blocks') )
		openMobileFilters();
})