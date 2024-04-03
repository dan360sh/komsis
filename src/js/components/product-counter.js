$('body').on('click', '.product-counter__button', function (event) {
    var $input = $(this).parents('.product-counter').find('input');
    var val = parseFloat($input.attr("value").replace(",", "."));
    var step = parseFloat($input.data('step').replace(",", "."));

    if ($(this).hasClass('product-counter__button_minus') && val >= step) $input.attr("value", val - step);
    else $input.attr("value", val + step);

    $(this).parents('.product-counter').find('input').change();

    // setCoords($(this).parents('.product-counter'), event);
});

$('body').on('change', '.product-counter input', function () {
    var val = parseFloat($(this).attr("value").replace(",", "."));
    var min = parseFloat($(this).attr('min').replace(",", "."));
    var max = parseFloat($(this).attr('max').replace(",", "."));

    if (val > max)
        showTip($(this).parents('.product-counter'), 'max')

    if (val < min)
        showTip($(this).parents('.product-counter'))

    $(this).attr("value", (val > max) ? max : (val < min) ? min : val);
    updateFakeInput(this);
});

function updateFakeInput(target) {
    let parent = target.closest('.product-counter')
    // unit = parent.find('.product-counter__original-input').data('unit'),
    let val = parseInt((parent.querySelector('.product-counter__original-input').attributes.value.value).replace(",", "."));
    console.log(val)
    parent.querySelector('.product-counter__fake-input').innerText = `${val}`;
}

// function setCoords(target, event){
// 	$notification = target.find('.product-counter__notification');
// 	$notification.css({ 'left' : event.clientX, 'top' : event.clientY - $notification.outerHeight() })
// }

function showTip(target, type) {
    $('body').find('.product-counter__notification_max').hide();
    $('body').find('.product-counter__notification_min').hide();
    if (type) {
        target.find('.product-counter__notification_max').show();
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            target.find('.product-counter__notification_max').hide();
        }, 1000)
    } else {
        target.find('.product-counter__notification_min').show();
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            target.find('.product-counter__notification_min').hide();
        }, 1000)
    }
}

var timeout;