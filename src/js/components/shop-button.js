class ShopButton {
    constructor(button) {
        this.button = button
        this.counter = this.button.querySelector(".shop-button__count")
        this.counterMob = document.querySelector(".shop-button__count-mob")
        this.initState()
    }

    changeCount(num) {
        this.counter.innerHTML = parseInt(num)
        this.counterMob.innerHTML = parseInt(num)
        this.initState()
    }

    initState() {
            if (this.counter.innerText === "" || parseInt(this.counter.innerText) <= 0) {
                this.counter.classList.remove("filled")
            } else {
                this.counter.classList.add("filled")
            }
        }   
}


let cardButton = null
let compareButton = null
let favoritesButton = null

function initShopButtons() {
    cardButton = new ShopButton(document.querySelector(".cart-button"))
    // compareButton = new ShopButton(document.querySelector(".compare-button"))
    favoritesButton = new ShopButton(document.querySelector(".favorites-button"))
}
initShopButtons()


/////////
// API //
/////////

function changeCartCount(num) {
    cardButton.changeCount(num)
    return cardButton
}

function changeCompareCount(num) {
    compareButton.changeCount(num)
    return compareButton
}

function changeFavoritesCount(num) {
    favoritesButton.changeCount(num)
    return favoritesButton
}

// Variables
window.cardButton = cardButton
window.compareButton = compareButton
window.favoritesButton = favoritesButton

// Functions
window.changeCartCount = changeCartCount
window.changeCompareCount = changeCompareCount
window.changeFavoritesCount = changeFavoritesCount
