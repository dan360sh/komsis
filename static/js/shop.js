function sort_filter(reverse) {
  console.log("sort_filter");
  let filter_group = document.querySelectorAll(".filter-group");
  Array.prototype.slice.call(filter_group).forEach(function (item, i, arr) {
    nodeList = item.querySelectorAll(".custom-control");
    // console.log(nodeList)
    if (nodeList.length > 0) {
      var itemsArray = [];
      var parent = nodeList[0].parentNode;

      for (var i = 0; i < nodeList.length; i++) {
        itemsArray.push(parent.removeChild(nodeList[i]));
      }

      // console.log(itemsArray)
      itemsArray
        .sort(function (nodeA, nodeB) {
          var textA = nodeA.querySelector(
            "label.custom-control-label"
          ).textContent;
          var textB = nodeB.querySelector(
            "label.custom-control-label"
          ).textContent;
          var numberA = parseInt(textA);
          var numberB = parseInt(textB);
          if (numberA < numberB) {
            return reverse ? 1 : -1;
          }
          if (numberA > numberB) {
            return reverse ? -1 : 1;
          }
          return 0;
        })

        .forEach(function (node) {
          parent.appendChild(node);
        });
    }
  });
}

function getQueryParameters() {
  let result = {};
  if (location.search)
    location.search
      .substr(1)
      .split("&")
      .forEach(function (item) {
        var s = item.split("="),
          k = s[0],
          v = s[1] && decodeURIComponent(s[1]); //  null-coalescing / short-circuit
        //(k in qd) ? qd[k].push(v) : qd[k] = [v]
        (result[k] = result[k] || []).push(v); // null-coalescing / short-circuit
      });
  return result;
}

function get_get_query(more) {
  more = more || false;
  // var filters = $('form.filtering').serialize().split('%20').join('');
  let filters = $("form.filtering").serialize();
  filters = filters.split("&");
  let keys = filters.map((elem) => {
    let value = elem.split("=")[0];
    return value;
  });
  if (keys.includes("categories") && keys.includes("category")) {
    let index = keys.indexOf("categories");
    filters.splice(index, 1);
  }
  if (filters[0].match("search=")) {
    filters =
      filters[0] + "&" + filters.slice(1).join("&").split("%20").join("");
  } else {
    filters = filters.join("&").split("%20").join("");
  }
  var page = $(".pagination li.active a").attr("data-page");
  var sort = $("div.sort-parameters__order-by select").serialize();
  if (sort) {
    sort = "&" + sort;
  }
  var card_type = $(".sort-parameters__layout-types .active").attr("data-type");
  if (card_type) {
    card_type = "&card_type=" + card_type;
  }
  if (more) {
    page = $("#show_more").attr("data-page");
  }

  if (!page) page = 1;

  let salemode = false;
  let form_sale = document.querySelector("form.filtering input[name='sale']");
  if (form_sale && form_sale.checked) {
    // if (document.getElementById("salemode_flag").value == "true") {
    salemode = true;
    // }
  } else {
    document.getElementById("salemode_flag").value = "false";
  }
  let stockmode = false;
  let form_stock = document.querySelector("form.filtering input[name='stock']");
  if (form_stock && form_stock.checked) {
    // if (document.getElementById("stockmode_flag").value == "true")
    stockmode = true;
    document.getElementById("stockmode_flag").value = "true";
  } else {
    document.getElementById("stockmode_flag").value = "false";
  }
  let shockPriceMode = false;
  let formShock = document.querySelector("form.filtering input[name='shock']");
  if (formShock && formShock.checked) {
    shockPriceMode = true;
  }
  let result =
    filters +
    "&page=" +
    page +
    (sort ? sort : "") +
    (card_type ? card_type : "") +
    (salemode ? "&salemode" : "") +
    (stockmode ? "&stockmode" : "") +
    (shockPriceMode ? "&ch_117_664=on" : "");
  //   const queryParams = new URLSearchParams(window.location.search);
  //   const query = Object.fromEntries(queryParams.entries());
  //   for (let key in query) {
  //     if (key.startsWith("ch_")) {
  //       result += `&${key}=${query[key]}`;
  //     }
  //   }
  let params = new URLSearchParams(result);
  // var $sortsale = $('div.sort-parameters__order-by #sort-actions')
  // if ($('div.sort-parameters__order-by #sort-actions').prop('checked')) {
  //     params.set('sale', 'on');
  // }
  // if ($sortsale.prop('checked')){
  //     params.set('sale', 'on')
  // }
  // else if (!($sortsale.prop('checked')) || !(form_sale.checked)){
  //     params.delete('sale')
  // }
  // if ($sortsale.prop('checked') && salemode){
  //     params.set('sale', 'on')
  // }else{
  //     params.delete('sale')
  // }

  // var $sortstock = $('div.sort-parameters__order-by #sort-stock')
  // if ($sortstock.prop('checked')){
  //     params.set('stock', 'on');
  // }
  // else if (!($sortstock.prop('checked')) || !(form_stock.checked)){
  //     params.delete('stock')
  // }
  // if ($sortstock.prop('checked') && stockmode){
  //     params.set('stock', 'on')
  // }else{
  //     params.delete('stock')
  // }

  // else
  //     params.delete('stock');
  console.log(params.toString());
  return params.toString();
}

