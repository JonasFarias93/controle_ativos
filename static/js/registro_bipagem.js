// static/js/registro_bipagem.js

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Lógica para atualizar a página quando trocar o Kit (Dropdown)
    const kitSelect = document.querySelector('select[name="kit_utilizado"]');
    if (kitSelect) {
        kitSelect.addEventListener('change', function() {
            const kitId = this.value;
            const url = new URL(window.location);
            if (kitId) {
                url.searchParams.set('kit', kitId);
            } else {
                url.searchParams.delete('kit');
            }
            window.location.href = url.href;
        });
    }

    // 2. Lógica de Autopular campos com Enter (Workflow do Leitor)
    // O segredo está no :not([readonly]) -> ele ignora campos N/A
    const inputs = Array.from(document.querySelectorAll('input[type="text"]:not([readonly])'));
    
    inputs.forEach((input, index) => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Impede o envio acidental do formulário
                
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                } else {
                    // Se for o último campo real, foca no botão de finalizar
                    const btnSubmit = document.querySelector('button[type="submit"]');
                    if (btnSubmit) btnSubmit.focus();
                }
            }
        });
    });

    // 3. Foco inicial automático
    // Tenta focar no primeiro campo de bipagem que não seja somente leitura
    if (inputs.length > 0) {
        inputs[0].focus();
    }
});