import anime from "animejs"

import { parseHTML } from "../utils";

function blockedCartItem(item) {
    item.style.pointerEvents = "none"
}

function deleteCartItem(item) {
    anime({
        targets: item,
        opacity: [1, 0],
        height: [item.clientHeight, 0],
        duration: 400,
        easing: "easeOutQuart",
        complete: function() {
            item.remove()
        }
    })
}

function clearCart(markup) {
    const container = document.querySelector(".cart-container")
    anime({
        targets: container,
        opacity: [1, 0],
        duration: 400,
        easing: "easeOutQuart",
        complete: function() {
            container.innerHTML = markup
            anime({
                targets: container,
                opacity: [0, 1],
                duration: 400,
                easing: "easeOutQuart"
            })
        }
    })
}

window.blockedCartItem = blockedCartItem
window.deleteCartItem = deleteCartItem
window.clearCart = clearCart
