var main =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"main": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/ 	var jsonpArray = window["webpackJsonp_name_"] = window["webpackJsonp_name_"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./src/js/index.js","vendors"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/components/autocomplete-address.js":
/*!***************************************************!*\
  !*** ./src/js/components/autocomplete-address.js ***!
  \***************************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils */ \"./src/js/utils.js\");\n\nconst defaultClasses = {\n  container: \".sn-autocomplete-address-container\",\n  control: \".autocomplete-address\",\n  map: \".sn-autocomplete-address-map\"\n};\n\nclass AutocompleteContainer {\n  constructor(container) {\n    this.container = container;\n    this.map = this.container.querySelector(defaultClasses.map);\n    this.controls = [];\n    this.container.querySelectorAll(defaultClasses.control).forEach(control => {\n      this.controls.push(new AutocompleteField(this, control));\n    });\n  }\n\n  addRoute(x, y) {\n    // Добавление маршрута на карту\n    ymaps.route([{\n      type: 'wayPoint',\n      point: [this.map.ymap.propPlacemarks[0].lat, this.map.ymap.propPlacemarks[0].lng]\n    }, {\n      type: 'wayPoint',\n      point: [x, y]\n    }], {\n      mapStateAutoApply: true\n    }).done(function (route) {\n      if (this.route !== null) this.map.ymap.map.geoObjects.remove(this.route);\n      this.route = route;\n      this.map.ymap.map.geoObjects.add(this.route);\n    }, function (error) {\n      console.log(\"Возникла ошибка: \" + error.message);\n    }, this);\n\n    if (this.route !== undefined) {\n      $.ajax({\n        url: \"/api/shop/order/calculate/\",\n        dataType: 'json',\n        data: `id_ts=${this.container.dataset.typeShipping}&coord_x_delivery=${x}&coord_y_delivery=${y}&lenght=${this.route.getLength()}`,\n        success: _response => {\n          const shippingPrice = document.querySelector(\".shipping_price\");\n          const total = document.querySelector(\".order_total\");\n          const input = document.querySelector('[type=\"hidden\"][name=\"shipping_price\"]');\n          if (shippingPrice !== null) shippingPrice.innerHTML = _response.shippingPrice + \" руб.\";\n          if (input !== null) input.value = _response.shippingPrice;\n\n          if (total !== null) {\n            if (_response.shippingPrice === \"Бесплатно\" || _response.shippingPrice === \"Уточняйте у хз кого\") {\n              total.innerHTML = total.dataset.order_total + \" руб.\";\n            } else {\n              total.innerHTML = parseFloat(_response.shippingPrice) + parseFloat(total.dataset.order_total);\n              total.innerHTML += \" руб.\";\n            }\n          }\n        }\n      });\n    }\n  }\n\n}\n\nclass AutocompleteField {\n  constructor(container, control) {\n    if (!control || control === null) return null;\n    this.control = control;\n    this.container = container;\n    this.name = this.control.name;\n    this.dropdown = null;\n    this.control.parentElement.classList.add(\"dropdown-container\");\n\n    this.control.oninput = event => this.updateField(true);\n\n    this.control.onchange = event => this.updateField(false);\n  }\n\n  updateField(createDropdown) {\n    const address = this.control.value;\n    $.ajax({\n      url: 'https://geocode-maps.yandex.ru/1.x/',\n      dataType: 'json',\n      data: `geocode=${address}&format=json&kind=locality`,\n      method: \"POST\",\n      success: response => {\n        const choices = [];\n        const geoObjects = response.response.GeoObjectCollection.featureMember;\n        geoObjects.forEach(option => {\n          choices.push(option.GeoObject.metaDataProperty.GeocoderMetaData.AddressDetails.Country.AddressLine);\n        });\n\n        if (createDropdown && choices.length) {\n          this.createDropdown(choices);\n        }\n\n        if (geoObjects.length) {\n          const coords = geoObjects[0].GeoObject.Point.pos.split(' ');\n          this.container.addRoute(coords[1], coords[0]);\n        }\n      },\n      error: error => {}\n    });\n  }\n\n  createDropdown(choices) {\n    this.removeDropdown();\n    this.dropdown = document.createElement(\"div\");\n    this.dropdown.classList.add(\"input-dropdown\");\n    choices.forEach(choice => {\n      const item = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"parseHTML\"])(`<div class=\"input-dropdown-item\"><span class=\"input-dropdown-item__text\">${choice}</span></div>`);\n\n      item.onclick = event => {\n        this.control.value = item.innerText;\n        this.control.dispatchEvent(new Event(\"change\"));\n        this.removeDropdown();\n      };\n\n      this.dropdown.append(item);\n    });\n    document.body.addEventListener(\"click\", this.clickOut.bind(this));\n    this.control.parentElement.appendChild(this.dropdown);\n  }\n\n  removeDropdown() {\n    if (this.dropdown !== null) {\n      this.dropdown.remove();\n      removeEventListener(\"click\", this.clickOut.bind(this));\n    }\n  }\n\n  clickOut(event) {\n    if (!event.target.closest(\".dropdown-container\")) {\n      this.removeDropdown();\n    }\n  }\n\n}\n\nif (window.ymaps !== undefined) ymaps.ready(function () {\n  document.querySelectorAll(defaultClasses.container).forEach(container => new AutocompleteContainer(container));\n});\nconst autocompleteClasses = {\n  container: \".sn-autocomplete-address-container\",\n  control: \".sn-autocomplete-address\",\n  map: \".sn-autocomplete-address-map\"\n};\n\nclass AutocompleteAddress {\n  /**\n   * \n   * @param {HTMLElement} container \n   */\n  constructor(container) {\n    this.container = container;\n    this.map = this.container.querySelector(autocompleteClasses.map);\n    this.controls = new Array();\n    this.route = null;\n    this.container.querySelectorAll(autocompleteClasses.control).forEach(control => {\n      this.controls.push(new AutocompleteAddressControl(this, control));\n    });\n  }\n  /**\n   * Запрос на geocode-maps яндекса\n   * @param {AutocompleteAddressControl} control \n   */\n\n\n  yRequest(control, inputEvent = false) {\n    const address = this.serialize();\n    $.ajax({\n      url: 'https://geocode-maps.yandex.ru/1.x/',\n      dataType: 'json',\n      data: `geocode=${address}&format=json&kind=locality`,\n      method: \"POST\",\n      success: response => {\n        const choices = new Array();\n        const geoObjects = response.response.GeoObjectCollection.featureMember;\n        geoObjects.forEach(option => {\n          option.GeoObject.metaDataProperty.GeocoderMetaData.Address.Components.forEach(component => {\n            if (control.name == component.kind) {\n              choices.push(component.name);\n            }\n          });\n        });\n        if (inputEvent) control.createDropdown(choices);\n\n        if (geoObjects.length) {\n          const coords = geoObjects[0].GeoObject.Point.pos.split(' ');\n          this.addRoute(coords[1], coords[0]);\n        }\n      },\n      error: error => {}\n    });\n  }\n\n  serialize() {\n    const city = this.container.querySelector('[name=\"city\"]').value;\n    const street = this.container.querySelector('[name=\"street\"]').value;\n    const house = this.container.querySelector('[name=\"house\"]').value;\n    const housing = this.container.querySelector('[name=\"housing\"]').value;\n    let address = city + \" \" + street + \" \";\n    address += housing ? `${house}к${housing}` : house;\n    return address;\n  }\n\n  addRoute(x, y) {\n    // Добавление маршрута на карту\n    ymaps.route([{\n      type: 'wayPoint',\n      point: [this.map.ymap.propPlacemarks[0].lat, this.map.ymap.propPlacemarks[0].lng]\n    }, {\n      type: 'wayPoint',\n      point: [x, y]\n    }], {\n      mapStateAutoApply: true\n    }).done(function (route) {\n      if (this.route !== null) this.map.ymap.map.geoObjects.remove(this.route);\n      this.route = route;\n      this.map.ymap.map.geoObjects.add(this.route);\n    }, function (error) {\n      console.log(\"Возникла ошибка: \" + error.message);\n    }, this);\n    $.ajax({\n      url: \"/api/shop/order/calculate/\",\n      dataType: 'json',\n      data: `id_ts=${this.container.dataset.typeShipping}&coord_x_delivery=${x}&coord_y_delivery=${y}&lenght=${this.route.getLength()}`,\n      success: _response => {\n        const shippingPrice = document.querySelector(\".shipping_price\");\n        const total = document.querySelector(\".order_total\");\n        const input = document.querySelector('[type=\"hidden\"][name=\"shipping_price\"]');\n        if (shippingPrice !== null) shippingPrice.innerHTML = _response.shippingPrice + \" руб.\";\n        if (input !== null) input.value = _response.shippingPrice;\n\n        if (total !== null) {\n          if (_response.shippingPrice === \"Бесплатно\" || _response.shippingPrice === \"Уточняйте у хз кого\") {\n            total.innerHTML = total.dataset.order_total + \" руб.\";\n          } else {\n            total.innerHTML = parseFloat(_response.shippingPrice) + parseFloat(total.dataset.order_total);\n            total.innerHTML += \" руб.\";\n          }\n        }\n      }\n    });\n  }\n\n}\n\nclass AutocompleteAddressControl {\n  /**\n   * Поле с автозаполнением адреса\n   * @param {AutocompleteAddress} container \n   * @param {HTMLElement} control \n   */\n  constructor(container, control) {\n    if (!control || control === null) return null;\n    this.control = control;\n    this.container = container;\n    this.name = this.control.name;\n    this.dropdown = null;\n    if (this.name === \"city\") this.name = \"locality\";\n    this.control.parentElement.classList.add(\"dropdown-container\");\n\n    this.control.oninput = event => {\n      this.container.yRequest(this, true);\n    };\n\n    this.control.onchange = event => {\n      this.container.yRequest(this);\n    };\n  }\n\n  createDropdown(choices) {\n    this.removeDropdown();\n    this.dropdown = document.createElement(\"div\");\n    this.dropdown.classList.add(\"input-dropdown\");\n    choices.forEach(choice => {\n      const item = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"parseHTML\"])(`<div class=\"input-dropdown-item\"><span class=\"input-dropdown-item__text\">${choice}</span></div>`);\n\n      item.onclick = event => {\n        this.control.value = item.innerText;\n        this.control.dispatchEvent(new Event(\"change\"));\n        this.removeDropdown();\n      };\n\n      this.dropdown.append(item);\n    });\n    document.body.addEventListener(\"click\", this.clickOut.bind(this));\n    this.control.parentElement.appendChild(this.dropdown);\n  }\n\n  removeDropdown() {\n    if (this.dropdown !== null) {\n      this.dropdown.remove();\n      removeEventListener(\"click\", this.clickOut.bind(this));\n    }\n  }\n\n  clickOut(event) {\n    if (!event.target.closest(\".dropdown-container\")) {\n      this.removeDropdown();\n    }\n  }\n\n}\n\nif (window.ymaps !== undefined) ymaps.ready(function () {\n  document.querySelectorAll(autocompleteClasses.container).forEach(container => new AutocompleteAddress(container));\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/autocomplete-address.js?");

/***/ }),

