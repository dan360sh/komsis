function catalogSubcatsInit() {
  var width;
  var b = 1;
  var sum = 0;
  $(".catalog-categories__link").each(function (i, el) {
    var text = $(el).text();
    // Приводим ширину элементов к целочисленному значению
    var w = Math.ceil($(el).outerWidth(true)); // добавляем значение отступа справа
    sum += w; // Складываем ширину соседних элементов
    if (sum > width) {
      // Ограничиваем ширину
      b++; //Считаем кол-во строк
      sum = w; // Приравниваем значение ширины строки к ширине первого элемента в строке
    }
    if (b == 1) {
      width = 830;
    } // значение ширины 1 строки
    if (b == 2) {
      width = 760;
    } // значение ширины 2 строки
    else {
      width = 830;
    } // значение ширины остальных строк
    if (b >= 3) {
      // Убеждаемся что строк более 3х
      $(el).addClass("hidden-link"); // добавляем класс на элементы, которые будем скрывать
    }
  });
  $(".hidden-link").wrapAll(
    "<div class='catalog-categories__hidden-links'></div>"
  ); // делаем обертку для 3 и более строк
  $("div.catalog-categories__hidden-links").after(
    '<a href="" class="catalog-categories__open"><span>Еще</span><svg role="img" width="8" height="5"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/static/images/sprite.svg#caret-bottom"></use></svg></a>'
  ); // добавляем кнопку ЕЩЕ
  $(".catalog-categories__hidden-links a:last-child").after(
    '<a href="" class="catalog-categories__close"><span>Скрыть</span><svg role="img" width="8" height="5"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/static/images/sprite.svg#caret-bottom"></use></svg></a>'
  ); // добавляем кнопку скрыть
}
catalogSubcatsInit();

// Действия при кнопке ЕЩЕ
$("body").on("click", "a.catalog-categories__open", function (event) {
  $(".catalog-categories").toggleClass("opened");
  $("div.catalog-categories__hidden-links").slideDown(0, function () {
    $(".catalog-categories__close").css("display", "inline-block");
    $(".catalog-categories a.hidden-link").unwrap();
  });
  $(this).css("display", "none");

  return false;
});

// Действия при кнопке СКРЫТЬ
$("body").on("click", "a.catalog-categories__close", function (event) {
  $(".catalog-categories").toggleClass("opened");
  $(".catalog-categories a.hidden-link").wrapAll(
    '<div class="catalog-categories__hidden-links"></div>'
  );
  $("div.catalog-categories__hidden-links").slideUp(function () {
    $(".catalog-categories__open").css("display", "inline-block");
  });
  $(this).css("display", "none");

  return false;
});

function categoriesResize() {
  if ($(window).width() < 1200) {
    $(".catalog-categories__close, .catalog-categories__open").css(
      "display",
      "none"
    );
    $(
      ".catalog-categories .catalog-categories__hidden-links a.hidden-link"
    ).unwrap();
  } else {
    $(".catalog-categories > a.hidden-link").wrapAll(
      '<div class="catalog-categories__hidden-links"></div>'
    );
    if (!$(".catalog-categories").hasClass("opened"))
      $(".catalog-categories__open").css("display", "inline-block");
    else $(".catalog-categories__close").css("display", "inline-block");
  }
}
categoriesResize();
$(window).resize(function () {
  categoriesResize();
});

window.categoriesResize = categoriesResize;
window.catalogSubcatsInit = catalogSubcatsInit;
