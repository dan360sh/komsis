function blockingPagination() {
    const paginationBlock = document.querySelector(".paginationBlock")
    paginationBlock.style.pointerEvents = "none"
}

function unblickingPagination() {
    const paginationBlock = document.querySelector(".paginationBlock")
    paginationBlock.style.pointerEvents = ""
}

window.blockingPagination = blockingPagination
window.unblickingPagination = unblickingPagination