/***/ "./src/js/components/cart.js":
/*!***********************************!*\
  !*** ./src/js/components/cart.js ***!
  \***********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var animejs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! animejs */ \"./node_modules/animejs/anime.min.js\");\n/* harmony import */ var animejs__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(animejs__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils */ \"./src/js/utils.js\");\n\n\n\nfunction blockedCartItem(item) {\n  item.style.pointerEvents = \"none\";\n}\n\nfunction deleteCartItem(item) {\n  animejs__WEBPACK_IMPORTED_MODULE_0___default()({\n    targets: item,\n    opacity: [1, 0],\n    height: [item.clientHeight, 0],\n    duration: 400,\n    easing: \"easeOutQuart\",\n    complete: function () {\n      item.remove();\n    }\n  });\n}\n\nfunction clearCart(markup) {\n  const container = document.querySelector(\".cart-container\");\n  animejs__WEBPACK_IMPORTED_MODULE_0___default()({\n    targets: container,\n    opacity: [1, 0],\n    duration: 400,\n    easing: \"easeOutQuart\",\n    complete: function () {\n      container.innerHTML = markup;\n      animejs__WEBPACK_IMPORTED_MODULE_0___default()({\n        targets: container,\n        opacity: [0, 1],\n        duration: 400,\n        easing: \"easeOutQuart\"\n      });\n    }\n  });\n}\n\nwindow.blockedCartItem = blockedCartItem;\nwindow.deleteCartItem = deleteCartItem;\nwindow.clearCart = clearCart;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/cart.js?");

/***/ }),

/***/ "./src/js/components/catalog-categories.js":
/*!*************************************************!*\
  !*** ./src/js/components/catalog-categories.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {function catalogSubcatsInit() {\n  var width;\n  var b = 1;\n  var sum = 0;\n  $('.catalog-categories__link').each(function (i, el) {\n    var text = $(el).text(); // Приводим ширину элементов к целочисленному значению\n\n    var w = Math.ceil($(el).outerWidth(true)); // добавляем значение отступа справа    \n\n    sum += w; // Складываем ширину соседних элементов                \n\n    if (sum > width) {\n      // Ограничиваем ширину\n      b++; //Считаем кол-во строк\n\n      sum = w; // Приравниваем значение ширины строки к ширине первого элемента в строке\n    }\n\n    if (b == 1) {\n      width = 830;\n    } // значение ширины 1 строки\n\n\n    if (b == 2) {\n      width = 760;\n    } // значение ширины 2 строки\n    else {\n        width = 830;\n      } // значение ширины остальных строк\n\n\n    if (b >= 3) {\n      // Убеждаемся что строк более 3х\n      $(el).addClass('hidden-link'); // добавляем класс на элементы, которые будем скрывать\n    }\n  });\n  $('.hidden-link').wrapAll(\"<div class='catalog-categories__hidden-links'></div>\"); // делаем обертку для 3 и более строк\n\n  $('div.catalog-categories__hidden-links').after('<a href=\"\" class=\"catalog-categories__open\"><span>Еще</span><svg role=\"img\" width=\"8\" height=\"5\"><use xmlns:xlink=\"http://www.w3.org/1999/xlink\" xlink:href=\"/static/images/sprite.svg#caret-bottom\"></use></svg></a>'); // добавляем кнопку ЕЩЕ\n\n  $('.catalog-categories__hidden-links a:last-child').after('<a href=\"\" class=\"catalog-categories__close\"><span>Скрыть</span><svg role=\"img\" width=\"8\" height=\"5\"><use xmlns:xlink=\"http://www.w3.org/1999/xlink\" xlink:href=\"/static/images/sprite.svg#caret-bottom\"></use></svg></a>'); // добавляем кнопку скрыть\n}\n\ncatalogSubcatsInit(); // Действия при кнопке ЕЩЕ\n\n$('body').on('click', 'a.catalog-categories__open', function (event) {\n  $(\".catalog-categories\").toggleClass('opened');\n  $('div.catalog-categories__hidden-links').slideDown(0, function () {\n    $('.catalog-categories__close').css('display', 'inline-block');\n    $(\".catalog-categories a.hidden-link\").unwrap();\n  });\n  $(this).css('display', 'none');\n  return false;\n}); // Действия при кнопке СКРЫТЬ\n\n$('body').on('click', 'a.catalog-categories__close', function (event) {\n  $(\".catalog-categories\").toggleClass('opened');\n  $(\".catalog-categories a.hidden-link\").wrapAll('<div class=\"catalog-categories__hidden-links\"></div>');\n  $('div.catalog-categories__hidden-links').slideUp(function () {\n    $('.catalog-categories__open').css('display', 'inline-block');\n  });\n  $(this).css('display', 'none');\n  return false;\n});\n\nfunction categoriesResize() {\n  if ($(window).width() < 1200) {\n    $('.catalog-categories__close, .catalog-categories__open').css('display', 'none');\n    $(\".catalog-categories .catalog-categories__hidden-links a.hidden-link\").unwrap();\n  } else {\n    $(\".catalog-categories > a.hidden-link\").wrapAll('<div class=\"catalog-categories__hidden-links\"></div>');\n    if (!$(\".catalog-categories\").hasClass(\"opened\")) $('.catalog-categories__open').css('display', 'inline-block');else $('.catalog-categories__close').css('display', 'inline-block');\n  }\n}\n\ncategoriesResize();\n$(window).resize(function () {\n  categoriesResize();\n});\nwindow.categoriesResize = categoriesResize;\nwindow.catalogSubcatsInit = catalogSubcatsInit;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/catalog-categories.js?");

/***/ }),

/***/ "./src/js/components/catalog.js":
/*!**************************************!*\
  !*** ./src/js/components/catalog.js ***!
  \**************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! overlayscrollbars */ \"./node_modules/overlayscrollbars/js/OverlayScrollbars.js\");\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__);\n\n\nfunction showProductsPreloader() {\n  $(\"body\").addClass('loading-blocks');\n}\n\nfunction hideProductsPreloader() {\n  $(\"body\").removeClass('loading-blocks');\n}\n\nfunction replaceCatalogData(event, data, more) {\n  more = more || false;\n  $('.filter-counter').fadeOut(200);\n\n  if (data['products'] != undefined) {\n    var html_products = data['products'];\n    if (more) $('.sn-products-container').append(html_products);else $('.sn-products-container').html(html_products);\n    $('.paginationBlock').html(data['pagination']);\n    $('.filterBlock').replaceWith(data['template_filters']); // $('.filter-block__scroll-content').overlayScrollbars({\n    // \toverflowBehavior: {\n    // \t\tx: \"hidden\" \n    // \t}\n    // });\n\n    OverlayScrollbars(document.querySelectorAll(\".filter-block__scroll-content\"), {\n      autoUpdate: true,\n      overflowBehavior: {\n        x: \"hidden\",\n        y: \"scroll\"\n      }\n    }); // Init range slider\n\n    $(\".range-slider-field\").each(function (index, elem) {\n      new RangeSliderField(elem);\n    });\n  } else {\n    $('.paginationBlock').html(\"\");\n    $('.sn-products-container').html('<div class=\"products-container\">\\\n            <div class=\"row sn-products-container\">\\\n                <div class=\"col-12\">\\\n                <p class=\"empty-category__title\">По данному запросу товаров не найдено.</p>\\\n                </div>\\\n            \t</div>\\\n    \t\t</div>');\n  } // lazy load\n  // $('img.lazy').each(function (index, el) {\n  // \t$(el).parent().addClass('lazy_wrap');\n  // \t$(el).lazy({\n  // \t\tafterLoad: function (element) {\n  // \t\t\t$(el).parent().removeClass('lazy_wrap');\n  // \t\t}\n  // \t});\n  // });\n\n\n  $(\".product-card-body\").each(function (index, item) {\n    cutProductText(item);\n  });\n  sort_filter();\n  toggleCatalogPreloader();\n  hideProductsPreloader();\n}\n\nfunction toggleCatalogPreloader() {\n  $(\".products-container\").toggleClass('loading');\n}\n\nwindow.showProductsPreloader = showProductsPreloader;\nwindow.hideProductsPreloader = hideProductsPreloader;\nwindow.replaceCatalogData = replaceCatalogData;\nwindow.toggleCatalogPreloader = toggleCatalogPreloader;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/catalog.js?");

/***/ }),

/***/ "./src/js/components/checkout-form.js":
/*!********************************************!*\
  !*** ./src/js/components/checkout-form.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {function toggleCheckoutFormStatus() {\n  $(\".checkout-form\").toggleClass('loading');\n}\n\nwindow.toggleCheckoutFormStatus = toggleCheckoutFormStatus;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/checkout-form.js?");

/***/ }),

/***/ "./src/js/components/compare-component.js":
/*!************************************************!*\
  !*** ./src/js/components/compare-component.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {class CompareScroller {\n  constructor(scroller) {\n    this.selector = scroller;\n    this.rows = [];\n    this.productScroller;\n    this.init();\n  }\n\n  setRowWidth() {\n    var amount = $(\".product-card\").length;\n    var blockWidth = $(\".product-card\").outerWidth();\n    var blockMargin = parseInt($(\".product-card\").css('margin-left')) * 2;\n    $(\".compare-table__fixed-container\").width(amount * (blockWidth + blockMargin + 1)); // 1 – погрешность\n  }\n\n  showDifferentParams(isChecked) {\n    if (isChecked) {\n      var $table = $(\".compare-table\");\n      $table.find('.compare-table__row').each((ind1, row) => {\n        var $items = $(row).find('.compare-table__row-item');\n        var text = $items[0].innerHTML.trim();\n        var hasUnique = false;\n        $items.each(function (ind2, item) {\n          if (item.innerHTML.trim() !== text) hasUnique = true;\n        });\n\n        if (!hasUnique) {\n          var $item = $(row).find('.compare-table__row-wrapper');\n          $(row).addClass('not-unique');\n\n          for (let arrayRow of this.rows) {\n            if ($item[0] === $(arrayRow.getElements().target).closest('.compare-table__row-wrapper')[0]) {\n              arrayRow.sleep();\n            }\n          }\n        }\n      });\n      $table.each(function (i, el) {\n        if (!$(el).find('.compare-table__row').not('.not-unique').length) $(el).addClass('empty');\n      });\n    } else {\n      $('.compare-table.empty').removeClass('empty');\n      $('.compare-table__row.not-unique').each((i, el) => {\n        var $item = $(el).find('.compare-table__row-wrapper');\n        $(el).removeClass('not-unique');\n\n        for (let arrayRow of this.rows) {\n          if ($item[0] === $(arrayRow.getElements().target).closest('.compare-table__row-wrapper')[0]) {\n            arrayRow.scroll([this.productScroller.scroll().x.position, 0], 0);\n            arrayRow.update();\n          }\n        }\n      });\n    }\n  }\n\n  initProductScroller() {\n    let self = this;\n    self.productScroller = OverlayScrollbars(document.querySelector('.compare-component__product-scroller'), {\n      autoUpdate: true,\n      callbacks: {\n        onScroll: function (event) {\n          for (row in self.rows) {\n            self.rows[row].scroll([event.target.scrollLeft, 0], 0);\n          }\n        },\n        onInitialized: function () {\n          self.setRowWidth();\n        },\n        onUpdated: function () {\n          self.setRowWidth();\n        }\n      }\n    });\n  }\n\n  initCompareRows() {\n    let self = this;\n    $('.compare-table__row-wrapper').each((index, element) => {\n      self.rows.push(OverlayScrollbars($(element), {\n        autoUpdate: true,\n        scrollbars: {\n          visibility: 'hidden'\n        },\n        callbacks: {\n          onScroll: function (event) {\n            self.productScroller.scroll([event.target.scrollLeft, 0], 0);\n\n            for (row in self.rows) {\n              self.rows[row].scroll([event.target.scrollLeft, 0], 0);\n            }\n          }\n        }\n      }));\n    });\n  }\n\n  mobileScroll(elem) {\n    if ($(window).width() < 991) {\n      if (window.pageYOffset > elem.offset().top + elem.find('.compare-component__controlls').outerHeight() - 10) {\n        $('.compare-component').addClass('scrolled');\n      } else {\n        $('.compare-component').removeClass('scrolled');\n      }\n    } else {\n      $('.compare-component').removeClass('scrolled');\n    }\n  }\n\n  init() {\n    this.initProductScroller();\n    this.initCompareRows();\n  }\n\n}\n\nvar scroller = new CompareScroller('.compare-component');\n$(window).scroll(function () {\n  let elem = $('.compare-component');\n  if (elem.length) scroller.mobileScroll(elem);\n});\n$(\"body\").on(\"change\", \".show-different .toggle-button__input\", function () {\n  scroller.showDifferentParams($(this)[0].checked);\n});\n$('body').on('hidden.bs.collapse', '.compare-component .compare-table__body', function (event) {\n  $collapseElement = $(this);\n\n  for (let row of scroller.rows) {\n    if ($collapseElement[0] === $(row.getElements().target).closest('.compare-table__body')[0]) {\n      row.sleep();\n    }\n  }\n});\n$('body').on('shown.bs.collapse', '.compare-component .compare-table__body', function (event) {\n  $collapseElement = $(this);\n\n  for (let row of scroller.rows) {\n    if ($collapseElement[0] === $(row.getElements().target).closest('.compare-table__body')[0]) {\n      row.scroll([scroller.productScroller.scroll().x.position, 0], 0);\n      row.update();\n    }\n  }\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/compare-component.js?");

/***/ }),