//execute filtering
function updateCatalog(
  event,
  first,
  reset = false,
  d_none = undefined,
  updatePrice = false
) {
  first = first || false;
  let query_string;
  toggleCatalogPreloader();
  if (event) {
    event.preventDefault();
  }
  if (!first) {
    query_string = get_get_query();
    if (reset) {
      query_string = "";
    }
    window.history.pushState(
      null,
      null,
      window.location.pathname + "?" + query_string
    );
  } else {
    query_string = window.location.search;
    query_string = query_string.substr(1);
  }
  query_string += "&ajax=Y";
  console.log("Строка запроса", query_string);
  $.ajax({
    url: window.location.pathname,
    type: "GET",
    dataType: "json",
    data: query_string,
    success: function (data) {
      console.log("Ответ:", query_string);
      console.log("info:", data);
      replaceCatalogData(event, data);
      let category = 0;
      if (d_none === undefined) {
        category = document.querySelector('input[name="category"]').value;
        if (category === "None") {
          category = 0;
        }
        d_none = Boolean(category);
      }
      if (d_none !== undefined) {
        if (
          document.querySelectorAll(".filter-category[data-category].active")
            .length
        ) {
          d_none = true;
        }
        document
          .querySelectorAll(".filter-category[data-category]")
          .forEach((item) => {
            if (d_none) {
              if (
                item.classList.contains("active") ||
                category.toString() === item.dataset.category.toString()
              ) {
                // item.closest('.place-accordion-item').classList.remove('d-none');
                // item.classList.remove('d-none');
              } else {
                item.closest(".place-accordion-item").classList.add("d-none");
              }
            } else {
              item.closest(".place-accordion-item").classList.remove("d-none");
            }
          });
      }
      d_none = undefined;
      let params = new URLSearchParams(query_string);
      console.log(data);
      // if (data.filters && data.filters.sale || data.sale) {
      //     const sort_hit = document.querySelectorAll('.sort-actions');
      //     sort_hit.forEach(element => {
      //         element.style.display = 'block';
      //     })
      //     // sort_hit.style.display = 'block';
      // }
      if (
        data.filters.attributes &&
        data.display_related_categories_and_filters
      ) {
        const headerAttributes = data.filters.attributes.filter(
          (elem) => elem.show_in_header
        );
        createHeaderFilters(headerAttributes);
      }
      if ((data.filters && data.filters.sale) || data.sale) {
        const sort_sale = document.querySelector("#sort-sale");
        sort_sale.style.display = "flex";
      }
      if ((data.filters && data.filters.stock) || data.stock) {
        // if(data.filters.stock){
        const sort_stock = document.querySelector("#sort-stock").parentElement;
        sort_stock.style.display = "flex";
      }
      // if ((data.filters && data.filters.shock_sale) || data.shock_sale) {
      //   const sortShockSale =
      //     document.querySelector("#sort-shock").parentElement;
      //   sortShockSale.style.display = "flex";
      // }
      if (data.active.sale || params.get("sale")) {
        let boxes = document.querySelectorAll('input[name="sale"]');
        boxes.forEach((box) => {
          box.checked = true;
        });
      }
      if (data.active.stock || params.get("stock")) {
        let boxes = document.querySelectorAll('input[name="stock"]');
        boxes.forEach((box) => {
          box.checked = true;
        });
      }
      if (
        data.filters.price_min !== undefined &&
        data.filters.price_max !== undefined &&
        updatePrice
      ) {
        let minPrice = !data.active.sale
          ? data.filters.price_min
          : data.filters.available_price_min;
        let maxPrice = !data.active.sale
          ? data.filters.price_max
          : data.filters.available_price_max;
        $(".range-slider-field__min-price").val(minPrice);
        $(".range-slider-field__max-price").val(maxPrice);
        let $range_data = $(".range-slider-field__slider").data(
          "ionRangeSlider"
        );
        $range_data.update({
          from: minPrice,
          to: maxPrice,
        });
        $(".filter-counter").fadeOut(0);
        let query = get_get_query();
        window.history.pushState(
          null,
          null,
          window.location.pathname + "?" + query
        );
        updateCatalog(event);
      }
      if (data.count) {
        let count_products = document.querySelector(".count_products");
        if (count_products) count_products.innerHTML = data.count + data.word;
      }
      if (data.pagination === undefined) {
        $(".paginationBlock").empty();
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
}

/**
 *
 * @param {Array<Object>} filters
 */
function createHeaderFilters(filters) {
  const headerFiltersBlock = document.getElementById("header-filters");
  headerFiltersBlock.innerHTML = "";
  const query = getQueryParameters();
  filters.forEach((elem) => {
    const filterElem = document.createElement(`div`);
    const titleElem = document.createElement("span");
    titleElem.classList.add("catalog-header-filter-item-title");
    titleElem.innerText = elem.group;
    filterElem.append(titleElem);
    elem.attributes.forEach((attribute) => {
      const singleElem = document.createElement("span");
      singleElem.classList.add("catalog-categories__link");
      singleElem.classList.add("catalog-header-filter-item");
      if (query[attribute.name]) {
        singleElem.classList.add("active");
      }
      singleElem.innerText = attribute.value__title;
      singleElem.setAttribute("value", attribute.name);
      filterElem.append(singleElem);
      headerFiltersBlock.appendChild(filterElem);
    });
  });
}

function loadData(event, data, more) {
  more = more || false;
  $(".filter-counter").fadeOut(200);

  console.log(data);

  if (data["products"].length > 0) {
    var html_products = data["products"];
    if (more) $(".sn-products-container").append(html_products);
    else $(".sn-products-container").html(html_products);
    $(".paginationBlock").html(data["pagination"]);

    $(".filterBlock").replaceWith(data["template_filters"]);

    // range slider init
    $(".range-slider-field").each(function (elem) {
      new RangeSliderField(elem);
    });
  } else {
    $(".paginationBlock").empty();
    $("form.sort-parameters").html("");
    $(".sn-products-container").html(
      '<div class="products-container">\
            <div class="row sn-products-container">\
                <div class="col-12">\
                <p class="empty-category__title">По данному запросу товаров не найдено.</p>\
                </div>\
            	</div>\
    		</div>'
    );
  }
}

function loadDataNews(event, data, target) {
  if (data["objects"].length != 0) {
    var html_objects = "";
    $.each(data["objects"], function (key, value) {
      html_objects += value;
    });
    html_objects += data["pagination"];
    target.closest(".row").append(html_objects);
    target.parents(".parentMore").remove();
  }
}

//function change page
function changePage(event) {
  event.preventDefault();
  var target = $(event.target);
  $(".pagination li").removeClass("active");
  $(target).closest("li").addClass("active");
  updateCatalog(event, false);
  $("body,html").animate({ scrollTop: 0 }, 400);
}

//set csrf to data
function csrf(str) {
  var input = $(".csrf_token").find("input");
  return str + "&" + $(input).attr("name") + "=" + $(input).attr("value");
}

function scroll() {
  $("body").animate({ scrollTop: 400 }, "slow");
}

function submitVacancyForm(event) {
  event.preventDefault();

  let form = event.target.closest("form");
  let serial = $(form).serialize();
  let url = form.action;
  let method = form.method;

  $.ajax({
    url: url,
    type: method,
    dataType: "json",
    processData: false,
    contentType: false,
    data: new FormData(form), //csrf(serial),
    success: (response) => {
      if (response["error"]) {
        document.querySelector("#vacancy_result .modal_title").innerText =
          "Что-то пошло не так";
        document.querySelector("#vacancy_result .vacancy-message").innerText =
          response["message"];
      } else {
        document.querySelector("#vacancy_result .modal_title").innerText =
          "Заявка отправлена!";
        document.querySelector("#vacancy_result .vacancy-message").innerText =
          response["message"];
      }
      $modal = $(".custom_modal.opened");
      if ($modal.length) {
        resetModal($modal);
      }
      $("body, i.modal_bg").addClass("opened");
      $(".custom_modal.opened").toggleClass("opened");
      $("#vacancy_result").addClass("opened");
    },
    error: (error) => {
      console.log(error);
    },
  });
}

function ym_call(name) {
  const id = 56972323;
  try {
    ym(id, "reachGoal", name);
  } catch (e) {
    console.error(e);
  }
  return true;
}

//submit ajax forms
function submitAjaxForm(event, funcCall) {
  event.preventDefault();

  var form = event.target.closest("form");
  let ym_name = $(form).attr("data-ym");
  let inputCheck = form.querySelector(
    "label.acceptance_checkbox input[type='checkbox']"
  );
  if (inputCheck) {
    if (!inputCheck.checked) {
      return;
    }
  }

  var serial = $(form).serialize();
  var url = form.action;
  var method = form.method;

  clearForm(form);
  form.classList.add("load");

  $.ajax({
    url: url,
    type: method,
    dataType: "json",
    data: csrf(serial),
    success: function (response) {
      console.log(response);
      if (response.errors) {
        validateForm(form, response.fields);
      } else {
        if (ym_name !== undefined) {
          ym_call(ym_name);
        }
        if (response.redirect !== undefined) {
          window.location.pathname = response.redirect;
        } else {
          form.classList.add("success");
        }
      }
      form.classList.remove("load");
    },
    error: function (error) {
      form.classList.remove("load");
      console.log(error);
    },
  });
}

// function showErrors(event, data) {
// 	var error_message = "";
// 	$.each(data['errors'], function(key, value) {
// 		if(event.target.tagName == "BUTTON" || event.target.tagName == "A")
// 			target = $(event.target).closest("form");
// 		else
// 			target = $(event.target);
// 		$(target).find('input[name=' + key +  ']').addClass('error');
// 		$(target).find('textarea[name=' + key +  ']').addClass('error');
// 		$.each(value, function(key1, value1) {
// 			error_message += value1 + "</br>";
// 		});
// 	});
// 	var err = $(target).find('.error_message');

// 	$(err).html(error_message);
// 	$(err).addClass('active');
// }

function showErrors(event, data) {
  if (event.target.tagName == "BUTTON" || event.target.tagName == "A")
    target = $(event.target).closest("form");
  else target = $(event.target);
  $(target).find("input").removeClass("is-invalid is-valid");
  $(target).find("input").addClass("is-valid");
  $(target).find("div.state").removeClass("valid-feedback invalid-feedback");
  $(target).find("div.state").text("Готово!");
  $(target).find("div.state").addClass("valid-feedback");

  $.each(data["fields"], function (key, value) {
    var input_error = $(target).find("input[name=" + key + "]");
    input_error.removeClass("is-valid");
    input_error.addClass("is-invalid");
    var div_error = $(input_error.siblings("div"));
    $(div_error).addClass("invalid-feedback");
    div_error.text(value);
    $(target)
      .find("textarea[name=" + key + "]")
      .addClass("error");
  });
}

function showErrorsButton(target, data) {
  var error_message = "";
  $.each(data["errors"], function (key, value) {
    $(target)
      .find("input[name=" + key + "]")
      .addClass("error");
    $.each(value, function (key1, value1) {
      error_message += value1 + "</br>";
    });
  });
  var err = $(target).find(".error_message");

  $(err).html(error_message);
  $(err).addClass("active");
}

function offForm(form) {
  $(form).find("input").attr("disabled", true);
  //$(form).animate({opacity:0.5}, 500);
}

function onForm(form) {
  $(form).find("input").attr("disabled", false);
  //$(form).animate({opacity:1.0}, 0);
}

//call form
$("#callForm, #consForm").on("submit", function (event) {
  submitAjaxForm(event, callBackForm);
});

function callBackForm(event, data) {
  if (event.target.tagName == "BUTTON")
    target = $(event.target).closest("form");
  else target = $(event.target);
  onForm(target);
  $(".error_message").removeClass("active");
  if (data["error"] != 0) {
    showErrors(event, data);
    console.log("error");
  } else
    $(target).html(
      '<h3 style="color:white;">Заявка отправлена. Наш менеджер свяжется с вами в ближайшее время</h3>'
    );
}

//execute filtering
function showMore(event) {
  event.preventDefault();

  // Блокировака для избежания нажатия несколько раз
  blockingPagination();

  // Включение прелоадера
  toggleCatalogPreloader();

  $("a.ajax_page").addClass("ajax");
  query_string = get_get_query(true);
  window.history.pushState(
    null,
    null,
    window.location.pathname + "?" + query_string
  );
  query_string += "&ajax=Y";
  $.ajax({
    url: window.location.pathname,
    type: "GET",
    dataType: "json",
    data: query_string,
    success: function (data) {
      replaceCatalogData(event, data, true);

      // Разблокировка
      unblickingPagination();
    },
    error: function () {
      console.log("error");
    },
  });
}

function countProducts(event) {
  // $(".tooltip_count").fadeOut();
  query_string = get_get_query();
  query_string += "&ajax=Y";
  $.ajax({
    url: window.location.pathname,
    type: "GET",
    dataType: "json",
    data: query_string,
    success: function (data) {
      if (data["count"] > 0) {
        $(".filter-counter span").text(
          "Показать " + data["count"] + " " + data["word_count"]
        );
      } else {
        $(".filter-counter span").text("Товаров не найдено ");
      }
    },
    error: function () {
      console.log("error");
    },
  });
}

function updateCartCount(cartAmount) {
  changeCartCount(cartAmount);
  // Обновление корзины для мобильной версии
  var cartCountBlocks = document.querySelectorAll(".cart_count");
  cartCountBlocks.forEach((block) => {
    block.innerText = cartAmount;
  });
}

function addProductInCart(event) {
  event.preventDefault();
  var form = $(event.currentTarget).closest("form");
  let toCartBtn = form.find("button.sn-add-to-cart")[0];
  let productCountInput = $(form).find("input[name=product-count]")[0];
  let inputValue = parseFloat(productCountInput.getAttribute("value"));
  let stepValue = parseFloat(productCountInput.getAttribute("data-step"));
  if (inputValue % stepValue !== 0) {
    toCartBtn.disabled = true;
    toCartBtn.classList.add("disabled-button");
    if (inputValue % stepValue !== 0 && event.target.value != 0) {
      $(form).find(".product-counter__notification_step").show();
      setTimeout(() => {
        $(form).find(".product-counter__notification_step").hide();
      }, 1000);
    }
    return;
  }
  var data = form.serialize();
  var url = form.attr("action");
  var product = event.currentTarget.closest(".product-card");
  if (product === null)
    product = event.currentTarget.closest(".product-card-wide");
  if (product === null) product = event.currentTarget.closest(".product-form");
  if (product === null) product = event.currentTarget.closest("form");

  console.log(form, "success", data);
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf(data),
    success: function (data) {
      dataLayer.push({
        ecommerce: {
          add: {
            products: [data["ecommerce-product"]],
          },
        },
      });
      $("div.order-table").replaceWith(data["dropdown"]);
      updateCartCount(data["count"]);
      productCartAdded(product);
    },
    error: function () {
      console.log("error");
    },
  });
}

function addProducts(event) {
  event.preventDefault();
  var form = $(event.currentTarget).closest("form");
  var data;
  var url = form.attr("action");

  var product = event.currentTarget.closest(".product-card");
  if (product === null)
    product = event.currentTarget.closest(".product-card-wide");
  if (product === null) product = event.currentTarget.closest(".product-form");

  data = "product-id=" + form.find("input[name=product-id]").val();

  var products = [];

  $.each(form.find(".variations-table-row"), function (index, value) {
    products.push({
      option: $(value).find("input[name=product-option]").val(),
      count: $(value).find("input[name=product-count]").val(),
    });
  });
  data += "&products=" + JSON.stringify(products);
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf(data),
    success: function (data) {
      dataLayer.push({
        ecommerce: {
          add: {
            products: [data["ecommerce-product"]],
          },
        },
      });
      $("div.order-table").replaceWith(data["dropdown"]);
      changeCartCount(data["count"]);
      productCartAdded(product);
      console.log("succes");
    },
    error: function () {
      console.log("error");
    },
  });
}

