$('.applications').mosaicflow({
    itemSelector: '.app',
    minItemWidth: 420,
    minColumns: 1,
    columnClass: 'applications__column'
});

$('input[type="tel"]').mask("+7 (999) 999-99-99")

$('.submit_row input').hover(function() {
    if($('.submit_row .submit_row__popup').length) return false

    let $container = $(this).closest('.submit_row')
    let value = $(this).val()
    let position = $(this).position().top
    let height = $(this).height()

    $container.append(`<p class="submit_row__popup">${ value }</p>`)
    $container.find('.submit_row__popup').css({
        'top': position + height - $container.find('.submit_row__popup').height() / 1.5,
        'opacity': '1'
    });
}, function() {
    let $container = $(this).closest('.submit_row')
    $container.find('.submit_row__popup').remove()
})
