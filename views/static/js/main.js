document.addEventListener('DOMContentLoaded', function() {
    
    const loginForm = document.getElementById('login-form-modal');
    const errorMessageDiv = document.getElementById('login-error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            // Prevenimos que el formulario se envíe de la forma tradicional (recargando la página)
            event.preventDefault();

            // Ocultamos cualquier mensaje de error anterior
            errorMessageDiv.classList.add('d-none');

            const email = document.getElementById('modal-email').value;
            const password = document.getElementById('modal-password').value;

            // Usamos la API Fetch para enviar los datos al servidor en segundo plano
            fetch('/auth/login_ajax', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email, password: password }),
            })
            .then(response => response.json()) // Convertimos la respuesta del servidor a JSON
            .then(data => {
                // Procesamos la respuesta JSON
                if (data.status === 'success') {
                    // Si el login fue exitoso, redirigimos a la URL que nos dijo el servidor
                    window.location.href = data.redirect_url;
                } else {
                    // Si hubo un error, mostramos el mensaje en el div de error
                    errorMessageDiv.textContent = data.message;
                    errorMessageDiv.classList.remove('d-none');
                }
            })
            .catch(error => {
                // En caso de un error de red o del servidor
                console.error('Error:', error);
                errorMessageDiv.textContent = 'Ocurrió un error de conexión. Inténtalo de nuevo.';
                errorMessageDiv.classList.remove('d-none');
            });
        });
    }
});