function sendCreateOrder(event, overrideUrl = null, extraData = null) {
  event.preventDefault();
  var target = $(event.target).closest("form");

  const commentElement = target.find("#comment");
  let commentText = commentElement.val();

  if (commentText.length > 500) {
    commentElement.css("border-color", "red");
    var errorMessageElement = commentElement.next();
    errorMessageElement.css("display", "block");
    return;
  }

  var data = $(target).serialize();
  data = new FormData($(target).get(0));
  if (extraData != null) {
    data = appendData(data, extraData);
  }
  var url = $(target).attr("action");
  if (overrideUrl != null) url = event.target.dataset.href;
  let ym_name = $(target).attr("data-ym");
  toggleCheckoutFormStatus();
  // $(target).find(".error_message").detach();
  // $(target).find(".error").removeClass("error");
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    // data: csrf(data),
    cache: false,
    processData: false,
    contentType: false,
    data: data,
    success: function (data) {
      if (data["errors"]) {
        target.find("input").removeClass("is-invalid");
        // target.find("input").addClass("is-valid");
        // target.find("input").siblings("div").removeClass("invalid-feedback");
        // target.find("input").siblings("div").addClass("valid-feedback");
        $.each(data["fields"], function (key, value) {
          let inp = target
            .find("input[name=" + key + "][type!=hidden][disabled!=disabled]")
            .addClass("is-invalid");
          inp.removeClass("is-valid");
          inp
            .siblings("div:not(.suggestions-wrapper)")
            .removeClass("valid-feedback");
          inp
            .siblings("div:not(.suggestions-wrapper)")
            .addClass("invalid-feedback");
          inp.siblings("div:not(.suggestions-wrapper)").text(value);
        });
        if (data["auth_user"] || data["fields"]["order"]) {
          var $errorBlock = $(".order-error");
          $errorBlock.css("display", "block");
          var responseString = "";
          $.each(data["fields"], function (key, value) {
            responseString += `<span style='display:block';>${value}</span>`;
          });
          $errorBlock.html(responseString);
        }
        if (data["modal"]) {
          $modal = $(".custom_modal.opened");
          if ($modal.length) {
            resetModal($modal);
          }
          $("body, i.modal_bg").addClass("opened");
          $(".custom_modal.opened").toggleClass("opened");
          $("#checkout_result").addClass("opened");
        }
        if (data["online_payment_error"]) {
          $modal = $(".custom_modal.opened");
          if ($modal.length) {
            resetModal($modal);
          }
          $("body, i.modal_bg").addClass("opened");
          $(".custom_modal.opened").toggleClass("opened");
          $("#online_payment_error").addClass("opened");
        }
        scroll();
      } else {
        dataLayer.push(data["ecommerce-product"]);
        if (ym_name !== undefined) {
          ym_call(ym_name);
        }
        $(".removeSuccess").remove();
        $(".orderContainer").append(data["template"]);
        changeCartCount(0);
        if (data["redirect"]) window.location = data["redirect"];
      }
      toggleCheckoutFormStatus();
    },
    error: function () {
      console.log("error");
      toggleCheckoutFormStatus();
    },
  });
}