/***/ "./src/js/components/content-text.js":
/*!*******************************************!*\
  !*** ./src/js/components/content-text.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {function custom_resize() {\n  $('.content img').each(function (i, e) {\n    var w_post_img = $(e).width();\n    var h_post_img = w_post_img * 32 / 87;\n    $(e).css('height', h_post_img);\n  });\n  $('.gallery a').each(function (i, e) {\n    var w_gallery_img = $(e).width();\n    var h_gallery_img = w_gallery_img / 1.5;\n    $(e).css('height', h_gallery_img);\n  });\n  $('.gallery .item-thumbnail, .certificates .certificate-thumbnail').each(function (i, e) {\n    var w_gallery_img = $(e).width();\n    var h_gallery_img = w_gallery_img / 1.5;\n    $(e).css('height', h_gallery_img);\n  });\n}\n\ncustom_resize();\n$(window).resize(function () {\n  custom_resize();\n});\n/*     Обертка таблицы на текстовых    */\n\n$('.content-text > table').prev('h3').addClass('for_table');\n$(\".content-text > table\").wrap(\"<div class='table'><div class='table-responsive'></div></div>\");\n$('.content-text > .table').each(function () {\n  $(this).prev('h3.for_table').prependTo($(this));\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/content-text.js?");

/***/ }),

/***/ "./src/js/components/cut-articles-text.js":
/*!************************************************!*\
  !*** ./src/js/components/cut-articles-text.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\".article-card-info\").dotdotdot();\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/cut-articles-text.js?");

/***/ }),

/***/ "./src/js/components/extra-products-slider.js":
/*!****************************************************!*\
  !*** ./src/js/components/extra-products-slider.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {/*\tСлайдер доп товаров в карточке товара\n---------------------------------------*/\n$('.extra-products-slider__slider-body').each(function (i, e) {\n  $parent = $(e).parents('.extra-products-slider');\n  $parent.addClass('active');\n  $(e).slick({\n    centerMode: false,\n    slidesToShow: 4,\n    slidesToScroll: 4,\n    nextArrow: $parent.find('.next'),\n    prevArrow: $parent.find('.prev'),\n    responsive: [{\n      breakpoint: 1200,\n      settings: {\n        slidesToShow: 3,\n        slidesToScroll: 3\n      }\n    }, {\n      breakpoint: 992,\n      settings: {\n        slidesToShow: 2,\n        slidesToScroll: 2\n      }\n    }, {\n      breakpoint: 768,\n      settings: {\n        slidesToShow: 1,\n        slidesToScroll: 1\n      }\n    }]\n  });\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/extra-products-slider.js?");

/***/ }),

/***/ "./src/js/components/filter-block.js":
/*!*******************************************!*\
  !*** ./src/js/components/filter-block.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/filter-block.js?");

/***/ }),

/***/ "./src/js/components/filter-counter.js":
/*!*********************************************!*\
  !*** ./src/js/components/filter-counter.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {// $('.filters input[type=\"checkbox\"]').each(function (index, el) {\n// \t$(el).click(function (event) {\n// \t\tvar current = $('.filters input[type=\"checkbox\"]:checked').length;\n// \t\tif (current > 0) {\n// \t\t\tshowFilterCounter();\n// \t\t\tclearTimeout(window.labelTimeout);\n// \t\t\twindow.labelTimeout = setTimeout(function () {\n// \t\t\t\thideFilterCounter();\n// \t\t\t}, 5000);\n// \t\t} else {\n// \t\t\thideFilterCounter();\n// \t\t}\n// \t\tif ($(el).prop('checked')) {\n// \t\t\t$(el).next('label').find('span').addClass('active');\n// \t\t} else {\n// \t\t\t$(el).next('label').find('span').removeClass('active');\n// \t\t}\n// \t});\n// });\n// $('.filters label').each(function (index, el) {\n// \t$(el).click(function (event) {\n// \t\tvar position = $(el).position();\n// \t\tvar $filters = $(el).parents(\".filters\");\n// \t\tfilterShowCounter(this);\n// \t});\n// });\n$('body').on('click', '.filters label', function () {\n  filterShowCounter(this);\n});\n$('body').on('hide.bs.collapse', '.filter>div', function () {\n  hideFilterCounter();\n});\n$('body').on('click', '.filter-counter', function (e) {\n  $('body,html').animate({\n    scrollTop: 0\n  }, 400);\n});\n\nfunction filterShowCounter(this_ob, offset = -8) {\n  var $filters = $(this_ob).parents(\".filters\");\n  $('.filter-counter').css('top', $(this_ob).offset().top - $filters.offset().top + offset);\n  showFilterCounter();\n  clearTimeout(window.labelTimeout);\n  window.labelTimeout = setTimeout(function () {\n    hideFilterCounter();\n  }, 5000);\n}\n\nfunction hideFilterCounter() {\n  $('.filter-counter').fadeOut(200);\n}\n\nfunction showFilterCounter() {\n  $('.filter-counter').fadeIn(200);\n}\n\nwindow.filterShowCounter = filterShowCounter;\nwindow.hideFilterCounter = hideFilterCounter;\nwindow.showFilterCounter = showFilterCounter;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/filter-counter.js?");

/***/ }),

/***/ "./src/js/components/filters.js":
/*!**************************************!*\
  !*** ./src/js/components/filters.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("/* WEBPACK VAR INJECTION */(function($) {\n\n$(\"body\").on('click', '.filters__mobile-submit', function () {\n  updateCatalog(event);\n  showProductsPreloader();\n  closeMobileFilters();\n  catalogScrollTop();\n});\n$(\"body\").on('click', '.filters__mobile-reset, #reset_filter', function () {\n  let form = $(\".filtering\")[0];\n  form.reset();\n  updateCatalog(event, false, true);\n  showProductsPreloader();\n  closeMobileFilters();\n  catalogScrollTop();\n});\n\nfunction openMobileFilters() {\n  $(\".filters, body, .nav-close\").addClass('opened');\n}\n\nfunction closeMobileFilters() {\n  $(\".filters, body, .nav-close\").removeClass('opened');\n}\n\nfunction catalogScrollTop() {\n  $('html, body').animate({\n    scrollTop: 0\n  }, 500);\n}\n\n$('body').on('submit', 'form.filtering', catalogScrollTop);\nwindow.openMobileFilters = openMobileFilters;\nwindow.closeMobileFilters = closeMobileFilters;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/filters.js?");

/***/ }),

/***/ "./src/js/components/footer-social-link.js":
/*!*************************************************!*\
  !*** ./src/js/components/footer-social-link.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {var divs = $(\".footer-social-link\").not('.footer-social-link_wide');\n\nfor (var i = 0; i < divs.length; i += 3) {\n  divs.slice(i, i + 3).wrapAll(\"<div class='footer-social-links-wrapper'></div>\");\n}\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/footer-social-link.js?");

/***/ }),

/***/ "./src/js/components/form.js":
/*!***********************************!*\
  !*** ./src/js/components/form.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function validateForm(form, fields) {\n  let isValid = true;\n\n  for (const key in fields) {\n    if (fields.hasOwnProperty(key)) {\n      const control = form.querySelector('[name=\"' + key + '\"]');\n      const group = control.parentElement;\n      const feedback = document.createElement(\"div\");\n      control.classList.add(\"is-invalid\");\n      feedback.classList.add(\"invalid-feedback\");\n      feedback.innerHTML = fields[key];\n      group.appendChild(feedback);\n      isValid = false;\n    }\n  }\n\n  const agree = form.querySelector('[name=\"agree\"]');\n\n  if (agree !== null) {\n    if (!agree.checked) isValid = false;\n  }\n\n  return isValid;\n}\n\nfunction clearForm(form) {\n  form.querySelectorAll(\".form-control\").forEach(control => {\n    const group = control.parentElement;\n    control.classList.remove(\"is-invalid\", \"is-valid\");\n    form.querySelectorAll(\".invalid-feedback, .valid-feedback, .alert\").forEach(element => {\n      element.remove();\n    });\n  });\n}\n\nfunction successForm(form, message) {\n  const alertSuccess = document.createElement(\"div\");\n  const group = form.querySelector(\".form-group\");\n  clearForm(form);\n  alertSuccess.classList.add(\"alert\", \"alert-success\");\n  alertSuccess.innerHTML = message;\n  alertSuccess.role = \"alert\";\n\n  if (group !== null) {\n    form.insertBefore(alertSuccess, group);\n  } else {\n    form.appendChild(alertSuccess);\n  }\n} /////////////\n//   API   //\n/////////////\n\n\nwindow.validateForm = validateForm;\nwindow.clearForm = clearForm;\nwindow.successForm = successForm;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/form.js?");

/***/ }),

/***/ "./src/js/components/header.js":
/*!*************************************!*\
  !*** ./src/js/components/header.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function(jQuery) {jQuery(document).ready(function ($) {\n  console.log(\"Header init\");\n  var mainHeader = $('.cd-auto-hide-header'),\n      secondaryNavigation = $('.cd-secondary-nav'),\n      //this applies only if secondary nav is below intro section\n  belowNavHeroContent = $('.sub-nav-hero'),\n      headerHeight = mainHeader.height(); //set scrolling variables\n\n  var scrolling = false,\n      previousTop = 0,\n      currentTop = 0,\n      scrollDelta = 10,\n      scrollOffset = 150;\n  mainHeader.on('click', '.nav-trigger', function (event) {\n    // open primary navigation on mobile\n    event.preventDefault();\n    mainHeader.toggleClass('nav-open');\n  });\n  $(window).on('scroll', function () {\n    if (!scrolling) {\n      scrolling = true;\n      !window.requestAnimationFrame ? setTimeout(autoHideHeader, 250) : requestAnimationFrame(autoHideHeader);\n    }\n  });\n  $(window).on('resize', function () {\n    headerHeight = mainHeader.height();\n  });\n\n  function autoHideHeader() {\n    var currentTop = $(window).scrollTop();\n    belowNavHeroContent.length > 0 ? checkStickyNavigation(currentTop) // secondary navigation below intro\n    : checkSimpleNavigation(currentTop);\n    previousTop = currentTop;\n    scrolling = false;\n  }\n\n  function checkSimpleNavigation(currentTop) {\n    //there's no secondary nav or secondary nav is below primary nav\n    if (previousTop - currentTop > scrollDelta) {\n      //if scrolling up...\n      mainHeader.removeClass('is-hidden');\n    } else if (currentTop - previousTop > scrollDelta && currentTop > scrollOffset) {\n      //if scrolling down...\n      mainHeader.addClass('is-hidden');\n    }\n  }\n\n  function checkStickyNavigation(currentTop) {\n    //secondary nav below intro section - sticky secondary nav\n    var secondaryNavOffsetTop = belowNavHeroContent.offset().top - secondaryNavigation.height() - mainHeader.height();\n\n    if (previousTop >= currentTop) {\n      //if scrolling up... \n      if (currentTop < secondaryNavOffsetTop) {\n        //secondary nav is not fixed\n        mainHeader.removeClass('is-hidden');\n        secondaryNavigation.removeClass('fixed slide-up');\n        belowNavHeroContent.removeClass('secondary-nav-fixed');\n      } else if (previousTop - currentTop > scrollDelta) {\n        //secondary nav is fixed\n        mainHeader.removeClass('is-hidden');\n        secondaryNavigation.removeClass('slide-up').addClass('fixed');\n        belowNavHeroContent.addClass('secondary-nav-fixed');\n      }\n    } else {\n      //if scrolling down...\t\n      if (currentTop > secondaryNavOffsetTop + scrollOffset) {\n        //hide primary nav\n        mainHeader.addClass('is-hidden');\n        secondaryNavigation.addClass('fixed slide-up');\n        belowNavHeroContent.addClass('secondary-nav-fixed');\n      } else if (currentTop > secondaryNavOffsetTop) {\n        //once the secondary nav is fixed, do not hide primary nav if you haven't scrolled more than scrollOffset \n        mainHeader.removeClass('is-hidden');\n        secondaryNavigation.addClass('fixed').removeClass('slide-up');\n        belowNavHeroContent.addClass('secondary-nav-fixed');\n      }\n    }\n  }\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/header.js?");

/***/ }),

