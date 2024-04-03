import { parseHTML } from "../utils";

const defaultClasses = {
    container: ".sn-autocomplete-address-container",
    control: ".autocomplete-address",
    map: ".sn-autocomplete-address-map"
}

class AutocompleteContainer {
    constructor(container) {
        this.container = container
        this.map = this.container.querySelector(defaultClasses.map)
        this.controls = []

        this.container.querySelectorAll(defaultClasses.control).forEach(control => {
            this.controls.push(new AutocompleteField(this, control))
        })
    }

    addRoute(x, y) {
        // Добавление маршрута на карту
        ymaps.route([{
            type: 'wayPoint',
            point: [this.map.ymap.propPlacemarks[0].lat, this.map.ymap.propPlacemarks[0].lng]
        }, {
            type: 'wayPoint',
            point: [x, y]
        }], {mapStateAutoApply: true}).done(function(route) {
            if (this.route !== null)
                this.map.ymap.map.geoObjects.remove(this.route)
            this.route = route
            this.map.ymap.map.geoObjects.add(this.route)
        }, function(error) {
            console.log("Возникла ошибка: " + error.message)
        }, this)

        if (this.route !== undefined) {
            $.ajax({
                url: "/api/shop/order/calculate/",
                dataType: 'json',
                data: `id_ts=${this.container.dataset.typeShipping}&coord_x_delivery=${x}&coord_y_delivery=${y}&lenght=${this.route.getLength()}`,
                success: _response => {
                    const shippingPrice = document.querySelector(".shipping_price")
                    const total = document.querySelector(".order_total")
                    const input = document.querySelector('[type="hidden"][name="shipping_price"]')
    
                    if (shippingPrice !== null)
                        shippingPrice.innerHTML = _response.shippingPrice + " руб."
    
                    if (input !== null)
                        input.value = _response.shippingPrice
    
                    if (total !== null) {
                        if (_response.shippingPrice === "Бесплатно" || _response.shippingPrice === "Уточняйте у хз кого"){
                            total.innerHTML = total.dataset.order_total + " руб."
                        } else {
                            total.innerHTML = parseFloat(_response.shippingPrice) + parseFloat(total.dataset.order_total)
                            total.innerHTML += " руб."
                        }
                    }
                }
            })
        }
    }
}

class AutocompleteField {
    constructor(container, control) {
        if (!control || control === null) return null
        this.control = control
        this.container = container
        this.name = this.control.name
        this.dropdown = null

        this.control.parentElement.classList.add("dropdown-container")

        this.control.oninput = event => this.updateField(true)
        this.control.onchange = event => this.updateField(false)
    }

    updateField(createDropdown) {
        const address = this.control.value
        
        $.ajax({
            url: 'https://geocode-maps.yandex.ru/1.x/',
            dataType: 'json',
            data: `geocode=${address}&format=json&kind=locality`,
            method: "POST",
            success: response => {
                const choices = [];
                const geoObjects = response.response.GeoObjectCollection.featureMember;

                geoObjects.forEach(option => {
                    choices.push(option.GeoObject.metaDataProperty.GeocoderMetaData.AddressDetails.Country.AddressLine)
                })

                if (createDropdown && choices.length) {
                    this.createDropdown(choices)
                }

                if (geoObjects.length) {
                    const coords = geoObjects[0].GeoObject.Point.pos.split(' ')
                    this.container.addRoute(coords[1], coords[0])
                }
            },

            error: error => {}
        });
    }

    createDropdown(choices) {
        this.removeDropdown()
        this.dropdown = document.createElement("div")
        this.dropdown.classList.add("input-dropdown")

        choices.forEach(choice => {
            const item = parseHTML(`<div class="input-dropdown-item"><span class="input-dropdown-item__text">${choice}</span></div>`)
            item.onclick = event => {
                this.control.value = item.innerText
                this.control.dispatchEvent(new Event("change"))
                this.removeDropdown()
            }
            this.dropdown.append(item)
        })

        document.body.addEventListener("click", this.clickOut.bind(this))
        this.control.parentElement.appendChild(this.dropdown)
    }

    removeDropdown() {
        if (this.dropdown !== null) {
            this.dropdown.remove()
            removeEventListener("click", this.clickOut.bind(this))
        }
    }

    clickOut(event) {
        if (!event.target.closest(".dropdown-container")) {
            this.removeDropdown()
        }
    }
}

if (window.ymaps !== undefined)
    ymaps.ready(function () {
        document.querySelectorAll(defaultClasses.container)
            .forEach(container => new AutocompleteContainer(container))
    })


const autocompleteClasses = {
    container: ".sn-autocomplete-address-container",
    control: ".sn-autocomplete-address",
    map: ".sn-autocomplete-address-map"
}

