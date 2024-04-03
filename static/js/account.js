function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handlerAccountForm(event) {
    event.preventDefault()

    const form = event.currentTarget
    const data = $(form).serialize()
    clearForm(form)
    $.ajax({
		url: form.action,
		type: form.method, 
		dataType: 'json',
		data: data,
		success: function(response) {
            if (response.errors) {
                validateForm(form, response.fields)
                if(response.fields.hasOwnProperty('acceptance')){
                    const control = form.querySelector('[name="' + 'acceptance' + '"]')
                    const group = control.parentElement;
                    const error = group.querySelector('.invalid-feedback')
                    error.style.display = 'block';
                    error.style.width = '50%';
                    error.style.marginLeft = '50px';
                }
            } else {
                successForm(form, response.message);
                if(response.redirect)
                    window.location = response.redirect;
            }
		},
		error: function(error) {

        }
	});
}

document.querySelectorAll(".sn-account-data-form, .sn-account-password-form").forEach(form => {
    form.onsubmit = handlerAccountForm
})

function displayJuricalBlock(event){
    const target = event.target;
    const checked = target.checked;
    const juricalBlock = $('#jurical-block');
    if(checked){
        juricalBlock.animate({'maxHeight': 300}, 500);
        return;
    }
    juricalBlock.animate({'maxHeight': 0}, 500)
}

var juricalCheckbox = document.querySelector('#jurical');
if(juricalCheckbox){
    juricalCheckbox.addEventListener('change', displayJuricalBlock)
}

function submitAccountForm(event, beforeSendFunction, collectData, successCallBack){
    event.preventDefault();
    const target = event.target;

    var requestData = {}
    if(collectData){
        var form = target.closest('form');
        requestData = $(form).serialize();
    }
    const url = target.href;
    const csrftoken = getCookie('csrftoken');
    if(beforeSendFunction)
        beforeSendFunction(event);
    $.ajax({
		url: url,
		type: 'POST', 
		dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
		data: requestData,
		success: function(response) {
            if (response.errors) {
                displayAccountErrors(response)
                return;
            }

            if(!response.errors && successCallBack){
                successCallBack(response);
            }

            if (response.redirect){
                const orderId = target.dataset.order;
                if(orderId){
                    postForm(response.redirect, {order_id: orderId}, 'get');
                    return
                }
                window.location.href = response.redirect;
            }

		},
		error: function(error) {
            console.log(error);
            alert('Ошибка, перезагрузите страницу!');
        }
	});
}


function disableOrderControlButtons(event){
    const target = event.target;
    target.classList.add('btn-loading');
    target.removeAttribute('href');
    target.innerText = 'Секунду...';
    var orderControlButtons = document.querySelectorAll('.order-button');
    if(orderControlButtons){
        orderControlButtons.forEach(btn => {
            btn.classList.add('btn-loading');
            btn.removeAttribute('href');
        })
    }
}

