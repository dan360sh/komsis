
function allDisabled(content, disabled=true){
    content.querySelectorAll('input, select, textarea').forEach(item => {
        item.disabled = disabled
    })
}

function disabledTypePayment(value, disabled=true){
    const receiving = document.querySelector(`.payment_type input[value="${value}"]`);
    if (receiving) {
        receiving.checked = !disabled;
        receiving.disabled = disabled;
    }
    const other = document.querySelector(`.payment_type input:not([value="${value}"])`);
    if (other) {
        other.checked = disabled;
    }
}

/**
 *
 * @param {string} value name of input
 */
function selectPaymentType(value, isSelected = true) {
    const other = document.querySelectorAll(`.payment_type input:not([value="${value}"])`);
    other.forEach((elem) => elem.checked = false);
    const paymentTypeRadioButton = document.querySelector(`.payment_type input[value="${value}"]`);
    paymentTypeRadioButton.checked = isSelected;
}

function change_type_delivery(event){
    const target = event.currentTarget || event.target;
    const target_id = target.href.split('#')[1]
    //Если поле неактивно
    if (!target.classList.contains('active')){
        document.querySelectorAll('.delivery_types .tab-content .tab-pane').forEach(content => {
            allDisabled(content, target_id !== content.id);
        })
        // disabledTypePayment('receiving', target.dataset.typeShipping === '5');
        disableTypes(target);
    }
}


/**
 *  Метод блокировки типов оплаты, если был выбран другой тип доставки
*/
function disableTypes(target){
    var juricalCheckbox = document.querySelector('#face');
    let deliveryRadioButton = $(".dostavka");
    // let clickedRadioButton = target;

    if (juricalCheckbox?.checked) {
        // Если заказ от юр. лица, оставляем "Оплату при получении"
        // А также, блокируем оплату "По карте"
        disabledTypePayment('bank', true);
        setOtherTypesActive('bank');
        if (target.classList.contains("dostavka")) {
            disabledTypePayment('receiving', true);
            selectPaymentType('bill');
        }
        return;
    }
    // Если заказ не от юр лица, блокируем "Оплата при получении"
    disabledTypePayment('receiving', target.dataset.typeShipping === '5');
    setOtherTypesActive('receiving');
    // if (deliveryRadioButton.hasClass("active")) {
    //     disabledTypePayment('receiving');
    // }
    return
}

/**
* Метод блокировки способов оплаты, если был переключен чекбокс юр. лица
*/
function toggleTypeDelivery(target){
    var isJurical = target.checked;
    var receivingType = document.querySelector('.dostavka');
    // Если доставку отключат
    if (!receivingType)
        return

    if(isJurical && receivingType.classList.contains('active')){
        disabledTypePayment('bank', true);
        setOtherTypesActive('bank');
        disabledTypePayment('receiving', true);
        selectPaymentType('bill');
    }

    if(!isJurical && receivingType.classList.contains('active')){
        disabledTypePayment('receiving', true);
        setOtherTypesActive('receiving');
    }
}


/**
 * Метод включения всех вариантов оплаты, за исключением одного
 * @param {string} valueToExclude - value блока, который надо исключить
 * */
function setOtherTypesActive(valueToExclude){
    const other = document.querySelector(`.payment_type input:not([value="${valueToExclude}"])`);
    if (other) {
        other.disabled = false;
    }
}

function toggleVisible(value) {
    var targetBlock = document.querySelector('.panel-use');
    if(!targetBlock)
        return
    if(value == 'use')
        targetBlock.classList.add('active')
    if(value == 'collect')
        targetBlock.classList.remove('active');
}

function calculateDiscount(event) {
    var target = document.querySelector('#points-value');
    var value = target.value;
    var url = window.location.href;
    var requestData = {
        points: value,
        discount: 'use'
    }
    requestData = new URLSearchParams(requestData);
    requestData = requestData.toString()
    requestData = csrf(requestData)
    $.ajax({
        method: 'POST',
        url: url,
        dataType: 'json',
        data: requestData,
        success: function(response) {
            var hasErrors = false
            if(response.errors)
                hasErrors = true;

            displayResponse(response, hasErrors)
        }
    })
}

