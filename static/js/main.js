// Lógica Global do Sistema
console.log("Scripts globais carregados com sucesso!");

document.addEventListener("DOMContentLoaded", function() {
    
    // Auto-close para os alertas de sucesso após 5 segundos
    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Aqui você pode adicionar máscaras de input ou outras funções globais
});