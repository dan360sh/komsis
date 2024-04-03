$('body').on('click', '.product-amount__button', function (event) {
	var $input = $(this).parents('.product-amount').find('input');
	var val = parseFloat($input.val().replace(",","."));

	if ($(this).hasClass('product-amount__button_minus')) $input.val(val - 1);
	else $input.val(val + 1);

	$(this).parents('.product-amount').find('input').change();
	
	setCoords($(this).parents('.product-amount'), event);
});

$('body').on('change', '.product-amount input', function () {
	var val = parseFloat($(this).val().replace(",","."));
	var min = parseFloat($(this).attr('min').replace(",","."));
	var max = parseFloat($(this).attr('max').replace(",","."));

	if(val > max)
		showTip( $(this).parents('.product-amount') , 'max')

	if(val < min)
		showTip( $(this).parents('.product-amount') )

	$(this).val((val > max) ? max : (val < min) ? min : val);
});

function setCoords(target, event){
	$notification = target.find('.product-amount__notification');
	$notification.css({ 'left' : event.clientX, 'top' : event.clientY - $notification.outerHeight() })
}

function showTip(target, type){
	if(type){
		target.find('.product-amount__notification_max').show();
		clearTimeout(timeout)
		timeout = setTimeout(()=>{
			target.find('.product-amount__notification_max').hide();
		}, 1000)
	}
	else{
		target.find('.product-amount__notification_min').show();
		clearTimeout(timeout)
		timeout = setTimeout(()=>{
			target.find('.product-amount__notification_min').hide();
		}, 1000)
	}
}

var timeout;