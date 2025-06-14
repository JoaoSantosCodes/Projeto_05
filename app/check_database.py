import sqlite3
import pandas as pd

def check_database():
    # Conectar ao banco de dados
    conn = sqlite3.connect('inventario.db')
    
    # Verificar dados da tabela lojas
    print("\n=== Dados da tabela lojas ===")
    df_lojas = pd.read_sql_query("SELECT COUNT(*) as total_lojas FROM lojas", conn)
    print(f"Total de lojas: {df_lojas['total_lojas'][0]}")
    print("\nPrimeiras 5 lojas:")
    df_lojas_sample = pd.read_sql_query("SELECT codigo, peop, nome, status FROM lojas LIMIT 5", conn)
    print(df_lojas_sample)
    
    # Verificar dados da tabela servicos_internet
    print("\n=== Dados da tabela servicos_internet ===")
    df_servicos = pd.read_sql_query("SELECT COUNT(*) as total_servicos FROM servicos_internet", conn)
    print(f"Total de serviços: {df_servicos['total_servicos'][0]}")
    print("\nPrimeiros 5 serviços:")
    df_servicos_sample = pd.read_sql_query("SELECT people, nome, operadora, velocidade FROM servicos_internet LIMIT 5", conn)
    print(df_servicos_sample)
    
    conn.close()

if __name__ == "__main__":
    check_database() 