function postForm(path, params, method) {
    method = method || 'post';

    var form = document.createElement('form');
    form.setAttribute('method', method);
    form.setAttribute('action', path);

    for (var key in params) {
        if (params.hasOwnProperty(key)) {
            var hiddenField = document.createElement('input');
            hiddenField.setAttribute('type', 'hidden');
            hiddenField.setAttribute('name', key);
            hiddenField.setAttribute('value', params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


var orderControlButtons = document.querySelectorAll('.order-button');
if(orderControlButtons){
    orderControlButtons.forEach(btn => {
        btn.addEventListener('click', (event) => {
            submitAccountForm(event, disableOrderControlButtons, false, null)
        })
    })
}

function replaceOrderList(response){
    var $orderList = $('.order-list');
    $orderList.replaceWith(response.template);
}

function displayAccountErrors(response){
    var errorBlock = document.querySelector('.error-message');
    errorBlock.innerText = response.message;
    errorBlock.style.display = 'block';
    response.fields.forEach(field => {
        document.querySelector(`input[name=${field}]`).classList.add('hasError')
    })
}

function removeAccountErrors(event){
    document.querySelectorAll('.hasError').forEach(element => {
        element.classList.remove('hasError')
    })
    document.querySelector('.error-message').style.display = 'none';
}

function resetForm(event){
    var form = event.target.closest('form')
    if(form)
        form.reset();
    removeAccountErrors(event)
}

function removeOrderItem(event){
    var target = event.target;
    var orderItemId = target.dataset.item;
    var url = target.dataset.href;
    var requestData = {
        'item_id': orderItemId
    }
    const csrftoken = getCookie('csrftoken');
    $.ajax({
		url: url,
		type: 'POST', 
		dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
		data: requestData,
		success: function(response) {
            $('.cart-total').text(response['total']);

            if(response.count > 0){
                removeOrderItemRow(target);
                return;
            }

            if(response.count < 1){
                removeOrder(target);
            }
		},
		error: function(error) {
            console.log(error);
            alert('Ошибка, перезагрузите страницу!');
        }
	});
}

function removeOrderItemRow(target){
    var itemId = target.dataset.item;
    var item = `.item-${itemId}`
    document.querySelector(item).remove();
}

function removeOrder(target){
    var url = target.dataset.orderDelete;
    const csrftoken = getCookie('csrftoken');

    $.ajax({
		url: url,
		type: 'POST', 
		dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
		data: {},
		success: function(response) {

            if (response.redirect){
                window.location.href = response.redirect;
            }

		},
		error: function(error) {
            console.log(error);
            alert('Ошибка, перезагрузите страницу!');
        }
	});
}

function toggleClickableTarget(event) {
    const CLICKABLE_EVENT_TARGET = "clickable"
    const CLICKABLE_TARGET = ".clickable-target"
    const ACTIVE_CLASS = "active"

    var target = event.target;
    if (!target.classList.contains(CLICKABLE_EVENT_TARGET)) {
        target = target.closest("." + CLICKABLE_EVENT_TARGET)
    }
    var toggleTargetId = target.getAttribute("data-target")
    var toggleTarget = document.querySelector(toggleTargetId)
    
    var isHidden = toggleTarget.classList.contains(ACTIVE_CLASS)
    if (isHidden) {
        toggleTarget.classList.remove(ACTIVE_CLASS)
    } else {
        toggleTarget.classList.add(ACTIVE_CLASS)
    }
}

var filterForm = document.querySelector('#filter-orders')
if(filterForm){
    filterForm.addEventListener('submit', function(event){
        submitAccountForm(event, removeAccountErrors, true, replaceOrderList)
    })
}

var resetOrdersFilter = document.querySelector('#reset_order_filter')
if(resetOrdersFilter){
    resetOrdersFilter.addEventListener('click', function(event){
        submitAccountForm(event, resetForm, false, replaceOrderList);
    })
}

document.querySelectorAll('.order-item-delete').forEach(btn => {
    btn.addEventListener('click', removeOrderItem)
})

document.querySelector(".clickable").addEventListener("click", function(event) {
    toggleClickableTarget(event)
})

// Скопировано с src/js/product-counter.js ибо он просто перестал работать
// Оно еще на моменте написания стало легаси
$('body').on('click', '.broken-counter__button', function (event) {
    var form = event.target.closest('form');
    var $input = $(form).find('.broken-change-count');
    var value = parseFloat($input.val().replace(",", "."));
    var step = parseFloat($input.attr('data-step').replace(",", "."));

    var isIncrementing = true;
    var isMinusButton = $(event.target).hasClass('product-counter__button_minus');
    var isValueValid = value >= step;

    if (isMinusButton && isValueValid)
        isIncrementing = false;

    value = isIncrementing ? value + step : value - step;

    var resultValue = validateCounterInput($input, value);

    changeOrderItemCount(form, resultValue)
    
});

function validateCounterInput(input, value, isIncrementing){
    // var val = parseFloat($(input).attr("value").replace(",", "."));
    var min = parseFloat($(input).attr('min').replace(",", "."));
    var max = parseFloat($(input).attr('max').replace(",", "."));
    var result = value;

    if (value > max){
        result = max;
        alertUser(input.closest('form'), 'max')
    }

    if (value < min){
        result = min;
        alertUser(input.closest('form'))
    }

    input.val(result);
    return result;
}

function alertUser(form, type){
    $('body').find('.product-counter__notification_max').hide();
    $('body').find('.product-counter__notification_min').hide();
    if (type) {
        form.find('.product-counter__notification_max').show();
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            form.find('.product-counter__notification_max').hide();
        }, 1000)
    } else {
        form.find('.product-counter__notification_min').show();
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            form.find('.product-counter__notification_min').hide();
        }, 1000)
    }

}

function changeOrderItemCount(form, value){
    var url = form.action;
    var requestData = new FormData(form)
    const csrftoken = getCookie('csrftoken');

    $.ajax({
		url: url,
        processData: false,
        contentType: false,
		type: 'POST', 
		dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
		data: requestData,
		success: function(response) {
            displayOrderTotalPrice(response, form)
		},
		error: function(error) {
            console.log(error);
            alert('Ошибка, перезагрузите страницу!');
        }
	});
}

function displayOrderTotalPrice(response, form){
    form = $(form)
    var tableRow = form.closest('.cart-table-row');
    

    tableRow.find('.cart-item-total').text(String(response['price']).toLocaleString('ru-RU'));
    $('.cart-total').text(String(response['total']).toLocaleString().replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 '));
}