/***/ "./src/js/components/input-tel.js":
/*!****************************************!*\
  !*** ./src/js/components/input-tel.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// eval("/* WEBPACK VAR INJECTION */(function($) {$('input[type=\"tel\"]').mask(\"+7 (999) 999-99-99\");\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/input-tel.js?");

/***/ }),

/***/ "./src/js/components/loading-blocks.js":
/*!*********************************************!*\
  !*** ./src/js/components/loading-blocks.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/loading-blocks.js?");

/***/ }),

/***/ "./src/js/components/map.js":
/*!**********************************!*\
  !*** ./src/js/components/map.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("const defaultMapClasses = {\n  contacts: \".contacts-block__map-container\",\n  order: \".checkout-form__map-container\"\n};\n\nclass YMap {\n  /**\n   * Яндекс карта\n   * @param {HTMLElement} container Контейнер с метками\n   */\n  constructor(container) {\n    if (!container || container === null) return null;\n    this.container = container;\n    this.propPlacemarks = new Array();\n    this.map = null; // Получение свойств меток карты\n\n    Array.prototype.slice.call(container.children).forEach(HTMLPlacemark => {\n      this.propPlacemarks.push({\n        lat: HTMLPlacemark.dataset.lat.replace(/,/, '.'),\n        lng: HTMLPlacemark.dataset.lng.replace(/,/, '.'),\n        popup: HTMLPlacemark.dataset.popup,\n        message: HTMLPlacemark.dataset.message\n      });\n      HTMLPlacemark.remove();\n    }); // Создание карты\n\n    this.map = new ymaps.Map(container, {\n      center: [this.propPlacemarks[0].lat, this.propPlacemarks[0].lng],\n      zoom: 14,\n      controls: []\n    }, {\n      searchControlProvider: 'yandex#search'\n    }); // Создание и добавление макреров на курту\n\n    this.propPlacemarks.forEach(props => this.addPlacemark(props)); // Перецентровка после изменения размера карты\n\n    this.map.events.add('sizechange', () => {\n      this.map.setBounds(this.map.geoObjects.getBounds(), {\n        checkZoomRange: true\n      });\n    });\n    this.container.ymap = this;\n  }\n  /**\n   * Добавление метки на карту\n   * @param {{lat: string, lng: string, popup?: string, message?: string}} props Свойства метки\n   */\n\n\n  addPlacemark(props) {\n    const MyIconContentLayout = ymaps.templateLayoutFactory.createClass('<div style=\"color: #FFFFFF; font-weight: bold;\">$[properties.iconContent]</div>');\n    const placemark = new ymaps.Placemark([props.lat, props.lng], {\n      hintContent: props.message,\n      balloonContent: props.popup\n    }, {\n      iconLayout: 'default#imageWithContent',\n      iconImageHref: '/static/images/map-pin.png',\n      iconImageSize: [58, 64],\n      iconImageOffset: [-29, -64],\n      iconContentOffset: [22, 22],\n      iconContentLayout: MyIconContentLayout\n    });\n    this.map.geoObjects.add(placemark);\n    return placemark;\n  }\n\n}\n\nif (window.ymaps !== undefined) ymaps.ready(function () {\n  document.querySelectorAll(defaultMapClasses.contacts).forEach(container => new YMap(container));\n  document.querySelectorAll(defaultMapClasses.order).forEach(container => new YMap(container));\n}); /////////////\n//   API   //\n/////////////\n\nwindow.YMap = YMap;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/map.js?");

/***/ }),

/***/ "./src/js/components/mini-button.js":
/*!******************************************!*\
  !*** ./src/js/components/mini-button.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function miniButtonHandler(button) {\n  if (button.classList.contains(\"active\")) {\n    button.classList.remove(\"active\");\n  } else {\n    button.classList.add(\"active\");\n  }\n}\n\nwindow.miniButtonHandler = miniButtonHandler;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/mini-button.js?");

/***/ }),

/***/ "./src/js/components/mobile-filters-trigger.js":
/*!*****************************************************!*\
  !*** ./src/js/components/mobile-filters-trigger.js ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('body').on('click', '.mobile-filters-trigger', function (e) {\n  e.preventDefault();\n  if (!$(\"body\").hasClass('loading-blocks')) openMobileFilters();\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/mobile-filters-trigger.js?");

/***/ }),

/***/ "./src/js/components/mobile-menu.js":
/*!******************************************!*\
  !*** ./src/js/components/mobile-menu.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {const button = document.querySelector(\".mobile-menu-button\");\nconst opened = false;\n\nbutton.onclick = function (event) {\n  if (button.classList.contains(\"opened\")) {\n    button.classList.remove(\"opened\");\n    document.querySelector(\"body\").classList.remove('opened');\n    $(\".mobile-menu *.opened\").removeClass('opened');\n  } else {\n    button.classList.add(\"opened\");\n    document.querySelector(\"body\").classList.add('opened');\n  }\n\n  $(\".mobile-menu\").toggleClass('opened');\n  $(\".mobile-search-wrapper, .mobile-search-trigger\").removeClass('opened');\n\n  if ($(this).hasClass(\"opened\")) {\n    $(\".mobile-menu .sub-menu.opened\").removeClass('opened');\n    $(\".mobile-menu.no-scroll, .mobile-menu .sub-menu.no-scroll\").removeClass('no-scroll');\n  }\n};\n/*\tОткрытие мобильного подменю\n---------------------------------------*/\n\n\n$(\"body\").on('click', '.mobile-menu .has-children > a', function (e) {\n  e.preventDefault();\n  $(this).closest(\".sub-menu, .mobile-menu\").toggleClass('no-scroll');\n  $(this).closest(\".has-children\").find(\"> .sub-menu\").toggleClass('opened');\n});\n/*\tЗакрытие мобильного подменю\n---------------------------------------*/\n\n$(\"body\").on('click', '.mobile-menu .step_back', function (e) {\n  e.preventDefault();\n  $(this).closest(\".sub-menu.no-scroll, .mobile-menu.no-scroll\").toggleClass('no-scroll');\n  $(this).closest(\".sub-menu.opened\").toggleClass('opened');\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/mobile-menu.js?");

/***/ }),

/***/ "./src/js/components/mobile-search-trigger.js":
/*!****************************************************!*\
  !*** ./src/js/components/mobile-search-trigger.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\"body\").on('click', '.mobile-search-trigger', function () {\n  if (!$(this).hasClass(\"opened\")) {\n    if (!$(\"body\").hasClass(\"opened\")) $(\"body\").addClass('opened');\n  } else $(\"body\").removeClass('opened');\n\n  $(this).toggleClass('opened');\n  $(\".mobile-menu, .mobile-menu-button, .mobile-menu .sub-menu.opened\").removeClass('opened');\n  $(\".mobile-menu.no-scroll, .mobile-menu .sub-menu.no-scroll\").removeClass('no-scroll');\n  $(\".mobile-search-wrapper\").toggleClass('opened');\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/mobile-search-trigger.js?");

/***/ }),

/***/ "./src/js/components/modal.js":
/*!************************************!*\
  !*** ./src/js/components/modal.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {/* Открытие другой модалки из модалки */\n$(\".open_other_modal\").click(function (e) {\n  e.preventDefault();\n  $(this).parents(\".custom_modal\").toggleClass(\"opened\");\n  $($(this).data(\"target\")).toggleClass(\"opened\");\n});\n$(\"body\").on('click', \".modal_trigger\", function (e) {\n  e.preventDefault();\n  $modal = $(\".custom_modal.opened\");\n\n  if ($modal.length) {\n    resetModal($modal);\n  }\n\n  $(\"body, i.modal_bg\").addClass('opened');\n  $(\".custom_modal.opened\").toggleClass('opened');\n  $($(this).data(\"target\")).addClass(\"opened\");\n});\n$(\"body\").on('click', \".modal_close, i.modal_bg\", function (e) {\n  e.preventDefault();\n\n  if (!$(\".mobile-menu\").hasClass('opened')) {\n    $(\"body\").removeClass('opened');\n  }\n\n  resetModal($(\".custom_modal.opened\"));\n  $(\"i.modal_bg, .custom_modal.opened\").removeClass('opened');\n});\n\nfunction resetModal(modal) {\n  let form = modal.find('form');\n\n  if (form.length) {\n    modal.find('form')[0].reset();\n    modal.find('form').removeClass('success load');\n    modal.find('form').find('.form-control').removeClass('is-valid is-invalid');\n  }\n}\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/modal.js?");

/***/ }),

/***/ "./src/js/components/nav-close.js":
/*!****************************************!*\
  !*** ./src/js/components/nav-close.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('body').on('click', '.nav-close', function (e) {\n  e.preventDefault();\n  $(\".filters, body, .nav-close\").removeClass('opened');\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/nav-close.js?");

/***/ }),

/***/ "./src/js/components/pagination.js":
/*!*****************************************!*\
  !*** ./src/js/components/pagination.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("function blockingPagination() {\n  const paginationBlock = document.querySelector(\".paginationBlock\");\n  paginationBlock.style.pointerEvents = \"none\";\n}\n\nfunction unblickingPagination() {\n  const paginationBlock = document.querySelector(\".paginationBlock\");\n  paginationBlock.style.pointerEvents = \"\";\n}\n\nwindow.blockingPagination = blockingPagination;\nwindow.unblickingPagination = unblickingPagination;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/pagination.js?");

/***/ }),

/***/ "./src/js/components/product-amount.js":
/*!*********************************************!*\
  !*** ./src/js/components/product-amount.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('body').on('click', '.product-amount__button', function (event) {\n  var $input = $(this).parents('.product-amount').find('input');\n  var val = parseFloat($input.val().replace(\",\", \".\"));\n  if ($(this).hasClass('product-amount__button_minus')) $input.val(val - 1);else $input.val(val + 1);\n  $(this).parents('.product-amount').find('input').change();\n  setCoords($(this).parents('.product-amount'), event);\n});\n$('body').on('change', '.product-amount input', function () {\n  var val = parseFloat($(this).val().replace(\",\", \".\"));\n  var min = parseFloat($(this).attr('min').replace(\",\", \".\"));\n  var max = parseFloat($(this).attr('max').replace(\",\", \".\"));\n  if (val > max) showTip($(this).parents('.product-amount'), 'max');\n  if (val < min) showTip($(this).parents('.product-amount'));\n  $(this).val(val > max ? max : val < min ? min : val);\n});\n\nfunction setCoords(target, event) {\n  $notification = target.find('.product-amount__notification');\n  $notification.css({\n    'left': event.clientX,\n    'top': event.clientY - $notification.outerHeight()\n  });\n}\n\nfunction showTip(target, type) {\n  if (type) {\n    target.find('.product-amount__notification_max').show();\n    clearTimeout(timeout);\n    timeout = setTimeout(() => {\n      target.find('.product-amount__notification_max').hide();\n    }, 1000);\n  } else {\n    target.find('.product-amount__notification_min').show();\n    clearTimeout(timeout);\n    timeout = setTimeout(() => {\n      target.find('.product-amount__notification_min').hide();\n    }, 1000);\n  }\n}\n\nvar timeout;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/product-amount.js?");

/***/ }),

