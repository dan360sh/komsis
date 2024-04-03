const defaultMapClasses = {
    contacts: ".contacts-block__map-container",
    order: ".checkout-form__map-container"
}

class YMap {
    /**
     * Яндекс карта
     * @param {HTMLElement} container Контейнер с метками
     */
    constructor(container) {
        if (!container || container === null) return null

        this.container = container
        this.propPlacemarks = new Array()
        this.map = null

        // Получение свойств меток карты
        Array.prototype.slice.call(container.children).forEach(HTMLPlacemark => {
            this.propPlacemarks.push({
                lat: HTMLPlacemark.dataset.lat.replace(/,/, '.'),
                lng: HTMLPlacemark.dataset.lng.replace(/,/, '.'),
                popup: HTMLPlacemark.dataset.popup,
				message: HTMLPlacemark.dataset.message
            })
            HTMLPlacemark.remove()
        })

        // Создание карты
        this.map = new ymaps.Map(container, {
            center: [this.propPlacemarks[0].lat, this.propPlacemarks[0].lng],
            zoom: 14,
            controls: [],
        }, {
            searchControlProvider: 'yandex#search'
        })

        // Создание и добавление макреров на курту
        this.propPlacemarks.forEach(props => this.addPlacemark(props))

        // Перецентровка после изменения размера карты
        this.map.events.add('sizechange', () => {
            this.map.setBounds(this.map.geoObjects.getBounds(), {checkZoomRange: true})
        })

        this.container.ymap = this
    }

    /**
     * Добавление метки на карту
     * @param {{lat: string, lng: string, popup?: string, message?: string}} props Свойства метки
     */
    addPlacemark(props) {
		const MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
			'<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
		);
        const placemark = new ymaps.Placemark([props.lat, props.lng], {
            hintContent: props.message,
            balloonContent: props.popup,
		}, {
			iconLayout: 'default#imageWithContent',
			iconImageHref: '/static/images/map-pin.png',
			iconImageSize: [58, 64],
			iconImageOffset: [-29, -64],
			iconContentOffset: [22, 22],
			iconContentLayout: MyIconContentLayout
		});
        this.map.geoObjects.add(placemark)
        return placemark
    }
}

if (window.ymaps !== undefined)
    ymaps.ready(function () {
        document.querySelectorAll(defaultMapClasses.contacts).forEach(container => new YMap(container))
        document.querySelectorAll(defaultMapClasses.order).forEach(container => new YMap(container))
    })


/////////////
//   API   //
/////////////

window.YMap = YMap