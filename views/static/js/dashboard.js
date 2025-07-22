document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendario-admin');

    if (calendarEl) {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            // Configuración del calendario
            initialView: 'dayGridMonth', // Vista de mes
            locale: 'es', // Idioma español
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek' // Opciones de vista
            },
            
            // Aquí está la magia: le decimos dónde buscar los eventos
            events: '/api/admin/eventos_calendario',

            // Ajustes visuales
            height: 'auto', // Ajusta la altura al contenedor
            eventColor: '#378006' // Color por defecto (aunque lo sobreescribimos con CSS)
        });

        calendar.render();
    }
});