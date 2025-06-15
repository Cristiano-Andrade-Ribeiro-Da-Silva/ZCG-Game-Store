document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#form-busca');
    const campoBusca = document.querySelector('#campo-busca');
    const msgErro = document.querySelector('#mensagem-erro');

    form.addEventListener('submit', function(e) {
        const termo = campoBusca.value.trim();
        if (termo.length < 2) {
            e.preventDefault();
            msgErro.style.display = 'block';
        } else {
            msgErro.style.display = 'none';
        }
    });
});