/***/ "./src/js/components/product-card.js":
/*!*******************************************!*\
  !*** ./src/js/components/product-card.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {if (!Array.prototype.forEach) {\n  Array.prototype.forEach = function (callback, thisArg) {\n    var T, k;\n\n    if (this == null) {\n      throw new TypeError(' this is null or not defined');\n    }\n\n    var O = Object(this);\n    var len = O.length >>> 0;\n\n    if (typeof callback !== 'function') {\n      throw new TypeError(callback + ' is not a function');\n    }\n\n    if (arguments.length > 1) {\n      T = thisArg;\n    }\n\n    k = 0;\n\n    while (k < len) {\n      var kValue;\n\n      if (k in O) {\n        kValue = O[k];\n        callback.call(T, kValue, k, O);\n      }\n\n      k++;\n    }\n  };\n}\n\nfunction removeProduct(product) {\n  product.classList.add('removed');\n}\n\nfunction restoreProduct(product) {\n  product.classList.remove('removed');\n}\n\nfunction productCartAdded(product) {\n  var button = product.querySelector(\".add-to-cart\");\n  button.classList.add(\"added\");\n  button.disabled = true;\n  button.dataset.text = button.innerText;\n  button.innerHTML = \"Добавлено\";\n  setTimeout(function () {\n    button.classList.remove(\"added\");\n    button.disabled = false;\n    button.innerHTML = button.dataset.text;\n    button.dataset.text = \"\";\n  }, 3000);\n}\n\nfunction cutProductText(item) {\n  $(item).dotdotdot();\n}\n\nwindow.removeProduct = removeProduct;\nwindow.restoreProduct = restoreProduct;\nwindow.productCartAdded = productCartAdded;\nwindow.cutProductText = cutProductText;\n$(\".product-card-remove\").each(function (index, button) {\n  var product = button.closest(\".product-card\");\n  button.addEventListener(\"click\", function (event) {\n    removeProduct(product);\n  });\n});\n$(\".product-card-restore\").each(function (index, button) {\n  var product = button.closest(\".product-card\");\n  button.addEventListener(\"click\", function (event) {\n    restoreProduct(product);\n  });\n});\n$(\".product-card-body\").each(function (index, item) {\n  cutProductText(item);\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/product-card.js?");

/***/ }),

/***/ "./src/js/components/product-counter.js":
/*!**********************************************!*\
  !*** ./src/js/components/product-counter.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// eval("/* WEBPACK VAR INJECTION */(function($) {$('body').on('click', '.product-counter__button', function (event) {\n  var $input = $(this).parents('.product-counter').find('input');\n  var val = parseFloat($input.attr(\"value\").replace(\",\", \".\"));\n  var step = parseFloat($input.data('step').replace(\",\", \".\"));\n  if ($(this).hasClass('product-counter__button_minus') && val >= step) $input.attr(\"value\", val - step);else $input.attr(\"value\", val + step);\n  $(this).parents('.product-counter').find('input').change(); // setCoords($(this).parents('.product-counter'), event);\n});\n$('body').on('change', '.product-counter input', function () {\n  var val = parseFloat($(this).val().replace(\",\", \".\"));\n  var min = parseFloat($(this).attr('min').replace(\",\", \".\"));\n  var max = parseFloat($(this).attr('max').replace(\",\", \".\"));\n  if (val > max) showTip($(this).parents('.product-counter'), 'max');\n  if (val < min) showTip($(this).parents('.product-counter'));\n  $(this).attr(\"value\", val > max ? max : val < min ? min : val);\n  updateFakeInput(this);\n});\n\nfunction updateFakeInput(target) {\n  let parent = target.closest('.product-counter'); // unit = parent.find('.product-counter__original-input').data('unit'),\n\n  let val = parseInt(parent.querySelector('.product-counter__original-input').attributes.value.value.replace(\",\", \".\"));\n  console.log(val);\n  parent.querySelector('.product-counter__fake-input').innerText = `${val}`;\n $(this).val(val.toString());} // function setCoords(target, event){\n// \t$notification = target.find('.product-counter__notification');\n// \t$notification.css({ 'left' : event.clientX, 'top' : event.clientY - $notification.outerHeight() })\n// }\n\n\nfunction showTip(target, type) {\n  $('body').find('.product-counter__notification_max').hide();\n  $('body').find('.product-counter__notification_min').hide();\n\n  if (type) {\n    target.find('.product-counter__notification_max').show();\n    clearTimeout(timeout);\n    timeout = setTimeout(() => {\n      target.find('.product-counter__notification_max').hide();\n    }, 1000);\n  } else {\n    target.find('.product-counter__notification_min').show();\n    clearTimeout(timeout);\n    timeout = setTimeout(() => {\n      target.find('.product-counter__notification_min').hide();\n    }, 1000);\n  }\n}\n\nvar timeout;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/product-counter.js?");
$('body').on('click', '.product-counter__button', function (event) {
    var $input = $(this).parents('.product-counter').find('input');
    var val = parseFloat($input.val().replace(",", "."));
    var step = parseFloat($input.data('step').replace(",", "."));

    if ($(this).hasClass('product-counter__button_minus') && val >= step) $input.val(val - step);
    else $input.val(val + step);

    $(this).parents('.product-counter').find('input').change();

    // setCoords($(this).parents('.product-counter'), event);
});

$('body').on('change', '.product-counter input', function () {
    var val = parseFloat($(this).val().replace(",", "."));
    var min = parseFloat($(this).attr('min').replace(",", "."));
    var max = parseFloat($(this).attr('max').replace(",", "."));

    if (val > max)
        showTip($(this).parents('.product-counter'), 'max')

    if (val < min)
        showTip($(this).parents('.product-counter'))
    let result = (val > max) ? max : (val < min) ? min : val;
    console.log(min, '>', val, '>', max, '=', result)
    $(this).val(result);
    $(this).attr('value', result);
    updateFakeInput(this);
});

function updateFakeInput(target) {
    // let parent = target.closest('.product-counter')
    // unit = parent.find('.product-counter__original-input').data('unit'),
    // let val = parseInt((parent.querySelector('.product-counter__original-input').attributes.value.value).replace(",", "."));
    // console.log(parent.querySelector('input'));
    // let val = parseInt($(parent.querySelector('input')).val().replaceAll(",", '.'))
    // console.log('value', val)
    // parent.querySelector('.product-counter__fake-input').innerText = `${val}`;
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
document.querySelectorAll('.amount .product-counter input').forEach(input => {
    input.addEventListener('keydown', event => {
        if (event.keyCode === 13){
            event.preventDefault();
            const target = event.currentTarget || event.target;
            target.blur();
            return false;
        }
    })
})
/***/ }),

/***/ "./src/js/components/product-form.js":
/*!*******************************************!*\
  !*** ./src/js/components/product-form.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/product-form.js?");

/***/ }),

/***/ "./src/js/components/product-slider.js":
/*!*********************************************!*\
  !*** ./src/js/components/product-slider.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('.product-slider__container').slick({\n  slidesToShow: 1,\n  slidesToScroll: 1,\n  infinite: false,\n  arrows: false,\n  asNavFor: '.product-slider__carousel',\n  responsive: [{\n    breakpoint: 768,\n    settings: {\n      dots: true\n    }\n  }]\n});\n$('.product-slider__carousel').slick({\n  slidesToShow: 4,\n  asNavFor: '.product-slider__container',\n  arrows: false,\n  focusOnSelect: true\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/product-slider.js?");

/***/ }),

/***/ "./src/js/components/products-tabs.js":
/*!********************************************!*\
  !*** ./src/js/components/products-tabs.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('a[data-toggle=\"tab\"]').on('shown.bs.tab', function (e) {\n  $($(e.target).attr('href')).find('.product-card-body').each(function (item, el) {\n    cutProductText(el);\n  });\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/products-tabs.js?");

/***/ }),

/***/ "./src/js/components/range-slider-field.js":
/*!*************************************************!*\
  !*** ./src/js/components/range-slider-field.js ***!
  \*************************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\");\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);\n\n\nclass RangeSliderField {\n  constructor(container) {\n    this.container = jquery__WEBPACK_IMPORTED_MODULE_0___default()(container);\n    this.slider = this.container.find('.range-slider-field__slider');\n    this.inputs = this.container.find('.range-slider-field__inputs input');\n    this.minPrice = this.container.find('.range-slider-field__inputs .range-slider-field__min-price');\n    this.maxPrice = this.container.find('.range-slider-field__inputs .range-slider-field__max-price');\n    this.init();\n  }\n\n  initSlider() {\n    let self = this;\n    this.minPrice.val(String(this.slider.data(\"from\")).replace(/\\B(?=(\\d{3})+(?!\\d))/g, \" \"));\n    this.maxPrice.val(String(this.slider.data(\"to\")).replace(/\\B(?=(\\d{3})+(?!\\d))/g, \" \"));\n    this.slider.ionRangeSlider();\n    this.slider.on(\"change\", function (event) {\n      let $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),\n          _thisMin,\n          _thisMax,\n          value = $this.prop(\"value\").split(\";\");\n\n      _thisMin = value[0].replace(/ /g, \"\");\n      _thisMin = _thisMin.replace(/\\B(?=(\\d{3})+(?!\\d))/g, \" \");\n      _thisMax = value[1].replace(/ /g, \"\");\n      _thisMax = _thisMax.replace(/\\B(?=(\\d{3})+(?!\\d))/g, \" \");\n      self.minPrice.val(_thisMin);\n      self.maxPrice.val(_thisMax);\n      filterShowCounter(this, -4);\n    });\n  }\n\n  init() {\n    this.initSlider();\n  }\n\n}\n\njquery__WEBPACK_IMPORTED_MODULE_0___default()(\".range-slider-field\").each(function (elem) {\n  new RangeSliderField(elem);\n});\njquery__WEBPACK_IMPORTED_MODULE_0___default()(\"body\").on('change', '.range-slider-field__inputs input', function () {\n  filterShowCounter(this, -4);\n  let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).parents(\".range-slider-field\");\n  let $range_data = parent.find('.range-slider-field__slider').data(\"ionRangeSlider\");\n  $range_data.update({\n    from: parent.find(\".range-slider-field__min-price\").val().replace(' ', ''),\n    to: parent.find(\".range-slider-field__max-price\").val().replace(' ', '')\n  });\n});\njquery__WEBPACK_IMPORTED_MODULE_0___default()('body').on('input', '.range-slider-field__min-price', capacity);\njquery__WEBPACK_IMPORTED_MODULE_0___default()('body').on('input', '.range-slider-field__max-price', capacity);\n\nfunction capacity() {\n  this.value = this.value.replace(/[^\\d]/g, '');\n  this.value = this.value.replace(/ /g, \"\");\n  this.value = this.value.replace(/\\B(?=(\\d{3})+(?!\\d))/g, \" \");\n}\n\nwindow.RangeSliderField = RangeSliderField;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/range-slider-field.js?");

/***/ }),

