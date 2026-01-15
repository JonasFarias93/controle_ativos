/**
 * gestao_kits.js
 * Gerencia a adição dinâmica de linhas na tabela de itens do kit
 */
document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-item');
    const tbody = document.getElementById('item-tbody');
    const totalForms = document.querySelector('[id$="-TOTAL_FORMS"]');
    const templateContainer = document.getElementById('empty-form-template');

    if (addButton && templateContainer) {
        addButton.addEventListener('click', function() {
            const currentFormCount = parseInt(totalForms.value);
            
            // Pega o HTML do molde (template)
            let newRowHtml = templateContainer.innerHTML;
            
            // Substitui o prefixo reservado __prefix__ pelo índice atual
            newRowHtml = newRowHtml.replace(/__prefix__/g, currentFormCount);
            
            // Insere a nova linha no final do corpo da tabela
            tbody.insertAdjacentHTML('beforeend', newRowHtml);
            
            // Atualiza o contador de formulários para o Django
            totalForms.value = currentFormCount + 1;
        });
    }
});