function appendData(oldFormData, newObject) {
  for (const key in newObject) {
    if (newObject.hasOwnProperty(key)) {
      oldFormData.append(key, newObject[key]);
    }
  }
  return oldFormData;
}

var AJAX_SEARCH_MUTEX = false;

function smartAjaxSearch(event) {
  var search = $.trim($(event.target).val());
  var url = $(event.target).closest("form").attr("url-api");
  if ($(event.target).closest("form").attr("data-attr") == "desc")
    class_block = ".search-form__ajax-search";
  else class_block = ".ajax_search";
  console.log(class_block);
  if (search.length == 0) {
    AJAX_SEARCH_MUTEX = false;
    $("#navbarNavDropdown").html("");
    $(class_block + " ul").slideUp(350);
    console.log("slide up first");
    return true;
  }
  if (AJAX_SEARCH_MUTEX && AJAX_SEARCH_MUTEX != event) {
    AJAX_SEARCH_MUTEX = event;
    return true;
  }
  AJAX_SEARCH_MUTEX = event;
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf($(event.target).closest("form").serialize()),
    success: function (data) {
      console.log("data", data);
      if (AJAX_SEARCH_MUTEX == event) {
        AJAX_SEARCH_MUTEX = false;
      } else {
        smartAjaxSearch(AJAX_SEARCH_MUTEX);
        return true;
      }
      var result_html = "";
      if (data["template"]) {
        result_html = data["template"];
        $(class_block).html(result_html);
        // $(class_block + ' ul').stop().slideDown();
      } else {
        $(class_block).html("");
        // $(class_block + ' ul').stop().slideUp(350);
        console.log("slide up second");
      }
    },
    error: function () {
      console.log("error");
    },
  });
}