/***/ "./src/js/components/scrollbar.js":
/*!****************************************!*\
  !*** ./src/js/components/scrollbar.js ***!
  \****************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! overlayscrollbars */ \"./node_modules/overlayscrollbars/js/OverlayScrollbars.js\");\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__);\n\nOverlayScrollbars(document.querySelectorAll(\".search-form__ajax-search > ul, .filters .scroll_content, .modal-order .order-table__body\"), {\n  autoUpdate: true,\n  overflowBehavior: {\n    x: \"hidden\",\n    y: \"scroll\"\n  }\n});\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/scrollbar.js?");

/***/ }),

/***/ "./src/js/components/search-form.js":
/*!******************************************!*\
  !*** ./src/js/components/search-form.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {function open(event) {\n  const search = document.querySelectorAll('.search-form')[1];\n  search.classList.add('active');\n}\n\nfunction close(event) {\n  const search = document.querySelectorAll('.search-form')[1];\n  search.classList.remove('active');\n}\n\nfunction check(event) {\n  const target = event.target.closest('.search-form');\n  console.log(target);\n\n  if (!target) {\n    close();\n    window.removeEventListener('click', check);\n  }\n}\n\n$('body').on('focusin', '.search-form__label input', function (event) {\n  // $('.search-form__ajax-search ul').stop().slideDown();\n  hideText($(this).closest('.search-form'));\n  open();\n  window.addEventListener('click', check);\n});\n$('body').on('mouseleave', '.search-form', function (event) {\n  // $('.search-form__ajax-search ul').stop().slideUp();\n  showText($(this).closest('.search-form'));\n});\n$('body').on('click', '.search-form__label-text', function (event) {\n  hideText($(this).closest('.search-form'));\n  $(this).closest('.search-form').find('input').focus(); // $('.search-form__ajax-search ul').slideDown();\n});\n\nfunction showText(searchForm) {\n  if ($(searchForm).find('input').val().length < 1) {\n    $(searchForm).find('.search-form__label-text').css('display', 'flex');\n  }\n}\n\nfunction hideText(searchForm) {\n  $(searchForm).find('.search-form__label-text').css('display', 'none');\n}\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/search-form.js?");

/***/ }),

/***/ "./src/js/components/select-tabs.js":
/*!******************************************!*\
  !*** ./src/js/components/select-tabs.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\"body\").on('click', '.select-tabs__list-trigger', function () {\n  $(this).toggleClass('focused');\n  $(this).closest('.select-tabs').find('.select-tabs__list').stop(false).slideToggle();\n});\n$('.select-tabs a[data-toggle=\"tab\"]').on('shown.bs.tab', function (e) {\n  $(\".contacts-block__map-container.active\").removeClass('active');\n  $($(this).data('map')).addClass('active');\n  $(this).closest('.select-tabs').find('.select-tabs__list a.active').removeClass('active');\n  $(this).addClass('active');\n  $(this).closest('.select-tabs').find('.select-tabs__list-trigger').text($(this).text());\n});\n$(document).on('focusout', \".select-tabs__list-trigger\", function () {\n  $(this).closest('.select-tabs').find('.select-tabs__list').slideUp();\n  $(this).removeClass('focused');\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/select-tabs.js?");

/***/ }),

/***/ "./src/js/components/seo-scroller.js":
/*!*******************************************!*\
  !*** ./src/js/components/seo-scroller.js ***!
  \*******************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! overlayscrollbars */ \"./node_modules/overlayscrollbars/js/OverlayScrollbars.js\");\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(overlayscrollbars__WEBPACK_IMPORTED_MODULE_0__);\n\n/*  Обработка картинок в сео-блоке  */\n\n$(\".seo-scroller\").each(function () {\n  var $wrapper = $(this).find(\".seo-scroller__seo-images\");\n  var $images = $wrapper.find(\"img\");\n\n  if ($images.length === 1) {\n    $images.each(function (i, e) {\n      $wrapper.append(\"<div class='seo_img large'>\" + $(e)[0].outerHTML + \"</div>\");\n      $(e).remove();\n    });\n  } else if ($images.length === 2) {\n    var count = 0;\n    $images.each(function (i, e) {\n      if (!count) {\n        $wrapper.append(\"<div class='img_row'><div class='seo_img big'>\" + $(e)[0].outerHTML + \"</div></div>\");\n      } else {\n        $wrapper.append(\"<div class='seo_img big'>\" + $(e)[0].outerHTML + \"</div>\");\n      }\n\n      $(e).remove();\n      count++;\n    });\n  } else if ($images.length === 3) {\n    var count = 0;\n    $wrapper.append(\"<div class='img_row'></div>\");\n    $images.each(function (i, e) {\n      if (count !== 2) {\n        $wrapper.find(\".img_row\").append(\"<div class='seo_img'>\" + $(e)[0].outerHTML + \"</div>\");\n      } else {\n        $wrapper.append(\"<div class='seo_img big'>\" + $(e)[0].outerHTML + \"</div>\");\n      }\n\n      $(e).remove();\n      count++;\n    });\n  } else {\n    $images.each(function (i, e) {\n      $wrapper.append(\"<div class='img_row'><div class='seo_img big'>\" + $(e)[0].outerHTML + \"</div></div>\");\n      $(e).remove();\n    });\n  }\n});\nOverlayScrollbars(document.querySelectorAll(\".seo-scroller__seo-text\"), {\n  autoUpdate: true,\n  overflowBehavior: {\n    x: \"hidden\",\n    y: \"scroll\"\n  }\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/seo-scroller.js?");

/***/ }),

/***/ "./src/js/components/shop-button.js":
/*!******************************************!*\
  !*** ./src/js/components/shop-button.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("class ShopButton {\n  constructor(button) {\n    this.button = button;\n    this.counter = this.button.querySelector(\".shop-button__count\");this.counterMob = document.querySelector(\".shop-button__count-mob\");\n    this.initState();\n  }\n\n  changeCount(num) {\n    this.counter.innerHTML = parseInt(num);this.counterMob.innerHTML = parseInt(num);\n    this.initState();\n  }\n\n  initState() {\n    if (this.counter.innerText === \"\" || parseInt(this.counter.innerText) <= 0) {\n      this.counter.classList.remove(\"filled\");\n    } else {\n      this.counter.classList.add(\"filled\");\n    }\n  }\n\n}\n\nlet cardButton = null;\nlet compareButton = null;\nlet favoritesButton = null;\n\nfunction initShopButtons() {\n  cardButton = new ShopButton(document.querySelector(\".cart-button\")); // compareButton = new ShopButton(document.querySelector(\".compare-button\"))\n\n  favoritesButton = new ShopButton(document.querySelector(\".favorites-button\"));\n}\n\ninitShopButtons(); /////////\n// API //\n/////////\n\nfunction changeCartCount(num) {\n  cardButton.changeCount(num);\n  return cardButton;\n}\n\nfunction changeCompareCount(num) {\n  compareButton.changeCount(num);\n  return compareButton;\n}\n\nfunction changeFavoritesCount(num) {\n  favoritesButton.changeCount(num);\n  return favoritesButton;\n} // Variables\n\n\nwindow.cardButton = cardButton;\nwindow.compareButton = compareButton;\nwindow.favoritesButton = favoritesButton; // Functions\n\nwindow.changeCartCount = changeCartCount;\nwindow.changeCompareCount = changeCompareCount;\nwindow.changeFavoritesCount = changeFavoritesCount;\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/shop-button.js?");

/***/ }),

/***/ "./src/js/components/short-slider.js":
/*!*******************************************!*\
  !*** ./src/js/components/short-slider.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\".short-slider\").slick({\n  slidesToShow: 1,\n  slidesToShow: 1,\n  autoplay: true,\n  autoplaySpeed: 3000,\n  infinite: true,\n  arrows: true,\n  dots: true,\n  prevArrow: '<span class=\"short-slider__arrow short-slider__arrow_prev\"><svg role=\"img\" width=\"9\" height=\"11\"><use xlink:href=\"/static/images/sprite.svg#slider-arr\"></use></svg></span>',\n  nextArrow: '<span class=\"short-slider__arrow short-slider__arrow_next\"><svg role=\"img\" width=\"9\" height=\"11\"><use xlink:href=\"/static/images/sprite.svg#slider-arr\"></use></svg></span>'\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/short-slider.js?");

/***/ }),

/***/ "./src/js/components/sidebar-helper.js":
/*!*********************************************!*\
  !*** ./src/js/components/sidebar-helper.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\"body\").on('click', '.sidebar-helper', function () {\n  $(\"body, i.modal_bg\").addClass('opened');\n  $($(this).attr('href')).addClass('opened');\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/sidebar-helper.js?");

/***/ }),

/***/ "./src/js/components/sort-parameters.js":
/*!**********************************************!*\
  !*** ./src/js/components/sort-parameters.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\"body\").on('click', '.sort-parameters__layout-types button', function () {\n  $(\".sort-parameters__layout-types button.active\").removeClass(\"active\");\n  $(this).addClass(\"active\");\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/sort-parameters.js?");

/***/ }),

/***/ "./src/js/components/stock-block.js":
/*!******************************************!*\
  !*** ./src/js/components/stock-block.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$('.index-row_stock .wrapper').slick({\n  infinite: false,\n  centerMode: false,\n  centerPadding: '0px',\n  slidesToShow: 2,\n  responsive: [{\n    breakpoint: 992,\n    settings: {\n      arrows: false,\n      centerMode: true,\n      centerPadding: '15%',\n      adaptiveHeight: true,\n      slidesToShow: 1\n    }\n  }]\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/stock-block.js?");

/***/ }),

/***/ "./src/js/components/variation-table.js":
/*!**********************************************!*\
  !*** ./src/js/components/variation-table.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function($) {$(\"body\").on('change', '.variation-table .product-counter__original-input', function () {\n  var sum = 0;\n  console.log('sum', Number($(el).find('.variations-table-col_price.price-c').data('price')));\n  $(\".variation-table .variations-table-row\").each(function (i, el) {\n    let count = Number($(el).find('.product-counter__fake-input').text());\n    count = count ? count : 0;\n    let price = Number($(el).find('.variations-table-col_price.price-c').data('price'));\n    sum += count * price;\n  });\n  $(\".variation-table .variations-table_price-value\").text(sum.toLocaleString());\n});\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/components/variation-table.js?");

/***/ }),

