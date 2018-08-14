$(".events-group").hover(function () {
    $(this).css("background-color", "rgba(0,0,0,0.1)");
    $(this).css("cursor", "pointer");
}, function () {
    $(this).css("background-color", "rgba(0,0,0,0.0)");
});

$('#reservaModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var dia = button.data('day'); // Extract info from data-* attributes
    var dias_array = ['Lunes','Martes','Miercoles','Jueves','Viernes'];

    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this);
    modal.find('.modal-title').text('Reserva un espacio el ' + dias_array[dia]);
    modal.find('#dia_seleccionado').val(dia);
});