function resetFilter(event) {
  let salemode = false;
  if (document.querySelector("form.filtering input[name='sale']").checked) {
    salemode = true;
  } else {
    document.getElementById("salemode_flag").value = "false";
  }
  let stockmode = false;
  if (document.querySelector("form.filtering input[name='stock']").checked) {
    stockmode = true;
  } else {
    document.getElementById("stockmode_flag").value = "false";
  }
  window.location =
    window.location.pathname +
    "?" +
    (salemode ? "sale=on&salemode" : "") +
    (stockmode ? "&stock=on&stockmode" : "");
}

function addProductFromCart(event) {
  event.preventDefault();
  var form = $(event.target).closest("form");
  var data = form.serialize();
  var url = form.attr("action");
  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf(data),
    success: function (data) {
      form
        .find(".cart-item-total")
        .text(String(data["price"]).toLocaleString("ru-RU"));
      $(`#order-item-count-${data["product_id"]}`).text(
        String(data["item_count"])
      );
      $(".cart-total").text(
        String(data["total"])
          .toLocaleString()
          .replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, "$1 ")
      );
      $(".order_total").text(
        String(data["total"])
          .toLocaleString()
          .replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, "$1 ")
      );
      toggleOverflowNote(data.is_overflowed, event.target);
    },
    error: function () {
      console.log("error");
    },
  });
}

function changeCardType(event) {
  if (event.target.tagName == "BUTTON") var target = $(event.target);
  else var target = $(event.target).closest("button");
  var url = $(target).attr("data-url");
  var type = $(target).attr("data-type");

  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf("type=" + type),
    success: function (data) {
      if (data["change"]) console.log(11);
      updateCatalog(event);
    },
    error: function () {
      console.log("error");
    },
  });
}

function addInAccount(event, setState) {
  event.preventDefault();
  if (event.target.tagName === "BUTTON") var button = $(event.target);
  else var button = $(event.target).closest("button");
  var product = button
    .closest(".product-card, .product-card-wide")
    .attr("data-product");

  if (product == undefined) product = button.attr("data-product");
  var url = button.attr("data-url");

  console.log(button);

  $.ajax({
    url: url,
    type: "POST",
    dataType: "json",
    data: csrf("product=" + product),
    success: function (data) {
      setState(data["count"]);
      miniButtonHandler(button[0]);
    },
    error: function () {
      console.log("error");
    },
  });
}

// Функции добавления, удаления, восстановления избранных товаров
$("body").on(
  "click",
  ".sn-add-to-favorites, .favorite-remove, .favorite-restore",
  function (event) {
    addInAccount(event, changeFavoritesCount);
  }
);

$("body").on(
  "click",
  ".compare, .sn-add-to-compare, .compare-remove, .compare-restore",
  function (event) {
    addInAccount(event, changeCompareCount);
  }
);

//Личный кабинет

function loginCallback(event, data) {
  if (data["reload"]) {
    window.location = window.location;
  }
}

$("#custom_modal-1 form").on("submit", function (event) {
  event.preventDefault();
  console.log("popopp");
  submitAjaxForm(event, loginCallback);
});

$("#custom_modal-3 button").on("click", function (event) {
  event.preventDefault();
  console.log("popopp");
  submitAjaxForm(event, loginCallback);
  grecaptcha.reset();
});

$("#custom_modal-4 button").on("click", function (event) {
  event.preventDefault();
  console.log("popopp");
  submitAjaxForm(event, loginCallback);
});

//call form
$("#recall_modal button").on("click", function (event) {
  submitAjaxForm(event, callBackForm);
});

$("#product-nutify button").on("click", function (event) {
  submitAjaxForm(event, callBackForm);
});
// $('#product-nutify form').on('submit', function(event) {
// 	submitAjaxForm(event, callBackForm)
// })

