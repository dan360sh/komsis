
function filterBrandsByLetter(letter) {
    var url = window.location.href;
    var requestData = {
        'letter': letter
    }
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: requestData,
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) {
            updateBrandsList(data.template)
        },
        error: function () {
            console.log('error');
        }
    });
}

function updateBrandsList(template) {
    $("#brand-list-container").html(template)
}

function toggleAlphabets(target) {
    target.removeClass("hidden");
    var targetClass = target.attr("class");
    $(`.${targetClass}`).not(target).addClass("hidden");
}

document.addEventListener("DOMContentLoaded", function(event) {
    $(".letter-filter__item").not(".letter-filter__item.disabled").on("click", function(event) {
        var letterValue = event.target.dataset["value"];
        filterBrandsByLetter(letterValue);
    });
    $(".letter-filter-controls__item").on("click", function(event) {
        var currentElement = event.target;
        currentElement.classList.add("hidden");
        var others = $(".letter-filter-controls__item").not(this);
        others.each(function(index, elem) {
            elem.classList.remove("hidden");
        })
        toggleAlphabets($(currentElement.dataset.target));
    })
});
