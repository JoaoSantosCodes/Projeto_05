import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
import re
import unicodedata

class Database:
    def __init__(self, db_name="inventario.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()

    def inspect_excel_file(self, excel_file):
        """Inspeciona a estrutura do arquivo Excel"""
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(excel_file)
            
            print(f"\nEstrutura do arquivo: {excel_file}")
            print("\nColunas encontradas:")
            for col in df.columns:
                print(f"- {col}")
            
            print("\nPrimeiras 5 linhas:")
            print(df.head())
            
            print("\nInformações do DataFrame:")
            print(df.info())
            
            return df
        except Exception as e:
            print(f"Erro ao inspecionar arquivo Excel: {e}")
            return None

    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        # Tabela de Lojas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lojas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo INTEGER UNIQUE,
                peop TEXT,
                nome TEXT NOT NULL,
                status TEXT,
                politica_comercial INTEGER,
                regiao_ggl TEXT,
                regiao_gr TEXT,
                regiao_div TEXT,
                nome_ggl TEXT,
                nome_gr TEXT,
                nome_div TEXT,
                regiao_im TEXT,
                endereco TEXT,
                bairro TEXT,
                cidade TEXT,
                uf TEXT,
                cep TEXT,
                latitude TEXT,
                longitude TEXT,
                nome_fachada TEXT,
                data_inauguracao TEXT,
                safra TEXT,
                cluster TEXT,
                cluster_abrev TEXT,
                parcelamento TEXT,
                cluster_parcelamento TEXT,
                telefone1 TEXT,
                telefone2 TEXT,
                celular TEXT,
                email TEXT,
                horario_semana TEXT,
                horario_sabado TEXT,
                horario_domingo TEXT,
                funcionamento TEXT,
                tipo_loja TEXT,
                fachada TEXT,
                psicotropicos TEXT,
                farmacia_pop TEXT,
                servicos_farmaceuticos TEXT,
                vacinas TEXT,
                ifood TEXT,
                rappi TEXT,
                corner_shop TEXT,
                super_expressa TEXT,
                vagas_estacionamento TEXT,
                bicicletario TEXT,
                pdvs_ativos INTEGER,
                imobiliario TEXT,
                cd_supridor TEXT,
                inscricao_estadual TEXT,
                cnpj TEXT,
                centro_custos TEXT,
                vd_novo TEXT,
                data_unificacao TEXT,
                cnpj_novo TEXT,
                data_inativacao TEXT,
                realocacao TEXT,
                data_virada TEXT,
                eac TEXT,
                dengue_covid TEXT,
                injetaveis TEXT,
                reforma TEXT,
                data_atualizacao TEXT
            )
        ''')

        # Tabela de Serviços de Internet
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicos_internet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loja_id INTEGER,
                status_loja TEXT,
                people TEXT,
                nome TEXT,
                centro_custo TEXT,
                operadora TEXT,
                contrato TEXT,
                circuito_designacao TEXT,
                novo_circuito_designacao TEXT,
                velocidade TEXT,
                servico TEXT,
                id_vivo TEXT,
                novo_id_vivo TEXT,
                status_servico TEXT,
                observacao TEXT,
                custo REAL,
                multa REAL,
                data_atualizacao TEXT,
                FOREIGN KEY (loja_id) REFERENCES lojas (id)
            )
        ''')

        self.conn.commit()

    def normalize_col(self, col):
        # Remove acentos, converte para minúsculo, remove espaços extras e quebras de linha
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
        col = col.lower()
        col = re.sub(r'\s+', ' ', col)
        col = col.strip()
        return col

    def normalize_columns(self, df):
        df.columns = [self.normalize_col(col) for col in df.columns]
        return df

    def import_lojas_data(self, excel_file):
        """Importa dados do arquivo de lojas"""
        try:
            df = pd.read_excel(excel_file)
            df = self.normalize_columns(df)
            # Dicionário de mapeamento: Excel padronizado -> banco
            mapping = {
                'codigo': 'codigo',
                'peop': 'peop',
                'lojas': 'nome',
                'status': 'status',
                'politica coml.': 'politica_comercial',
                'regiao ggl': 'regiao_ggl',
                'regiao gr': 'regiao_gr',
                'regiao div': 'regiao_div',
                'nome ggl': 'nome_ggl',
                'nome gr': 'nome_gr',
                'nome div': 'nome_div',
                'regiao im': 'regiao_im',
                'endereco': 'endereco',
                'bairro': 'bairro',
                'cidade': 'cidade',
                'uf': 'uf',
                'cep': 'cep',
                'latitude': 'latitude',
                'longitude': 'longitude',
                'nome da fachada': 'nome_fachada',
                'inaug.': 'data_inauguracao',
                'safra': 'safra',
                'cluster': 'cluster',
                'cluster abrev.': 'cluster_abrev',
                'parcelamento': 'parcelamento',
                'cluster de parcelamento': 'cluster_parcelamento',
                'telefone1': 'telefone1',
                'telefone2': 'telefone2',
                'celular': 'celular',
                'e-mail': 'email',
                '2a a 6a': 'horario_semana',
                'sab': 'horario_sabado',
                'dom': 'horario_domingo',
                'func.': 'funcionamento',
                'tipo loja': 'tipo_loja',
                'fachada': 'fachada',
                'psicotropicos': 'psicotropicos',
                'farmacia pop.': 'farmacia_pop',
                'servicos farmaceuticos': 'servicos_farmaceuticos',
                'vacinas': 'vacinas',
                'ifood': 'ifood',
                'rappi': 'rappi',
                'corner shop': 'corner_shop',
                'super expressa': 'super_expressa',
                'vagas/estacionamento': 'vagas_estacionamento',
                'bicicletario': 'bicicletario',
                'pdvs ativos': 'pdvs_ativos',
                'imobiliario': 'imobiliario',
                'cd supridor': 'cd_supridor',
                'inscr. estadual': 'inscricao_estadual',
                'cnpj': 'cnpj',
                'centro de custos': 'centro_custos',
                'vd novo': 'vd_novo',
                'data da unificacao': 'data_unificacao',
                'cnpj novo': 'cnpj_novo',
                'data inativacao': 'data_inativacao',
                'realocacao': 'realocacao',
                'data da virada': 'data_virada',
                'eac': 'eac',
                'dengue/covid': 'dengue_covid',
                'injetaveis': 'injetaveis',
                'reforma': 'reforma',
            }
            for _, row in df.iterrows():
                values = []
                for excel_col, db_col in mapping.items():
                    values.append(row.get(excel_col, None))
                values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.cursor.execute(f'''
                    INSERT OR REPLACE INTO lojas (
                        {', '.join(mapping.values())}, data_atualizacao
                    ) VALUES ({', '.join(['?'] * (len(mapping) + 1))})
                ''', values)
            self.conn.commit()
            print(f"Dados de lojas importados com sucesso!")
        except Exception as e:
            print(f"Erro ao importar dados de lojas: {e}")

    def import_servicos_internet(self, excel_file):
        """Importa dados do arquivo de serviços de internet"""
        try:
            df = pd.read_excel(excel_file)
            df = self.normalize_columns(df)
            mapping = {
                'status loja': 'status_loja',
                'people': 'people',
                'nome': 'nome',
                'centro de custo': 'centro_custo',
                'operadora': 'operadora',
                'contrato': 'contrato',
                'circuito/designacao': 'circuito_designacao',
                'novo circuito/designacao': 'novo_circuito_designacao',
                'velocidade': 'velocidade',
                'servico': 'servico',
                'id vivo': 'id_vivo',
                'novo id vivo': 'novo_id_vivo',
                'status servico': 'status_servico',
                'observacao': 'observacao',
                'custo': 'custo',
                'multa': 'multa',
            }
            for _, row in df.iterrows():
                # Encontrar loja_id pelo people
                self.cursor.execute('SELECT id FROM lojas WHERE peop = ?', (row.get('people', None),))
                loja_result = self.cursor.fetchone()
                loja_id = loja_result[0] if loja_result else None
                # Conversão de valores
                try:
                    custo = float(str(row.get('custo', '')).replace(',', '.')) if pd.notna(row.get('custo', None)) and row.get('custo', None) not in [None, '-'] else None
                except (ValueError, TypeError):
                    custo = None
                try:
                    multa = float(str(row.get('multa', '')).replace(',', '.')) if pd.notna(row.get('multa', None)) else None
                except (ValueError, TypeError):
                    multa = None
                values = [
                    loja_id,
                    row.get('status loja', None),
                    row.get('people', None),
                    row.get('nome', None),
                    row.get('centro de custo', None),
                    row.get('operadora', None),
                    row.get('contrato', None),
                    row.get('circuito/designacao', None),
                    row.get('novo circuito/designacao', None),
                    row.get('velocidade', None),
                    row.get('servico', None),
                    row.get('id vivo', None),
                    row.get('novo id vivo', None),
                    row.get('status servico', None),
                    row.get('observacao', None),
                    custo,
                    multa,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
                self.cursor.execute(f'''
                    INSERT INTO servicos_internet (
                        loja_id, status_loja, people, nome, centro_custo, operadora, contrato, circuito_designacao, novo_circuito_designacao, velocidade, servico, id_vivo, novo_id_vivo, status_servico, observacao, custo, multa, data_atualizacao
                    ) VALUES ({', '.join(['?'] * 18)})
                ''', values)
            self.conn.commit()
            print(f"Dados de serviços de internet importados com sucesso!")
        except Exception as e:
            print(f"Erro ao importar dados de serviços de internet: {e}")

def main():
    # Inicializa o banco de dados
    db = Database()
    db.connect()
    db.create_tables()
    
    # Importa dados dos arquivos Excel
    excel_dir = Path("Excel")
    for excel_file in excel_dir.glob("*.xlsx"):
        print(f"\nProcessando arquivo: {excel_file}")
        if "Lojas" in excel_file.name:
            db.import_lojas_data(excel_file)
        elif "Inventário" in excel_file.name:
            db.import_servicos_internet(excel_file)
    
    db.close()

if __name__ == "__main__":
    main() 