$("#summaryform").on("submit", function (event) {
  submitVacancyForm(event);
});

$("#contacts-form button").on("click", function (event) {
  submitAjaxForm(event, callBackForm);
});

function delProductFromCart(event) {
  var form = $(event.target).closest("form");
  var data = form.serialize();

  // Блокировка элемента корзины для избежания нескольких нажатий на кнопку
  // удаление товара из корзины
  blockedCartItem(form[0]);

  $.ajax({
    url: "/api/shop/cart/delete/",
    type: "POST",
    dataType: "json",
    data: csrf(data),
    success: function (response) {
      $(".cart-total").text(response["total"]);
      changeCartCount(response["count"]);
      var isOrderPage = document.querySelector("#order-page");

      if (response["count"] > 0) {
        deleteCartItem(form[0]);
        if (isOrderPage) {
          $(`#order-item-${response["product_id"]}`).remove();
        }
      } else {
        clearCart(response["empty"]);

        if (!isOrderPage) {
          return;
        }
        if (response["redirect"]) {
          window.location.href = response["redirect"];
        }
      }
      if (isOrderPage) {
        if (response["total"] < 3000) {
          $(".available_notify").css();
        }
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function getCartItems() {
  return [...document.querySelectorAll(".cart-item")];
}

function cartHasOverflow() {
  return getCartItems().some((el) => el.hasAttribute("is_overflowed"));
}

function switchCardPayment() {
  let isJuricalCheckbox = document.querySelector("#face");
  const isJurical = isJuricalCheckbox ? isJuricalCheckbox.checked : false;
  if (cartHasOverflow() || isJurical) {
    disabledTypePayment("bank");
  } else if (isJurical) {
    setOtherTypesActive("bank");
  } else {
    setOtherTypesActive(undefined);
  }
}

function toggleOverflowNote(isOverflowed, target) {
  var form = target.closest("form");
  var overflowNote = form.querySelector(".user-note-overflow");
  var isDisplayed = overflowNote.classList.contains("display");

  if (isOverflowed && !isDisplayed) {
    overflowNote.classList.add("display");
    form.classList.add("is_overflowed");
    form.setAttribute("is_overflowed", true);
  } else if (!isOverflowed && isDisplayed) {
    overflowNote.classList.remove("display");
    form.classList.remove("is_overflowed");
    form.removeAttribute("is_overflowed", false);
  }
  switchCardPayment();
}

function selectShipping(event) {
  var link = event.currentTarget;
  var container = link.closest(".nav").parentElement;
  var tabContent = container.querySelector(".tab-content");
  var pane = container.querySelector(link.attributes.href.textContent);

  $(".tab-pane").each(function (item) {
    $("input, select, textarea").each(function (element) {
      element.disabled = true;
    });
  });

  $("input, select, textarea").each(function (element) {
    element.disabled = false;
  });
}

function toggleState(target, callBack) {
  var otherButtons = document.querySelectorAll(`input[name="${target.name}"]`);
  var checkState = target.checked;
  otherButtons.forEach((checkBox) => {
    checkBox.checked = checkState;
  });
  if (callBack) callBack();
}

function canBeSubmitted(event) {
  let form = $(event.target);
  let searchInput = form.find("#search");
  let searchValue = searchInput.val();
  searchValue = searchValue.replace(/\s/g, "");
  return !(searchValue === "" || searchValue === null);
}

function updateFilterForm(target) {
  const value = target.getAttribute("value");
  const filterCheckbox = document.querySelector(`input[name="${value}"]`);
  if (filterCheckbox) {
    filterCheckbox.checked = target.classList.contains("active");
  }
}

$(window).on("load", function () {
  // //set events
  // $('form.filtering').on('submit', updateCatalog);
  $("body").on("submit", "form.filtering", updateCatalog);
  $("body").on("click", "#reset_filter", resetFilter);
  $("body").on(
    "click",
    ".sort-parameters__layout-types button",
    changeCardType
  );
  $("body").on("click", ".catalog-header-filter-item", function (event) {
    const { target } = event;
    const isChecked = target.classList.contains("active");
    isChecked
      ? target.classList.remove("active")
      : target.classList.add("active");
    updateFilterForm(target);
    updateCatalog();
  });
  // $('body').on('change', '#type_category', changeType);
  // $('.filters input').on('change', countProducts);
  // Сломанный гальп не позволяет удалить некоторые элементы в из исходника
  $("body").off("click", ".filters label");
  $("body").on("click", ".filters label:not(.off)", function () {
    filterShowCounter(this);
  });

  $("body").on("change", "#customCheckSale", function (event) {
    toggleState(event, function () {
      updateCatalog(event, undefined, undefined, undefined, true);
    });
  });
  $("body").on("change", "#sort-sale", function (event) {
    toggleState(event, function () {
      updateCatalog(event, undefined, undefined, undefined, true);
    });
  });
  $("body").on("change", "#customCheckStock", function (event) {
    toggleState(event.target, updateCatalog);
  });
  $("body").on("change", "#customCheckShock", function (event) {
    toggleState(event.target, updateCatalog);
  });
  $("body").on("change", "#sort-stock", function (event) {
    toggleState(event.target, updateCatalog);
  });
  $("body").on("change", "#sort-actions", function (event) {
    toggleState(event.target, updateCatalog);
  });
  $("body").on("change", "#sort-shock", function (event) {
    toggleState(event.target, updateCatalog);
  });

  $(".nav-link").on("click", selectShipping);

  // $('#base_search').on('click',baseSearch);
  // $('#base_map').on('click',baseSearchMap);

  // $('.trigger-link').on('click',vacancyInput);

  // $('#main_cats input').on('change', checkMainCat);
  // // $('.select2-selection').on('click', countProducts);
  // //activate filters
  // //2017$('#filters_form input[type=checkbox]').on('click', updateCatalog);
  // $('#sorting').on('change', updateCatalog);
  // $('button.add, button.reduce').on('click', changeCountProduct);

  // $('form.checkout_form .submit-button').on('click', sendCreateOrder);
  $("form.sn-order-form").on("submit", function (event) {
    // orderid - id сохраненного заказа
    var orderId = event.target.dataset.order;
    if (orderId) sendCreateOrder(event, null, { order_id: orderId });
    else sendCreateOrder(event, null);
  });

  // $('form.sort-parameters button').on('click', updateCatalog);
  $("form.sort-parameters select").on("change", updateCatalog);

  $(".search-form input").on("input", smartAjaxSearch);
  $(".search-form").on("submit", (event) => {
    return canBeSubmitted(event);
  });

  $("body").on("click", ".pagination li a", changePage);

  $("body").on("click", ".sn-add-to-cart", addProductInCart);
  // $('.add-products').on('click', addProducts);

  $("body").on("change", "input.change-count", addProductFromCart);
  $("body").on("click", ".cart-item-delete", delProductFromCart);

  $("body").on("click", "#show_more", showMore);

  $("body").on("click", ".modal_product_trigger", function (event) {
    var product = event.currentTarget.closest(".product-card");
    if (product === null)
      product = event.currentTarget.closest(".product-card-wide");

    var productId = product.dataset.product;
    var input = document.querySelector('#product-nutify [name="product_id"]');

    if (input !== null) input.value = productId;
  });

  let coll = document.getElementsByClassName("collapser-title");
  for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      this.classList.toggle("active");
      let content = this.nextElementSibling;
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      }
    });
  }

  function expand(element) {
    if (element && element.classList.contains("place-accordion-list")) {
      element.style.height = 0;
      element.style.height = element.scrollHeight.toString() + "px";
      expand(element.parentElement);
    } else {
      return;
    }
  }

  document.addEventListener("click", (event) => {
    //event.preventDefault();
    if (event.target.classList.contains("place-accordion-button")) {
      let item = event.target.closest(".place-accordion-item");
      let sibling = null;
      if (item) sibling = item.nextElementSibling;
      if (sibling && sibling.classList.contains("place-accordion-list")) {
        if (event.target.classList.contains("active")) {
          event.target.classList.remove("active");
          sibling.style.height = "0";
          expand(sibling.parentElement);
        } else {
          event.target
            .closest(".place-accordion-list")
            .querySelectorAll(".place-accordion-item")
            .forEach((element) => {
              let btn = element.querySelector(".place-accordion-button");
              if (btn) btn.classList.remove("active");
              let list = null;
              if (
                element.nextElementSibling &&
                element.nextElementSibling.classList.contains(
                  "place-accordion-list"
                )
              )
                list = element.nextElementSibling;
              if (list) list.style.height = "0";
            });
          event.target.classList.add("active");
          expand(sibling);
        }
        event.target.closest(".place-accordion").style.height = "100%";
      }
    }
  });

  /*document.querySelectorAll(".place-accordion .place-accordion-button").forEach(element => {
        element.addEventListener("click", event => {
            event.preventDefault();
            let item = event.target.closest(".place-accordion-item");
            let sibling = null;
            if (item) sibling = item.nextElementSibling;
            if (sibling && sibling.classList.contains("place-accordion-list")) {
                if (event.target.classList.contains("active")) {
                    event.target.classList.remove("active");
                    sibling.style.height = "0";
                    expand(sibling.parentElement);
                } else {
                    event.target.closest(".place-accordion-list").querySelectorAll(".place-accordion-item").forEach(element => {
                        let btn = element.querySelector(".place-accordion-button");
                        if (btn) btn.classList.remove("active");
                        let list = null;
                        if (element.nextElementSibling && element.nextElementSibling.classList.contains("place-accordion-list")) list = element.nextElementSibling;
                        if (list) list.style.height = "0";
                    });
                    event.target.classList.add("active");
                    expand(sibling);
                }
                event.target.closest(".place-accordion").style.height = "100%";
            }
        });
    });*/
});

if (document.querySelector(".product-counter__original-input")) {
  $("body").find(".product-counter__notification_step").hide();
  document
    .querySelectorAll(".product-counter__original-input")
    .forEach((element) => {
      new MutationObserver((mutationRecords) => {
        let inp = mutationRecords[0].target;
        //inp.value = inp.getAttribute("value");
        if (inp.getAttribute("value") != inp.value) updateCounter(inp); //inp.setAttribute("value", inp.value);
        console.log(mutationRecords, inp, inp.value);
      }).observe(element, {
        attributes: true,
        attributeFilter: ["value"],
        attributeOldValue: true,
      });
    });
}

var timeout;

function showTip(target, type) {
  if (type) {
    target.find(".product-amount__notification_max").show();
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      target.find(".product-amount__notification_max").hide();
    }, 1000);
  } else {
    target.find(".product-amount__notification_min").show();
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      target.find(".product-amount__notification_min").hide();
    }, 1000);
  }
}

