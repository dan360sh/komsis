const SEARCH_BUTTON_CLASS = "mobile-search-icon"
const TOGGLE_CLASS = "active"

function onSearchButtonClick(element) {
    var button = element;
    var isActive = button.classList.contains(TOGGLE_CLASS);
    if (isActive) {
        button.classList.remove(TOGGLE_CLASS)
    } else {
        button.classList.add(TOGGLE_CLASS)
    }
    toggleSvg(!isActive, button);
    toggleMobileSearch();
}

function toggleSvg(isParentActive, parent) {
    var searchIcon = parent.querySelector(".search-icon");
    var closeIcon = parent.querySelector(".close-icon");
    if (isParentActive) {
        searchIcon.classList.remove(TOGGLE_CLASS);
        closeIcon.classList.add(TOGGLE_CLASS);
    } else {
        searchIcon.classList.add(TOGGLE_CLASS);
        closeIcon.classList.remove(TOGGLE_CLASS);
    }
}

function toggleMobileSearch() {
    document.querySelector(".mobile-search-wrapper").classList.toggle("opened")
}

var searchButtons = document.getElementsByClassName(SEARCH_BUTTON_CLASS);
if(searchButtons.length > 0) {
    for (var index = 0; index < searchButtons.length; index++) {
        var element = searchButtons[index];
        element.addEventListener("click", function(event) {
            onSearchButtonClick(element)
        })
    }
}