import "overlayscrollbars"

OverlayScrollbars(document.querySelectorAll(".search-form__ajax-search > ul, .filters .scroll_content, .modal-order .order-table__body"), {
    autoUpdate: true,
    overflowBehavior: {
        x: "hidden",
        y: "scroll"
    }
})