class AutocompleteAddress {
    /**
     * 
     * @param {HTMLElement} container 
     */
    constructor(container) {
        this.container = container
        this.map = this.container.querySelector(autocompleteClasses.map)
        this.controls = new Array()
        this.route = null

        this.container.querySelectorAll(autocompleteClasses.control).forEach(control => {
            this.controls.push(new AutocompleteAddressControl(this, control))
        })
    }

    /**
     * Запрос на geocode-maps яндекса
     * @param {AutocompleteAddressControl} control 
     */
    yRequest(control, inputEvent = false) {
        const address = this.serialize()
        
        $.ajax({
            url: 'https://geocode-maps.yandex.ru/1.x/',
            dataType: 'json',
            data: `geocode=${address}&format=json&kind=locality`,
            method: "POST",
            success: response => {
                const choices = new Array();
                const geoObjects = response.response.GeoObjectCollection.featureMember;
    
                geoObjects.forEach(option => {
                    option.GeoObject.metaDataProperty.GeocoderMetaData.Address.Components.forEach(component => {
                        if (control.name == component.kind) {
                            choices.push(component.name)
                        }
                    })
                })

                if (inputEvent)
                    control.createDropdown(choices)

                if (geoObjects.length) {
                    const coords = geoObjects[0].GeoObject.Point.pos.split(' ')
                    this.addRoute(coords[1], coords[0])
                }
            },

            error: error => {}
        });
    }

    serialize() {
        const city = this.container.querySelector('[name="city"]').value
        const street = this.container.querySelector('[name="street"]').value
        const house = this.container.querySelector('[name="house"]').value
        const housing = this.container.querySelector('[name="housing"]').value

        let address = city + " " + street + " "
        address += housing ? `${house}к${housing}` : house

        return address
    }

    addRoute(x, y) {
        // Добавление маршрута на карту
        ymaps.route([{
            type: 'wayPoint',
            point: [this.map.ymap.propPlacemarks[0].lat, this.map.ymap.propPlacemarks[0].lng]
        }, {
            type: 'wayPoint',
            point: [x, y]
        }], {mapStateAutoApply: true}).done(function(route) {
            if (this.route !== null)
                this.map.ymap.map.geoObjects.remove(this.route)
            this.route = route
            this.map.ymap.map.geoObjects.add(this.route)
        }, function(error) {
            console.log("Возникла ошибка: " + error.message)
        }, this)

        $.ajax({
            url: "/api/shop/order/calculate/",
            dataType: 'json',
            data: `id_ts=${this.container.dataset.typeShipping}&coord_x_delivery=${x}&coord_y_delivery=${y}&lenght=${this.route.getLength()}`,
            success: _response => {
                const shippingPrice = document.querySelector(".shipping_price")
                const total = document.querySelector(".order_total")
                const input = document.querySelector('[type="hidden"][name="shipping_price"]')

                if (shippingPrice !== null)
                    shippingPrice.innerHTML = _response.shippingPrice + " руб."

                if (input !== null)
                    input.value = _response.shippingPrice

                if (total !== null) {
                    if (_response.shippingPrice === "Бесплатно" || _response.shippingPrice === "Уточняйте у хз кого"){
                        total.innerHTML = total.dataset.order_total + " руб."
                    } else {
                        total.innerHTML = parseFloat(_response.shippingPrice) + parseFloat(total.dataset.order_total)
                        total.innerHTML += " руб."
                    }
                }
            }
        })
    }
}

class AutocompleteAddressControl {
    /**
     * Поле с автозаполнением адреса
     * @param {AutocompleteAddress} container 
     * @param {HTMLElement} control 
     */
    constructor(container, control) {
        if (!control || control === null) return null
        this.control = control
        this.container = container
        this.name = this.control.name
        this.dropdown = null

        if (this.name === "city")
            this.name = "locality"

        this.control.parentElement.classList.add("dropdown-container")

        this.control.oninput = event => {this.container.yRequest(this, true)}
        this.control.onchange = event => {this.container.yRequest(this)}
    }

    createDropdown(choices) {
        this.removeDropdown()
        this.dropdown = document.createElement("div")
        this.dropdown.classList.add("input-dropdown")

        choices.forEach(choice => {
            const item = parseHTML(`<div class="input-dropdown-item"><span class="input-dropdown-item__text">${choice}</span></div>`)
            item.onclick = event => {
                this.control.value = item.innerText
                this.control.dispatchEvent(new Event("change"))
                this.removeDropdown()
            }
            this.dropdown.append(item)
        })

        document.body.addEventListener("click", this.clickOut.bind(this))
        this.control.parentElement.appendChild(this.dropdown)
    }

    removeDropdown() {
        if (this.dropdown !== null) {
            this.dropdown.remove()
            removeEventListener("click", this.clickOut.bind(this))
        }
    }

    clickOut(event) {
        if (!event.target.closest(".dropdown-container")) {
            this.removeDropdown()
        }
    }
}

if (window.ymaps !== undefined)
    ymaps.ready(function () {
        document.querySelectorAll(autocompleteClasses.container)
            .forEach(container => new AutocompleteAddress(container))
    })
