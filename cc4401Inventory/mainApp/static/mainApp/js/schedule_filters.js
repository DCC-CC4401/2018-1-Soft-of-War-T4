function change_button_type(id_filtro) {
    $('#' + id_filtro).toggleClass("btn-outline-primary").toggleClass("btn-primary");
    toogle_opacity('reserv_' + id_filtro)
}

function toogle_opacity(id_filtro) {
    $('.' + id_filtro).css("opacity", Math.abs(1 - $('.' + id_filtro).css("opacity")).toString());
}