import pandas as pd
from pathlib import Path

excel_dir = Path("Excel")

for excel_file in excel_dir.glob("*.xlsx"):
    print(f"\n{'='*50}")
    print(f"Arquivo: {excel_file}")
    print(f"{'='*50}")
    try:
        df = pd.read_excel(excel_file)
        print("Colunas detectadas:")
        for col in df.columns:
            print(f"- {repr(col)}")
    except Exception as e:
        print(f"Erro ao ler {excel_file}: {e}") 