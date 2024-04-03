function miniButtonHandler(button) {
    if (button.classList.contains("active")) {
        button.classList.remove("active")
    } else {
        button.classList.add("active")
    }
}

window.miniButtonHandler = miniButtonHandler