/***/ "./src/js/index.js":
/*!*************************!*\
  !*** ./src/js/index.js ***!
  \*************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _vendors__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./vendors */ \"./src/js/vendors.js\");\n/* harmony import */ var _components_header__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/header */ \"./src/js/components/header.js\");\n/* harmony import */ var _components_header__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_components_header__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _components_mobile_menu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/mobile-menu */ \"./src/js/components/mobile-menu.js\");\n/* harmony import */ var _components_mobile_menu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_components_mobile_menu__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _components_shop_button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/shop-button */ \"./src/js/components/shop-button.js\");\n/* harmony import */ var _components_shop_button__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_components_shop_button__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _components_product_card__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/product-card */ \"./src/js/components/product-card.js\");\n/* harmony import */ var _components_product_card__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_components_product_card__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _components_mini_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/mini-button */ \"./src/js/components/mini-button.js\");\n/* harmony import */ var _components_mini_button__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_components_mini_button__WEBPACK_IMPORTED_MODULE_5__);\n/* harmony import */ var _components_cut_articles_text__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/cut-articles-text */ \"./src/js/components/cut-articles-text.js\");\n/* harmony import */ var _components_cut_articles_text__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_components_cut_articles_text__WEBPACK_IMPORTED_MODULE_6__);\n/* harmony import */ var _components_map__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/map */ \"./src/js/components/map.js\");\n/* harmony import */ var _components_map__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_components_map__WEBPACK_IMPORTED_MODULE_7__);\n/* harmony import */ var _components_content_text__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/content-text */ \"./src/js/components/content-text.js\");\n/* harmony import */ var _components_content_text__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_components_content_text__WEBPACK_IMPORTED_MODULE_8__);\n/* harmony import */ var _components_input_tel__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/input-tel */ \"./src/js/components/input-tel.js\");\n/* harmony import */ var _components_input_tel__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_components_input_tel__WEBPACK_IMPORTED_MODULE_9__);\n/* harmony import */ var _components_cart__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/cart */ \"./src/js/components/cart.js\");\n/* harmony import */ var _components_footer_social_link__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./components/footer-social-link */ \"./src/js/components/footer-social-link.js\");\n/* harmony import */ var _components_footer_social_link__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_components_footer_social_link__WEBPACK_IMPORTED_MODULE_11__);\n/* harmony import */ var _components_compare_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./components/compare-component */ \"./src/js/components/compare-component.js\");\n/* harmony import */ var _components_compare_component__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_components_compare_component__WEBPACK_IMPORTED_MODULE_12__);\n/* harmony import */ var _components_range_slider_field__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./components/range-slider-field */ \"./src/js/components/range-slider-field.js\");\n/* harmony import */ var _components_pagination__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./components/pagination */ \"./src/js/components/pagination.js\");\n/* harmony import */ var _components_pagination__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_components_pagination__WEBPACK_IMPORTED_MODULE_14__);\n/* harmony import */ var _components_form__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./components/form */ \"./src/js/components/form.js\");\n/* harmony import */ var _components_form__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_components_form__WEBPACK_IMPORTED_MODULE_15__);\n/* harmony import */ var _components_mobile_filters_trigger__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./components/mobile-filters-trigger */ \"./src/js/components/mobile-filters-trigger.js\");\n/* harmony import */ var _components_mobile_filters_trigger__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_components_mobile_filters_trigger__WEBPACK_IMPORTED_MODULE_16__);\n/* harmony import */ var _components_nav_close__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./components/nav-close */ \"./src/js/components/nav-close.js\");\n/* harmony import */ var _components_nav_close__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_components_nav_close__WEBPACK_IMPORTED_MODULE_17__);\n/* harmony import */ var _components_sidebar_helper__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./components/sidebar-helper */ \"./src/js/components/sidebar-helper.js\");\n/* harmony import */ var _components_sidebar_helper__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_components_sidebar_helper__WEBPACK_IMPORTED_MODULE_18__);\n/* harmony import */ var _components_filters__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./components/filters */ \"./src/js/components/filters.js\");\n/* harmony import */ var _components_filters__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_components_filters__WEBPACK_IMPORTED_MODULE_19__);\n/* harmony import */ var _components_catalog__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./components/catalog */ \"./src/js/components/catalog.js\");\n/* harmony import */ var _components_filter_block__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./components/filter-block */ \"./src/js/components/filter-block.js\");\n/* harmony import */ var _components_filter_block__WEBPACK_IMPORTED_MODULE_21___default = /*#__PURE__*/__webpack_require__.n(_components_filter_block__WEBPACK_IMPORTED_MODULE_21__);\n/* harmony import */ var _components_filter_counter__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./components/filter-counter */ \"./src/js/components/filter-counter.js\");\n/* harmony import */ var _components_filter_counter__WEBPACK_IMPORTED_MODULE_22___default = /*#__PURE__*/__webpack_require__.n(_components_filter_counter__WEBPACK_IMPORTED_MODULE_22__);\n/* harmony import */ var _components_loading_blocks__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./components/loading-blocks */ \"./src/js/components/loading-blocks.js\");\n/* harmony import */ var _components_loading_blocks__WEBPACK_IMPORTED_MODULE_23___default = /*#__PURE__*/__webpack_require__.n(_components_loading_blocks__WEBPACK_IMPORTED_MODULE_23__);\n/* harmony import */ var _components_catalog_categories__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./components/catalog-categories */ \"./src/js/components/catalog-categories.js\");\n/* harmony import */ var _components_catalog_categories__WEBPACK_IMPORTED_MODULE_24___default = /*#__PURE__*/__webpack_require__.n(_components_catalog_categories__WEBPACK_IMPORTED_MODULE_24__);\n/* harmony import */ var _components_sort_parameters__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./components/sort-parameters */ \"./src/js/components/sort-parameters.js\");\n/* harmony import */ var _components_sort_parameters__WEBPACK_IMPORTED_MODULE_25___default = /*#__PURE__*/__webpack_require__.n(_components_sort_parameters__WEBPACK_IMPORTED_MODULE_25__);\n/* harmony import */ var _components_scrollbar__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./components/scrollbar */ \"./src/js/components/scrollbar.js\");\n/* harmony import */ var _components_extra_products_slider__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ./components/extra-products-slider */ \"./src/js/components/extra-products-slider.js\");\n/* harmony import */ var _components_extra_products_slider__WEBPACK_IMPORTED_MODULE_27___default = /*#__PURE__*/__webpack_require__.n(_components_extra_products_slider__WEBPACK_IMPORTED_MODULE_27__);\n/* harmony import */ var _components_product_slider__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! ./components/product-slider */ \"./src/js/components/product-slider.js\");\n/* harmony import */ var _components_product_slider__WEBPACK_IMPORTED_MODULE_28___default = /*#__PURE__*/__webpack_require__.n(_components_product_slider__WEBPACK_IMPORTED_MODULE_28__);\n/* harmony import */ var _components_product_form__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! ./components/product-form */ \"./src/js/components/product-form.js\");\n/* harmony import */ var _components_product_form__WEBPACK_IMPORTED_MODULE_29___default = /*#__PURE__*/__webpack_require__.n(_components_product_form__WEBPACK_IMPORTED_MODULE_29__);\n/* harmony import */ var _components_product_amount__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! ./components/product-amount */ \"./src/js/components/product-amount.js\");\n/* harmony import */ var _components_product_amount__WEBPACK_IMPORTED_MODULE_30___default = /*#__PURE__*/__webpack_require__.n(_components_product_amount__WEBPACK_IMPORTED_MODULE_30__);\n/* harmony import */ var _components_stock_block__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! ./components/stock-block */ \"./src/js/components/stock-block.js\");\n/* harmony import */ var _components_stock_block__WEBPACK_IMPORTED_MODULE_31___default = /*#__PURE__*/__webpack_require__.n(_components_stock_block__WEBPACK_IMPORTED_MODULE_31__);\n/* harmony import */ var _components_modal__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! ./components/modal */ \"./src/js/components/modal.js\");\n/* harmony import */ var _components_modal__WEBPACK_IMPORTED_MODULE_32___default = /*#__PURE__*/__webpack_require__.n(_components_modal__WEBPACK_IMPORTED_MODULE_32__);\n/* harmony import */ var _components_mobile_search_trigger__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! ./components/mobile-search-trigger */ \"./src/js/components/mobile-search-trigger.js\");\n/* harmony import */ var _components_mobile_search_trigger__WEBPACK_IMPORTED_MODULE_33___default = /*#__PURE__*/__webpack_require__.n(_components_mobile_search_trigger__WEBPACK_IMPORTED_MODULE_33__);\n/* harmony import */ var _components_search_form__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! ./components/search-form */ \"./src/js/components/search-form.js\");\n/* harmony import */ var _components_search_form__WEBPACK_IMPORTED_MODULE_34___default = /*#__PURE__*/__webpack_require__.n(_components_search_form__WEBPACK_IMPORTED_MODULE_34__);\n/* harmony import */ var _components_checkout_form__WEBPACK_IMPORTED_MODULE_35__ = __webpack_require__(/*! ./components/checkout-form */ \"./src/js/components/checkout-form.js\");\n/* harmony import */ var _components_checkout_form__WEBPACK_IMPORTED_MODULE_35___default = /*#__PURE__*/__webpack_require__.n(_components_checkout_form__WEBPACK_IMPORTED_MODULE_35__);\n/* harmony import */ var _components_autocomplete_address__WEBPACK_IMPORTED_MODULE_36__ = __webpack_require__(/*! ./components/autocomplete-address */ \"./src/js/components/autocomplete-address.js\");\n/* harmony import */ var _components_short_slider__WEBPACK_IMPORTED_MODULE_37__ = __webpack_require__(/*! ./components/short-slider */ \"./src/js/components/short-slider.js\");\n/* harmony import */ var _components_short_slider__WEBPACK_IMPORTED_MODULE_37___default = /*#__PURE__*/__webpack_require__.n(_components_short_slider__WEBPACK_IMPORTED_MODULE_37__);\n/* harmony import */ var _components_seo_scroller__WEBPACK_IMPORTED_MODULE_38__ = __webpack_require__(/*! ./components/seo-scroller */ \"./src/js/components/seo-scroller.js\");\n/* harmony import */ var _components_products_tabs__WEBPACK_IMPORTED_MODULE_39__ = __webpack_require__(/*! ./components/products-tabs */ \"./src/js/components/products-tabs.js\");\n/* harmony import */ var _components_products_tabs__WEBPACK_IMPORTED_MODULE_39___default = /*#__PURE__*/__webpack_require__.n(_components_products_tabs__WEBPACK_IMPORTED_MODULE_39__);\n/* harmony import */ var _components_product_counter__WEBPACK_IMPORTED_MODULE_40__ = __webpack_require__(/*! ./components/product-counter */ \"./src/js/components/product-counter.js\");\n/* harmony import */ var _components_product_counter__WEBPACK_IMPORTED_MODULE_40___default = /*#__PURE__*/__webpack_require__.n(_components_product_counter__WEBPACK_IMPORTED_MODULE_40__);\n/* harmony import */ var _components_variation_table__WEBPACK_IMPORTED_MODULE_41__ = __webpack_require__(/*! ./components/variation-table */ \"./src/js/components/variation-table.js\");\n/* harmony import */ var _components_variation_table__WEBPACK_IMPORTED_MODULE_41___default = /*#__PURE__*/__webpack_require__.n(_components_variation_table__WEBPACK_IMPORTED_MODULE_41__);\n/* harmony import */ var _components_select_tabs__WEBPACK_IMPORTED_MODULE_42__ = __webpack_require__(/*! ./components/select-tabs */ \"./src/js/components/select-tabs.js\");\n/* harmony import */ var _components_select_tabs__WEBPACK_IMPORTED_MODULE_42___default = /*#__PURE__*/__webpack_require__.n(_components_select_tabs__WEBPACK_IMPORTED_MODULE_42__);\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/index.js?");

/***/ }),

