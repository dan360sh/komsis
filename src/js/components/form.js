function validateForm(form, fields) {
    let isValid = true

    for (const key in fields) {
        if (fields.hasOwnProperty(key)) {
            const control = form.querySelector('[name="' + key + '"]')
            const group = control.parentElement
            const feedback = document.createElement("div")

            control.classList.add("is-invalid")
            feedback.classList.add("invalid-feedback")
            feedback.innerHTML = fields[key]
            group.appendChild(feedback)
            isValid = false
        }
    }

    const agree = form.querySelector('[name="agree"]')
    if (agree !== null) {
        if (!agree.checked)
            isValid = false
    }

    return isValid
}

function clearForm(form) {
    form.querySelectorAll(".form-control").forEach(control => {
        const group = control.parentElement

        control.classList.remove("is-invalid", "is-valid")
        form.querySelectorAll(".invalid-feedback, .valid-feedback, .alert")
            .forEach(element => { element.remove() })
    })
}

function successForm(form, message) {
    const alertSuccess = document.createElement("div")
    const group = form.querySelector(".form-group")

    clearForm(form)
    alertSuccess.classList.add("alert", "alert-success")
    alertSuccess.innerHTML = message
    alertSuccess.role = "alert"
    if (group !== null) {
        form.insertBefore(alertSuccess, group)
    } else {
        form.appendChild(alertSuccess)
    }
}

/////////////
//   API   //
/////////////

window.validateForm = validateForm
window.clearForm = clearForm
window.successForm = successForm
