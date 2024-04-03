if (!Array.prototype.forEach) {
    Array.prototype.forEach = function (callback, thisArg) {
        var T, k;
        if (this == null) {
            throw new TypeError(' this is null or not defined');
        }
        var O = Object(this);
        var len = O.length >>> 0;
        if (typeof callback !== 'function') {
            throw new TypeError(callback + ' is not a function');
        }
        if (arguments.length > 1) {
            T = thisArg;
        }
        k = 0;
        while (k < len) {
            var kValue;
            if (k in O) {
                kValue = O[k];
                callback.call(T, kValue, k, O);
            }
            k++;
        }
    };
}


function removeProduct(product) {
    product.classList.add('removed')
}

function restoreProduct(product) {
    product.classList.remove('removed')
}

function productCartAdded(product) {
    var button = product.querySelector(".add-to-cart")
    button.classList.add("added")
    button.disabled = true
    button.dataset.text = button.innerText
    button.innerHTML = "Добавлено"
    setTimeout(function() {
        button.classList.remove("added")
        button.disabled = false
        button.innerHTML = button.dataset.text
        button.dataset.text = ""
    }, 3000)
}

function cutProductText(item){
	$(item).dotdotdot();
}

window.removeProduct = removeProduct
window.restoreProduct = restoreProduct
window.productCartAdded = productCartAdded
window.cutProductText = cutProductText

$(".product-card-remove").each(function(index, button) {
    var product = button.closest(".product-card")
    button.addEventListener("click", function(event) {removeProduct(product)})
})

$(".product-card-restore").each(function(index, button) {
    var product = button.closest(".product-card")
    button.addEventListener("click", function(event) {restoreProduct(product)})
})

$(".product-card-body").each(function(index, item) {
    cutProductText(item);
})
