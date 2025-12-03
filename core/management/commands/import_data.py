# core/management/commands/import_data.py

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from core.models import Loja
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Importa dados de lojas de um arquivo CSV.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando a importação de dados de Lojas..."))

        # 1. Definir o nome do arquivo (deve estar na raiz do projeto)
        csv_file = 'lojas_base.csv'

        # =================================================================
        # 2. BLOCO CORRIGIDO: LÊ O ARQUIVO E CRIA O 'df' (DataFrame)
        # =================================================================
        try:
            # Tenta ler o CSV. Se falhar (arquivo não encontrado, por exemplo), 
            # o erro é capturado ANTES de tentar usar o 'df'.
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
            self.stdout.write(self.style.SUCCESS(f"Arquivo '{csv_file}' lido com sucesso."))
        
        except FileNotFoundError:
            # Se o arquivo não existir, gera um erro legível
            raise CommandError(f"Arquivo '{csv_file}' não encontrado na raiz do projeto.")
        except Exception as e:
            # Trata outros erros de leitura (codificação, formato)
            raise CommandError(f"Erro ao ler o CSV: {e}")
        # =================================================================

        lojas_processadas = 0
        for index, row in df.iterrows():
            try:
                filial_raw = str(row['Filial']) 
                if ',' in filial_raw:
                    filial_limpo = filial_raw.split(',')[0]
                else:
                    filial_limpo = filial_raw
                filial_id = int(filial_limpo)
                loja, created = Loja.objects.update_or_create(
            filial=filial_id,
                    
                    
                    # Os valores a serem ATUALIZADOS ou CRIADOS são definidos em 'defaults':
                    defaults={
                        'nome_filial': row['Nome Filial'],
                        'hist':row['Hist'],
                        'endereco': row['Endereço'],
                        'bairro': row['Bairro'],
                        'cidade': row['Cidade'],
                        'uf': row['UF'],
                        'logomarca': row['Logomarca'],
                        'telefone': row['Telefone'],
                        'ip_banco_12': row['IP Banco 12'],

                        # ... e todos os outros campos definidos no seu Loja Model
                        
                    }
                )

                lojas_processadas += 1
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Loja {loja.filial} (Nova) criada com sucesso."))
                else:
                    self.stdout.write(self.style.NOTICE(f"Loja {loja.filial} existente atualizada."))

            except KeyError as e:
                # Este erro ocorre se uma COLUNA mencionada em 'row[]' não existir no CSV
                raise CommandError(f"Coluna {e} não encontrada no CSV. Verifique os nomes das colunas e a digitação no seu script.")

        self.stdout.write(self.style.SUCCESS(f"Processo concluído. {lojas_processadas} registros processados."))