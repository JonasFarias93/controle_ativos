// static/js/registro_bipagem.js

function atualizarKit() {
    const kitId = document.getElementById('id_kit_utilizado').value;
    const url = new URL(window.location);
    if (kitId) {
        url.searchParams.set('kit', kitId);
    } else {
        url.searchParams.delete('kit');
    }
    window.location.href = url.href;
}

document.addEventListener('DOMContentLoaded', function() {
    // Captura todos os inputs de texto dentro da tabela de bipes
    const table = document.querySelector('table');
    if (!table) return;

    const inputs = Array.from(table.querySelectorAll('input[type="text"]'));
    
    inputs.forEach((input, index) => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); 
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                } else {
                    document.querySelector('button[type="submit"]').focus();
                }
            }
        });
    });

    // Foca no primeiro campo disponível para ganhar tempo
    const firstInput = inputs[0];
    if (firstInput) firstInput.focus();
});


// static/js/registro_bipagem.js

document.addEventListener('DOMContentLoaded', function() {
    // 1. Lógica para atualizar a página quando trocar o Kit
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

    // 2. Lógica de Autopular campos com Enter (Leitor de Código de Barras)
    const inputs = Array.from(document.querySelectorAll('input[type="text"]'));
    
    inputs.forEach((input, index) => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Impede o envio precoce do formulário
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                } else {
                    // Se for o último, foca no botão de finalizar
                    const btnSubmit = document.querySelector('button[type="submit"]');
                    if (btnSubmit) btnSubmit.focus();
                }
            }
        });
    });

    // 3. Foco inicial no primeiro campo de bipagem se o kit estiver carregado
    const firstBip = document.querySelector('.input-bip');
    if (firstBip) firstBip.focus();
});