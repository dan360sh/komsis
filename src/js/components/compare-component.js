class CompareScroller {
	constructor(scroller) {
		this.selector = scroller;
		this.rows = [];
		this.productScroller;

		this.init();
	};
	
	setRowWidth() {
		var amount = $(".product-card").length;
		var blockWidth = $(".product-card").outerWidth();
		var	blockMargin = parseInt($(".product-card").css('margin-left')) * 2;
		$(".compare-table__fixed-container").width(amount * (blockWidth + blockMargin + 1) ) // 1 – погрешность
	};

	showDifferentParams(isChecked) {
		if(isChecked){
			var $table = $(".compare-table");
			
			$table.find('.compare-table__row').each((ind1, row) => {
				var $items = $(row).find('.compare-table__row-item');
				var text = $items[0].innerHTML.trim();
				var hasUnique = false;
				
				$items.each(function(ind2, item){
					if(item.innerHTML.trim() !== text)
						hasUnique = true;
				});
	
				if(!hasUnique){
					var $item = $(row).find('.compare-table__row-wrapper');
	
					$(row).addClass('not-unique');
					for(let arrayRow of this.rows){
						if( $item[0] === $(arrayRow.getElements().target).closest('.compare-table__row-wrapper')[0] ){
							arrayRow.sleep();
						}
					}
				}
			})
	
			$table.each(function(i, el){
				if( !$(el).find('.compare-table__row').not('.not-unique').length )
					$(el).addClass('empty');
	
			});
		}
		else{
			$('.compare-table.empty').removeClass('empty');
			$('.compare-table__row.not-unique').each((i, el) => {
				var $item = $(el).find('.compare-table__row-wrapper');
	
				$(el).removeClass('not-unique');
				for(let arrayRow of this.rows){
					if( $item[0] === $(arrayRow.getElements().target).closest('.compare-table__row-wrapper')[0] ){
						arrayRow.scroll([this.productScroller.scroll().x.position, 0], 0);
						arrayRow.update();
					}
				}
				
			});
			
		}
	};

	initProductScroller() {
		let self = this;
		
       	self.productScroller = OverlayScrollbars(document.querySelector('.compare-component__product-scroller'), {
			autoUpdate: true,
			callbacks: {
				onScroll: function(event){
					for(row in self.rows){
						self.rows[row].scroll([ event.target.scrollLeft, 0 ], 0);
					}
				},
				onInitialized: function(){
					self.setRowWidth();
				},
				onUpdated: function(){
					self.setRowWidth();
				}
			}
		});
	}

	initCompareRows() {
		let self = this;
		$('.compare-table__row-wrapper').each((index, element) => {
			self.rows.push(
				OverlayScrollbars($(element), {
					autoUpdate: true,
					scrollbars: {
						visibility: 'hidden'
					},
					callbacks: {
						onScroll: function(event){
							self.productScroller.scroll([ event.target.scrollLeft, 0 ], 0);
							for(row in self.rows){
								self.rows[row].scroll([ event.target.scrollLeft, 0 ], 0);
							}
						}
					}
				})
			)
		});
	}

	mobileScroll(elem) {
		if($(window).width() < 991){
			if(window.pageYOffset > elem.offset().top + elem.find('.compare-component__controlls').outerHeight() - 10 ){
				$('.compare-component').addClass('scrolled');
			}
			else{
				$('.compare-component').removeClass('scrolled');
			}
		}
		else{
			$('.compare-component').removeClass('scrolled');
		}
	}


    init() {
		this.initProductScroller();
		this.initCompareRows();
		
    }
}

var scroller = new CompareScroller('.compare-component');






$(window).scroll(function(){
	let elem = $('.compare-component');
	if(elem.length) scroller.mobileScroll(elem);
	
});

$("body").on("change", ".show-different .toggle-button__input", function(){
	scroller.showDifferentParams( $(this)[0].checked );
});

$('body').on('hidden.bs.collapse', '.compare-component .compare-table__body', function (event) {
	$collapseElement = $(this);
	
	for(let row of scroller.rows){
		if( $collapseElement[0] === $(row.getElements().target).closest('.compare-table__body')[0] ){
			row.sleep();
		}
	}
});

$('body').on('shown.bs.collapse', '.compare-component .compare-table__body', function (event) {
	$collapseElement = $(this);

	for(let row of scroller.rows){
		if( $collapseElement[0] === $(row.getElements().target).closest('.compare-table__body')[0] ){
			row.scroll([scroller.productScroller.scroll().x.position, 0], 0);
			row.update();
		}
	}
})



