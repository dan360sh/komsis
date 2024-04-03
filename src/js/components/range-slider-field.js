import $ from "jquery";

class RangeSliderField {
	constructor(container) {
		this.container = $(container);
		this.slider = this.container.find('.range-slider-field__slider');
		this.inputs = this.container.find('.range-slider-field__inputs input');
		this.minPrice = this.container.find('.range-slider-field__inputs .range-slider-field__min-price');
		this.maxPrice = this.container.find('.range-slider-field__inputs .range-slider-field__max-price');

		this.init();
	};

	initSlider(){
		let self = this;

		this.minPrice.val( String(this.slider.data("from")).replace(/\B(?=(\d{3})+(?!\d))/g, " ") );
		this.maxPrice.val( String(this.slider.data("to")).replace(/\B(?=(\d{3})+(?!\d))/g, " ") );


		this.slider.ionRangeSlider();

		this.slider.on("change", function (event) {
			let $this = $(this), _thisMin, _thisMax,
				value = $this.prop("value").split(";");

			_thisMin = value[0].replace(/ /g,"");
			_thisMin = _thisMin.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
			_thisMax = value[1].replace(/ /g,"");
			_thisMax = _thisMax.replace(/\B(?=(\d{3})+(?!\d))/g, " ");

			self.minPrice.val(_thisMin);
			self.maxPrice.val(_thisMax);
			filterShowCounter(this, -4);
		});
	}

	init() {
		this.initSlider();
	}
}

$(".range-slider-field").each(function(elem) {
    new RangeSliderField( elem );
});



$("body").on('change', '.range-slider-field__inputs input', function () {
	filterShowCounter(this, -4);
	let parent = $(this).parents(".range-slider-field");
	let $range_data = parent.find('.range-slider-field__slider').data("ionRangeSlider");

	$range_data.update({
		from: parent.find(".range-slider-field__min-price").val().replace(' ', ''),
		to: parent.find(".range-slider-field__max-price").val().replace(' ', '')
	});
});


$('body').on('input', '.range-slider-field__min-price', capacity)
$('body').on('input', '.range-slider-field__max-price', capacity)

function capacity() {
    this.value = this.value.replace(/[^\d]/g, '');
	this.value = this.value.replace(/ /g,"");
	this.value = this.value.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

window.RangeSliderField = RangeSliderField