function updateCounter(element) {
  var val = parseFloat($(element).val().replace(",", ".")); //attr("value").replace(",","."));
  var min = parseFloat($(element).attr("min").replace(",", "."));
  var max = parseFloat($(element).attr("max").replace(",", "."));
  console.log("log prs float", val, min, max);

  if (val > max) showTip($(element).parents(".product-counter"), "max");

  if (val < min) showTip($(element).parents(".product-counter"));

  $(element).attr("value", val > max ? max : val < min ? min : val);
  element.value = val > max ? max : val < min ? min : val;
  updateFakeInput(element);
}

document.querySelectorAll('input[name="face"]').forEach((checkbox) => {
  open_step(checkbox.checked);
  checkbox.addEventListener("change", (event) => {
    const target = event.currentTarget || event.target;
    open_step(target.checked);
  });
});

function open_step(checked) {
  const container = document.querySelector(".face_step");
  if (container) {
    if (checked) {
      container.style.display = "block";
    } else {
      container.style.display = "none";
      // container.querySelectorAll('input').forEach(input => {
      //     input.value = ''
      // });
    }
  }
}

// function toggle_cart_payment(state){
//     var onlinePayment = document.querySelector('label[for=payment-1]');
//     var displayValue = state ? 'none' : 'inline-block';
//     onlinePayment.style.display = displayValue;
//     var nextLabel = onlinePayment.nextElementSibling;
//     var radioBtn = nextLabel.querySelector('input[type=radio]');
//     radioBtn.checked = true;
// }

