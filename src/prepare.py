"""Подготовка и очистка данных: data/student-por.csv -> data/clean.csv."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
raw = pd.read_csv(ROOT / "data" / "student-por.csv", sep=";")

df = raw.drop_duplicates().copy()

cat_cols = df.select_dtypes(include=["object", "string"]).columns
for col in cat_cols:
    df[col] = df[col].astype("string").str.strip()

for col in ["G1", "G2", "G3"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[(df[col] < 0) | (df[col] > 20), col] = np.nan

df.loc[(df["age"] < 14) | (df["age"] > 25), "age"] = np.nan
df.loc[df["absences"] < 0, "absences"] = np.nan

df.to_csv(ROOT / "data" / "clean.csv", index=False)
print("Очистка завершена:", raw.shape, "->", df.shape)
print("Пропусков всего:", int(df.isna().sum().sum()))
print("Дубликатов:", int(df.duplicated().sum()))