/***/ "./src/js/mask.js":
/*!************************!*\
  !*** ./src/js/mask.js ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function(jQuery) {//mask\n(function (e) {\n  function t() {\n    var e = document.createElement(\"input\"),\n        t = \"onpaste\";\n    return e.setAttribute(t, \"\"), \"function\" == typeof e[t] ? \"paste\" : \"input\";\n  }\n\n  var n,\n      a = t() + \".mask\",\n      r = navigator.userAgent,\n      i = /iphone/i.test(r),\n      o = /android/i.test(r);\n  e.mask = {\n    definitions: {\n      9: \"[0-9]\",\n      a: \"[A-Za-z]\",\n      \"*\": \"[A-Za-z0-9]\"\n    },\n    dataName: \"rawMaskFn\",\n    placeholder: \"_\"\n  }, e.fn.extend({\n    caret: function (e, t) {\n      var n;\n      if (0 !== this.length && !this.is(\":hidden\")) return \"number\" == typeof e ? (t = \"number\" == typeof t ? t : e, this.each(function () {\n        this.setSelectionRange ? this.setSelectionRange(e, t) : this.createTextRange && (n = this.createTextRange(), n.collapse(!0), n.moveEnd(\"character\", t), n.moveStart(\"character\", e), n.select());\n      })) : (this[0].setSelectionRange ? (e = this[0].selectionStart, t = this[0].selectionEnd) : document.selection && document.selection.createRange && (n = document.selection.createRange(), e = 0 - n.duplicate().moveStart(\"character\", -1e5), t = e + n.text.length), {\n        begin: e,\n        end: t\n      });\n    },\n    unmask: function () {\n      return this.trigger(\"unmask\");\n    },\n    mask: function (t, r) {\n      var c, l, s, u, f, h;\n      return !t && this.length > 0 ? (c = e(this[0]), c.data(e.mask.dataName)()) : (r = e.extend({\n        placeholder: e.mask.placeholder,\n        completed: null\n      }, r), l = e.mask.definitions, s = [], u = h = t.length, f = null, e.each(t.split(\"\"), function (e, t) {\n        \"?\" == t ? (h--, u = e) : l[t] ? (s.push(RegExp(l[t])), null === f && (f = s.length - 1)) : s.push(null);\n      }), this.trigger(\"unmask\").each(function () {\n        function c(e) {\n          for (; h > ++e && !s[e];);\n\n          return e;\n        }\n\n        function d(e) {\n          for (; --e >= 0 && !s[e];);\n\n          return e;\n        }\n\n        function m(e, t) {\n          var n, a;\n\n          if (!(0 > e)) {\n            for (n = e, a = c(t); h > n; n++) if (s[n]) {\n              if (!(h > a && s[n].test(R[a]))) break;\n              R[n] = R[a], R[a] = r.placeholder, a = c(a);\n            }\n\n            b(), x.caret(Math.max(f, e));\n          }\n        }\n\n        function p(e) {\n          var t, n, a, i;\n\n          for (t = e, n = r.placeholder; h > t; t++) if (s[t]) {\n            if (a = c(t), i = R[t], R[t] = n, !(h > a && s[a].test(i))) break;\n            n = i;\n          }\n        }\n\n        function g(e) {\n          var t,\n              n,\n              a,\n              r = e.which;\n          8 === r || 46 === r || i && 127 === r ? (t = x.caret(), n = t.begin, a = t.end, 0 === a - n && (n = 46 !== r ? d(n) : a = c(n - 1), a = 46 === r ? c(a) : a), k(n, a), m(n, a - 1), e.preventDefault()) : 27 == r && (x.val(S), x.caret(0, y()), e.preventDefault());\n        }\n\n        function v(t) {\n          var n,\n              a,\n              i,\n              l = t.which,\n              u = x.caret();\n          t.ctrlKey || t.altKey || t.metaKey || 32 > l || l && (0 !== u.end - u.begin && (k(u.begin, u.end), m(u.begin, u.end - 1)), n = c(u.begin - 1), h > n && (a = String.fromCharCode(l), s[n].test(a) && (p(n), R[n] = a, b(), i = c(n), o ? setTimeout(e.proxy(e.fn.caret, x, i), 0) : x.caret(i), r.completed && i >= h && r.completed.call(x))), t.preventDefault());\n        }\n\n        function k(e, t) {\n          var n;\n\n          for (n = e; t > n && h > n; n++) s[n] && (R[n] = r.placeholder);\n        }\n\n        function b() {\n          x.val(R.join(\"\"));\n        }\n\n        function y(e) {\n          var t,\n              n,\n              a = x.val(),\n              i = -1;\n\n          for (t = 0, pos = 0; h > t; t++) if (s[t]) {\n            for (R[t] = r.placeholder; pos++ < a.length;) if (n = a.charAt(pos - 1), s[t].test(n)) {\n              R[t] = n, i = t;\n              break;\n            }\n\n            if (pos > a.length) break;\n          } else R[t] === a.charAt(pos) && t !== u && (pos++, i = t);\n\n          return e ? b() : u > i + 1 ? (x.val(\"\"), k(0, h)) : (b(), x.val(x.val().substring(0, i + 1))), u ? t : f;\n        }\n\n        var x = e(this),\n            R = e.map(t.split(\"\"), function (e) {\n          return \"?\" != e ? l[e] ? r.placeholder : e : void 0;\n        }),\n            S = x.val();\n        x.data(e.mask.dataName, function () {\n          return e.map(R, function (e, t) {\n            return s[t] && e != r.placeholder ? e : null;\n          }).join(\"\");\n        }), x.attr(\"readonly\") || x.one(\"unmask\", function () {\n          x.unbind(\".mask\").removeData(e.mask.dataName);\n        }).bind(\"focus.mask\", function () {\n          clearTimeout(n);\n          var e;\n          S = x.val(), e = y(), n = setTimeout(function () {\n            b(), e == t.length ? x.caret(0, e) : x.caret(e);\n          }, 10);\n        }).bind(\"blur.mask\", function () {\n          y(), x.val() != S && x.change();\n        }).bind(\"keydown.mask\", g).bind(\"keypress.mask\", v).bind(a, function () {\n          setTimeout(function () {\n            var e = y(!0);\n            x.caret(e), r.completed && e == x.val().length && r.completed.call(x);\n          }, 0);\n        }), y();\n      }));\n    }\n  });\n})(jQuery);\n\nfunction _defineProperties(target, props) {\n  for (var i = 0; i < props.length; i++) {\n    var descriptor = props[i];\n    descriptor.enumerable = descriptor.enumerable || false;\n    descriptor.configurable = true;\n    if (\"value\" in descriptor) descriptor.writable = true;\n    Object.defineProperty(target, descriptor.key, descriptor);\n  }\n}\n\nfunction _createClass(Constructor, protoProps, staticProps) {\n  if (protoProps) _defineProperties(Constructor.prototype, protoProps);\n  if (staticProps) _defineProperties(Constructor, staticProps);\n  return Constructor;\n}\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/mask.js?");

/***/ }),

/***/ "./src/js/utils.js":
/*!*************************!*\
  !*** ./src/js/utils.js ***!
  \*************************/
/*! exports provided: parseHTML, parseArrayHTML, offset, svgRepairUse, createSVG, request, serialize */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"parseHTML\", function() { return parseHTML; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"parseArrayHTML\", function() { return parseArrayHTML; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"offset\", function() { return offset; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"svgRepairUse\", function() { return svgRepairUse; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"createSVG\", function() { return createSVG; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"request\", function() { return request; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"serialize\", function() { return serialize; });\n/**\n * Парсер HTML строки для ее перевода в HTML элементы\n * @param {string} markup HTML в виде строки\n * @returns {HTMLElement | Array<HTMLElement>} HTML элементы\n */\nfunction parseHTML(markup) {\n  var parser = new DOMParser();\n  var body = parser.parseFromString(markup, \"text/html\").body;\n\n  if (body.children.length > 1) {\n    var elements = new Array();\n    Array.prototype.slice.call(body.children).forEach(function (item) {\n      elements.push(item);\n    });\n    return elements;\n  } else {\n    return body.firstChild;\n  }\n}\n/**\n * Парсер массива HTML строк для перевода в массив HTML элементов\n * @param {Array<string>} markups Массив с html в виде строк\n */\n\nfunction parseArrayHTML(markups) {\n  var _this = this;\n\n  var elements = Array();\n  markups.forEach(function (markup) {\n    elements.push(_this.parseHTML(markup));\n  });\n  return elements;\n}\n/**\n * Получение отступов по документу\n * @param {HTMLElement} element\n */\n\nfunction offset(element) {\n  var rect = element.getBoundingClientRect(),\n      scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;\n  scrollTop = window.pageYOffset || document.documentElement.scrollTop;\n  return {\n    top: rect.top + scrollTop,\n    left: rect.left + scrollLeft\n  };\n}\n/**\n * Пересоздание тегов use в svg'шках\n * Помогает при выводе svg спрайтов ajax загрузки страницы\n */\n\nfunction svgRepairUse() {\n  const allSVG = Array.prototype.slice.call(document.querySelectorAll('svg'));\n  allSVG.forEach(function (svg) {\n    if (svg.firstElementChild.href !== undefined) {\n      const href = svg.firstElementChild.href.baseVal;\n      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');\n      use.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', href);\n      svg.firstElementChild.remove();\n      svg.appendChild(use);\n    }\n  });\n}\n/**\n * Создание svg элемента в документе\n * @param {string} href ссылка на svg\n * @param {string} className класс для svg элемента\n * @returns {SVGElement} svg элемент\n */\n\nfunction createSVG(href, className = '') {\n  const svg = document.createElementNS(\"http://www.w3.org/2000/svg\", \"svg\");\n  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');\n  use.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', href);\n  svg.classList.add(className);\n  svg.appendChild(use);\n  return svg;\n}\nfunction request(data, action, method, success = function (response) {}, error = function (error) {}) {\n  const url = new URL(action);\n  method = method.toLowerCase();\n  if (method == 'get') url.search = data;\n  return new Promise(function (resolve, reject) {\n    const xhr = new XMLHttpRequest();\n    xhr.open(method, url.href, true);\n\n    if (method === 'post') {\n      if (typeof data === 'string') {\n        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\n      }\n    }\n\n    xhr.setRequestHeader(\"X-Requested-With\", \"XMLHttpRequest\");\n\n    xhr.onload = function () {\n      if (this.status == 200) {\n        resolve(JSON.parse(this.response));\n      } else {\n        const err = new Error(this.statusText);\n        err.code = this.status;\n        reject(err);\n      }\n    };\n\n    xhr.send(data);\n  }).then(success, error);\n}\nfunction serialize(form) {\n  const formData = new FormData(form);\n  const arrayData = new Array();\n  const data = new String();\n\n  for (var item of formData.entries()) {\n    arrayData.push(item);\n  }\n\n  arrayData.forEach(function (item, index) {\n    if (index) data += '&';\n    data += item[0] + '=' + encodeURIComponent(item[1]);\n  });\n  return data;\n}\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/utils.js?");

/***/ }),

/***/ "./src/js/vendors.js":
/*!***************************!*\
  !*** ./src/js/vendors.js ***!
  \***************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\");\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _mask__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./mask */ \"./src/js/mask.js\");\n/* harmony import */ var _mask__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mask__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! bootstrap */ \"./node_modules/bootstrap/dist/js/bootstrap.js\");\n/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(bootstrap__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var dotdotdot__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! dotdotdot */ \"./node_modules/dotdotdot/src/js/jquery.dotdotdot.js\");\n/* harmony import */ var dotdotdot__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(dotdotdot__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! overlayscrollbars */ \"./node_modules/overlayscrollbars/js/OverlayScrollbars.js\");\n/* harmony import */ var overlayscrollbars__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(overlayscrollbars__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var ion_rangeslider__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ion-rangeslider */ \"./node_modules/ion-rangeslider/js/ion.rangeSlider.js\");\n/* harmony import */ var ion_rangeslider__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(ion_rangeslider__WEBPACK_IMPORTED_MODULE_5__);\n/* harmony import */ var slick_carousel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! slick-carousel */ \"./node_modules/slick-carousel/slick/slick.js\");\n/* harmony import */ var slick_carousel__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(slick_carousel__WEBPACK_IMPORTED_MODULE_6__);\n/* harmony import */ var _fancyapps_fancybox_dist_jquery_fancybox_min_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @fancyapps/fancybox/dist/jquery.fancybox.min.js */ \"./node_modules/@fancyapps/fancybox/dist/jquery.fancybox.min.js\");\n/* harmony import */ var _fancyapps_fancybox_dist_jquery_fancybox_min_js__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_fancyapps_fancybox_dist_jquery_fancybox_min_js__WEBPACK_IMPORTED_MODULE_7__);\n/* harmony import */ var svg_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! svg.js */ \"./node_modules/svg.js/dist/svg.js\");\n/* harmony import */ var svg_js__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(svg_js__WEBPACK_IMPORTED_MODULE_8__);\n // import \"jquery-mask-plugin\"\n\n\n\n\n\n\n\n\n\nwindow.$ = $;\nwindow.jQuery = $;\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\")))\n\n//# sourceURL=webpack://%5Bname%5D/./src/js/vendors.js?");

/***/ })

/******/ });