/**
 * Парсер HTML строки для ее перевода в HTML элементы
 * @param {string} markup HTML в виде строки
 * @returns {HTMLElement | Array<HTMLElement>} HTML элементы
 */
export function parseHTML(markup) {
    var parser = new DOMParser()
    var body = parser.parseFromString(markup, "text/html").body
    if (body.children.length > 1) {
        var elements = new Array()
        Array.prototype.slice.call(body.children).forEach(function(item) {
            elements.push(item)
        })
        return elements
    } else {
        return body.firstChild
    }
}

/**
 * Парсер массива HTML строк для перевода в массив HTML элементов
 * @param {Array<string>} markups Массив с html в виде строк
 */
export function parseArrayHTML(markups) {
    var _this = this
    var elements = Array()
    markups.forEach(function(markup) {
        elements.push(_this.parseHTML(markup))
    })
    return elements
}

/**
 * Получение отступов по документу
 * @param {HTMLElement} element
 */
export function offset(element) {
    var rect = element.getBoundingClientRect(),
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    scrollTop = window.pageYOffset || document.documentElement.scrollTop
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
}

/**
 * Пересоздание тегов use в svg'шках
 * Помогает при выводе svg спрайтов ajax загрузки страницы
 */
export function svgRepairUse() {
    const allSVG = Array.prototype.slice.call(document.querySelectorAll('svg'))
    allSVG.forEach(function(svg) {
        if (svg.firstElementChild.href !== undefined) {
            const href = svg.firstElementChild.href.baseVal
            const use = document.createElementNS('http://www.w3.org/2000/svg', 'use')
            use.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', href)
            svg.firstElementChild.remove()
            svg.appendChild(use)
        }
    })
}

/**
 * Создание svg элемента в документе
 * @param {string} href ссылка на svg
 * @param {string} className класс для svg элемента
 * @returns {SVGElement} svg элемент
 */
export function createSVG(href, className = '') {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    const use = document.createElementNS('http://www.w3.org/2000/svg', 'use')
    use.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', href)
    svg.classList.add(className)
    svg.appendChild(use)
    return svg
}

export function request(data, action, method, success = function(response) {}, error = function(error) {}) {
    const url = new URL(action)

    method = method.toLowerCase()
    if (method == 'get') url.search = data

    return new Promise(function(resolve, reject) {
        const xhr = new XMLHttpRequest()

        xhr.open(method, url.href, true)
        if (method === 'post') {
            if (typeof(data) === 'string') {
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
            }
        }
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        xhr.onload = function() {
            if (this.status == 200) {
                resolve(JSON.parse(this.response))
            } else {
                const err = new Error(this.statusText)
                err.code = this.status
                reject(err)
            }
        }
        xhr.send(data)
    }).then(success, error)
}

export function serialize(form) {
    const formData = new FormData(form)
    const arrayData = new Array()
    const data = new String()
    
    for (var item of formData.entries()) { arrayData.push(item) }

    arrayData.forEach(function(item, index) {
        if (index) data += '&'
        data += item[0] + '=' + encodeURIComponent(item[1])
    })

    return data
}

