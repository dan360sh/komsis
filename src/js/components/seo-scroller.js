import "overlayscrollbars"


/*  Обработка картинок в сео-блоке  */
$(".seo-scroller").each(function () {
	var $wrapper = $(this).find(".seo-scroller__seo-images");
	var $images = $wrapper.find("img");

	if ($images.length === 1) {
		$images.each(function (i, e) {
			$wrapper.append("<div class='seo_img large'>" + $(e)[0].outerHTML + "</div>");
			$(e).remove();
		})
	}
	else if ($images.length === 2) {
		var count = 0;
		$images.each(function (i, e) {
			if (!count) {
				$wrapper.append("<div class='img_row'><div class='seo_img big'>" + $(e)[0].outerHTML + "</div></div>");
			}
			else {
				$wrapper.append("<div class='seo_img big'>" + $(e)[0].outerHTML + "</div>");
			}

			$(e).remove();
			count++;
		});
	}
	else if ($images.length === 3) {
		var count = 0;
		$wrapper.append("<div class='img_row'></div>");
		$images.each(function (i, e) {
			if (count !== 2) {
				$wrapper.find(".img_row").append("<div class='seo_img'>" + $(e)[0].outerHTML + "</div>");
			}
			else {
				$wrapper.append("<div class='seo_img big'>" + $(e)[0].outerHTML + "</div>");
			}

			$(e).remove();
			count++;
		});
	}
	else {
		$images.each(function (i, e) {
			$wrapper.append("<div class='img_row'><div class='seo_img big'>" + $(e)[0].outerHTML + "</div></div>");
			$(e).remove();
		})
	}
});

OverlayScrollbars(document.querySelectorAll(".seo-scroller__seo-text"), {
    autoUpdate: true,
    overflowBehavior: {
        x: "hidden",
        y: "scroll"
    }
})
