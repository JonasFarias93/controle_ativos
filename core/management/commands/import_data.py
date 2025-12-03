import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from core.models import Loja
from django.db import IntegrityError
import numpy as np # Adicionado

class Command(BaseCommand):
    help = 'Importa dados de lojas de um arquivo CSV.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando a importação de dados de Lojas..."))

        csv_file = 'lojas_base.csv'

        try:
            # CORREÇÃO 1: Usar dtype=str para ler todos os campos como strings e evitar '.0'
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8', dtype=str, na_values=['', 'nan', 'NaN'])
            self.stdout.write(self.style.SUCCESS(f"Arquivo '{csv_file}' lido com sucesso. Colunas: {list(df.columns)}"))
        
        except FileNotFoundError:
            raise CommandError(f"Arquivo '{csv_file}' não encontrado na raiz do projeto.")
        except Exception as e:
            raise CommandError(f"Erro ao ler o CSV: {e}")

        
        # FUNÇÃO DE SEGURANÇA E LIMPEZA: Trata valores vazios/NaN e remove o ".0" de CNPJ e outros números
        def get_safe_value(row, col_name, required=False):
            value = row.get(col_name)
            
            # 1. Trata valores nulos ou vazios
            if value is None or (isinstance(value, str) and value.strip() == '') or (isinstance(value, str) and value.lower() in ('none', 'nan')):
                return '' if required else None
            
            # 2. Lógica principal: TENTA REMOVER O '.0' de números (IMPORTANTE PARA CNPJ)
            if isinstance(value, str):
                temp_value = value.strip()
                try:
                    # Verifica se a string contém o ponto decimal
                    if '.' in temp_value:
                        float_val = float(temp_value)
                        # Verifica se é um número que termina em .0 (ou seja, é um inteiro lido como float)
                        if float_val == int(float_val):
                            return str(int(float_val))
                except ValueError:
                    # Não é um float, segue como string normal
                    pass
            
            # 3. Retorna o valor original limpo (apenas espaços em branco removidos)
            return value.strip() if isinstance(value, str) else value


        lojas_processadas = 0
        
        # === MAPA DE COLUNAS ===
        COLUMN_MAP = {
            'Filial': 'filial',
            'Hist': 'hist',
            'Nome Filial': 'nome_filial',
            'Insc Estadual': 'insc_estadual', 
            'CNPJ': 'cnpj', 
            'Endereço': 'endereco',
            'Bairro': 'bairro',
            'Cidade': 'cidade',
            'UF': 'uf',
            'Região': 'regiao', 
            'Logomarca': 'logomarca',
            'Telefone': 'telefone',
            'IP Banco 12': 'ip_banco_12',
        }
        
        for index, row in df.iterrows():
            filial_id = None
            try:
                # 1. TRATAMENTO DO FILIAL (Chave) - Limpeza de '.0' e conversão para int
                filial_raw = get_safe_value(row, 'Filial', required=True)
                if not filial_raw:
                     self.stdout.write(self.style.WARNING(f"Ignorando linha {index}: Campo Filial vazio."))
                     continue
                
                try:
                    filial_id = int(filial_raw)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Ignorando linha {index}: Filial '{filial_raw}' não é um número válido."))
                    continue

                # 2. DEFINIÇÃO DOS VALORES (Com Segurança e Limpeza de '.0')
                safe_data = {}
                for csv_name, model_name in COLUMN_MAP.items():
                    # Campos obrigatórios no modelo (null=False)
                    required = model_name in ['nome_filial', 'endereco', 'bairro', 'cidade', 'uf']
                    
                    # Usa a função de limpeza que remove o '.0'
                    value = get_safe_value(row, csv_name, required=required)
                    safe_data[model_name] = value

                # Remove filial do dicionário, pois é o argumento de busca
                del safe_data['filial'] 

                # 3. UPDATE OR CREATE
                loja, created = Loja.objects.update_or_create(
                    filial=filial_id,
                    defaults=safe_data 
                )

                lojas_processadas += 1
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Loja {loja.filial} (Nova) criada com sucesso."))
                else:
                    self.stdout.write(self.style.NOTICE(f"Loja {loja.filial} existente atualizada."))
            
            except KeyError as e:
                # Este erro ocorre se um cabeçalho não existir no CSV.
                raise CommandError(f"Coluna '{e.args[0]}' não encontrada no CSV. Verifique se o nome '{e.args[0]}' está no seu CSV.")
            
            except IntegrityError as e:
                 # Tratamento de erro de integridade (e.g., campo NOT NULL vazio)
                 self.stdout.write(self.style.ERROR(f"ERRO DE INTEGRIDADE: Loja {filial_id} (Índice {index}). Causa: {e}"))
                 continue
            
            except Exception as e:
                 # Tratamento de erros genéricos
                 self.stdout.write(self.style.ERROR(f"Erro inesperado ao processar Loja {filial_id} (Índice {index}): {e}"))
                 continue
        
        self.stdout.write(self.style.SUCCESS(f"Processo concluído. {lojas_processadas} registros processados."))