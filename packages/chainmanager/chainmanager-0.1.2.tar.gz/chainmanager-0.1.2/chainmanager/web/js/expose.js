eel.expose(show_warning);
function show_warning(message) {
    Swal.fire({
        type: 'warning',
        title: 'Oops...',
        text: message
    })
}

eel.expose(close_window);
function close_window() {
    window.close()
}
