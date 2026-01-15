# 📦  Sistema de Controle de Movimentação de Ativos
##  <p align="center">📝 Visão Geral</p>
&nbsp;&nbsp;&nbsp;&nbsp;Este software digitaliza a operação do setor de Expansão, substituindo o uso fragmentado de planilhas de Excel por uma plataforma unificada de governança de dados. <br>O sistema gerencia todo o ciclo de saída de equipamentos — desde a demanda inicial do projeto até a coleta final — garantindo que cada movimentação seja rastreável e segura. 


### <p align="center">🎯 Objetivos Estratégicos</p>

 - Centralização de Dados: Unifica informações operacionais em uma única "fonte da verdade", eliminando perdas de dados críticas. 

 - Inteligência e Auditoria: Transforma dados brutos em históricos estruturados para consultas rápidas e processos de auditoria facilitados. 

 - Eficiência Operacional: Automatiza a validação física de itens através da bipagem, assegurando que o kit enviado à loja esteja 100% correto. 

 - Credibilidade da Informação: Garante a integridade do processo fiscal e logístico, travando etapas dependentes (ex: NF só após bipagem). 


### <p align="center">🛠️ Stack Tecnológica</p>

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem** | <img src="https://skillicons.dev/icons?i=py" height="25" vertical-align="middle" /> Python |
| **Framework Web** | <img src="https://skillicons.dev/icons?i=django" height="25" vertical-align="middle" /> Django |
| **Frontend** | <img src="https://skillicons.dev/icons?i=html,css,js,bootstrap" height="25" vertical-align="middle" /> |
| **Banco de Dados** | 📂 (Definindo estrutura relacional) |

### <p align="center">🔄 Fluxo de Trabalho (Workflow)</p>
O sistema opera como uma máquina de estados, acompanhando o ciclo de vida de um "Card" de expedição:
 - Pendente: O registro é criado após a demanda do Projeto/Estoque.
 - Em Bipagem: Início da conferência física dos números de série.
 - Aguardando NF: Todos os itens previstos foram bipados com sucesso.
 - Aguardando Coleta: Informações fiscais (Número da NF e Chamado) foram inseridas.
 - Concluído: Ciclo encerrado e registro movido para o histórico.

### <p align="center">📋 Funcionalidades Principais</p>

 - Dossiê da Expedição: Cards interativos que funcionam como ordens de serviço.
 - Bipagem Inteligente: O sistema gera "slots" vazios baseados no Kit escolhido e só permite avançar quando todos forem preenchidos.
 - Gestão de Pendências: Visualização em estilo "Sanfona" na Home para monitorar processos em aberto.
 - Histórico de Auditoria: Registro de quem realizou a bipagem e quem finalizou o processo.

### <p align="center">🚀 Como Executar (Em desenvolvimento)</p>
...

