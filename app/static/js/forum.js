// Contador de caracteres dos campos de post
document.querySelectorAll("textarea.campo-post").forEach(function (campo) {
    const contador = campo.closest("form").querySelector(".contador");
    if (!contador) return;

    function atualizar() {
        contador.textContent = campo.value.length + "/" + (campo.maxLength > 0 ? campo.maxLength : 500);
    }

    campo.addEventListener("input", atualizar);
    atualizar();
});