function displayDiscountResponse(target, value){
    toggleVisible(value);
    var requestData = {discount: value};
    if(value == "use"){
        var inputTarget = document.querySelector('#points-value');
        var pointsAmount = inputTarget.value;
        requestData["points"] = pointsAmount;
    }
    requestData = new URLSearchParams(requestData);
    requestData = requestData.toString()
    requestData = csrf(requestData)
    const url = window.location.href;
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: requestData,
        success: function (data) {
            var hasErrors = false;
            if(data.errors)
                hasErrors = true;
            displayResponse(data, hasErrors);
        },
        error: function () {
            console.log('error');
        }
    });
}

function displayResponse(response, hasErrors){
    var target = document.querySelector('.panel-response');
    target.classList.add('active');
    var messageBlock = target.querySelector('.title');
    messageBlock.classList.remove("error");
    var valueBlock = target.querySelector('.value');
    messageBlock.innerHTML = response.message;
    valueBlock.innerHTML = response.value;
    valueBlock.innerHTML = response.value ? response.value : "";
    if(hasErrors) {
        messageBlock.classList.add("error");
        messageBlock.innerHTML = response.error_message
        valueBlock.innerHTML = ""
    }

    if(!response.new_order_price)
        return;

    var newPrice = response.new_order_price;
    $('.order_total').text(String(newPrice).toLocaleString().replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ') + " руб.");

    if(response.extra_message){
        var extraMessageBlock = target.querySelector('.extra-title');
        extraMessageBlock.innerHTML = response.extra_message;
    }

    if(!response.new_products_prices)
        return;

    for(var key in response.new_products_prices){
        var targetPriceBlock = document.querySelector(`#order-item-price-${key}`)
        if(targetPriceBlock)
            targetPriceBlock.innerHTML = response.new_products_prices[key];
    }
}

function toggleBlock(event, targetBlock){

    if(!targetBlock)
        return

    var eventTarget = event.target;
    var eventValue = eventTarget.checked;
    if(eventValue){
        targetBlock.classList.remove('active');
        return
    }
    targetBlock.classList.add('active');
}

function togglePanel(event, targetBlock){

    if(!targetBlock)
        return

    var eventTarget = event.target;
    var eventValue = eventTarget.checked;
    if(eventValue){
        targetBlock.classList.add('active');
        return
    }
    targetBlock.classList.remove('active');
}

function toggleStashButton(target, stashButton){
    if(target.checked){
        stashButton.classList.remove('hidden');
        return;
    }

    stashButton.classList.add('hidden');
}

function toggleBonusSystemBlock(event){
    var target = document.querySelector(".bonus_type");
    $(target).prop('disabled', true);
    if(!target)
        return;

    var isDisplayed = event.target.checked;

    isDisplayed ? target.classList.remove("disabled") : target.classList.add("disabled")
}

document.querySelectorAll('.delivery_types .nav-link').forEach(link => {
    link.addEventListener('click', change_type_delivery);
});

document.querySelectorAll('.discount-btn').forEach(button => {
    button.addEventListener('click', function(event){
        const target = event.target;
        const value = target.value;
        displayDiscountResponse(target, value);
    })
})

function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
      textbox.addEventListener(event, function() {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
      });
    });
  }

var pointsInput = document.querySelector('#points-value')
if(pointsInput){
    pointsInput.addEventListener('input', function(event){
        calculateDiscount(event);
    });
    setInputFilter(pointsInput, function(value) {
        return /^\d*\.?\d*$/.test(value);
    });
}

var faceInput = document.querySelector('#face');
if(faceInput){
    faceInput.addEventListener('change', function(event){
        var faceTarget = document.querySelector('#discount-part');
        toggleBlock(event, faceTarget);
        var isJurical = event.target.checked;
        if(isJurical || cartHasOverflow()){
            disabledTypePayment('bank', true);
        }
        if(!isJurical && !cartHasOverflow()){
            setOtherTypesActive('');
        }
        toggleTypeDelivery(event.target);
    })
}

var stashOrderButton = document.querySelector('.order-stash');
if(stashOrderButton){
    $(stashOrderButton).on('click', function(event){
        var form = event.target.closest('form');
        var savedOrderId = form.dataset.order;
        extraRequestData = {
            order_id: savedOrderId ? savedOrderId : '',
            stash: true
        }
        sendCreateOrder(
            event,
            event.target.dataset.href,
            extraRequestData
        );
    });
}

var useBonusSystemCheckbox = document.querySelector(".form-part-title-checkbox");
if(useBonusSystemCheckbox){
    useBonusSystemCheckbox.addEventListener("click", function(e){
        toggleBonusSystemBlock(e);
    })
}