function add_file() {
  const container = document.querySelector(".example-1");
  if (container) {
    container.querySelectorAll("input").forEach((input) => {
      input.value = "";
      input.nextElementSibling.innerHTML = "Добавить файл";
    });
  }
}

// $('.product-counter__original-input').on('change', function (event) {
// 	var sum = 0;
// 	sum = parseInt($('[name=product-count-vologda]').val()) + parseInt($('[name=product-count-cherepovets]').val());
// 	console.log(sum);
// 	$('[name=product-count]').val(sum);
// })

document.querySelectorAll('input[type="file"]').forEach((input) => {
  let label = input.nextElementSibling;
  input.addEventListener("change", function (e) {
    label.innerHTML = this.files[0].name;
  });
});
const dataAnchore = document.querySelectorAll("[data-anchore]");
Array.prototype.slice.call(dataAnchore).forEach(function (button) {
  button.onclick = function (event) {
    event.preventDefault();
    const name = button.dataset.anchore;

    const target = $(name);
    if (target) {
      $("html, body").animate(
        {
          scrollTop: target.offset().top,
        },
        500
      );
      check_arrow_to_top();
    }
  };
});

function check_arrow_to_top() {
  const arrow = document.querySelector(".to-top");
  if (arrow) {
    if (window.scrollY > 300) {
      arrow.classList.remove("hide");
    } else {
      arrow.classList.add("hide");
    }
  }
}

$(window).scroll(check_arrow_to_top);

var options = {
  translation: {
    Y: { pattern: /[7-8]/ },
  },
  onKeyPress: function (cep, e, field, options) {
    var masks = [
      "+7 (999) 999-99-99",
      "8 (999) 999-99-99",
      "Y (999) 999-99-99",
    ];
    var mask;
    if (cep[0] === "7" || cep[0] === "+") {
      mask = masks[0];
    } else if (cep[0] === "8") {
      mask = masks[1];
    } else {
      mask = masks[2];
    }
    console.log("mask", mask, "cep", cep[0], cep[0] === "7");
    $('input[type="tel"]').mask(mask, options);
  },
};
/* Маска телефона */
$('input[type="tel"]').mask("Y (999) 999-99-99", options);

$("body").on("click", ".filter-category[data-category]", function (event) {
  const category = event.target.closest(".filter-category").dataset.category;
  const input = $('input[name="category"]');
  const shockInput = $('input[name="shock"]');
  const stockInput = $('input[name="stock"]');
  const saleInput = $('input[name="sale"]');
  [shockInput, stockInput, saleInput].forEach((elem) => {
    elem.prop("checked", false);
  });
  let d_none = false;
  if (
    category &&
    input.val() !==
      event.target.closest(".filter-category").dataset.category.toString()
  ) {
    input.val(category);
    d_none = true;
  } else {
    input.val("");
  }
  console.log(
    "call update catalog with",
    d_none,
    "on click category",
    input.val()
  );
  updateCatalog(event, false, false, d_none);
});

//cookie

// возвращает cookie если есть или undefined
function getCookie(name) {
  var matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

// уcтанавливает cookie
function setCookie(name, value, props) {
  props = props || {};

  var exp = props.expires;

  if (typeof exp == "number" && exp) {
    var d = new Date();

    d.setTime(d.getTime() + exp * 1000);

    exp = props.expires = d;
  }

  if (exp && exp.toUTCString) {
    props.expires = exp.toUTCString();
  }
  value = encodeURIComponent(value);

  var updatedCookie = name + "=" + value;

  for (var propName in props) {
    updatedCookie += "; " + propName;

    var propValue = props[propName];

    if (propValue !== true) {
      updatedCookie += "=" + propValue;
    }
  }
  document.cookie = updatedCookie;
}

// удаляет cookie
function deleteCookie(name) {
  setCookie(name, null, { expires: -1 });
}

let cookie_window = getCookie("cookie_window");
if (cookie_window) {
  document
    .querySelectorAll(".cookie-window")
    .forEach((item) => item.classList.add("disable"));
} else {
  document
    .querySelectorAll(".cookie-window")
    .forEach((item) => item.classList.remove("disable"));
}
document.querySelectorAll(".cookie-button").forEach((item) => {
  item.addEventListener("click", (event) => {
    let date = new Date();
    date.setFullYear(date.getFullYear() + 10);
    setCookie("cookie_window", true, { expires: date });
    document
      .querySelectorAll(".cookie-window")
      .forEach((item) => item.classList.add("disable"));
  });
});

const now = new Date();

let banner = document.querySelector("#banner-modal");
if (banner) {
  const start_banner = new Date(banner.dataset.start);
  const end_banner = new Date(banner.dataset.end);
  if ((now >= start_banner) && (now < end_banner)) {
    let has_banner = getCookie("banner");
    if (!has_banner) {
      let body = document.querySelector("body");
      let body_bg = document.querySelector("body .modal_bg");
      if (banner && body && body_bg) {
        banner.classList.add("opened");
        body.classList.add("opened");
        body_bg.classList.add("opened");
        now.setDate(now.getDate() + 1);
        setCookie("banner", true, { expires: now });
      }
    }
  }
}

var menuBtn = $('.messenger-btn'),
  menu = $('.messenger-links');
  menuBtn.on('click', function() {
      if (menu.hasClass('show')) {
        menu.removeClass('show');
      } else {
        menu.addClass('show');
      }
      if (menuBtn.hasClass('active')) {
        menuBtn.removeClass('active');
      } else {
        menuBtn.addClass('active');
      }
  });
  $(document).mouseup(function (e){
    var div = $('.socials-messenger');
    if (!div.is(e.target)
        && div.has(e.target).length === 0) {
      $('.messenger-links').removeClass('show');
    }
  });
