var divs = $(".footer-social-link").not('.footer-social-link_wide');

for(var i = 0; i < divs.length; i += 3) {
	divs.slice(i, i + 3).wrapAll("<div class='footer-social-links-wrapper'></div>");
}
