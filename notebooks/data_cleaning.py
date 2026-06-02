# -*- coding: utf-8 -*-
"""
Ancile Talent Intelligence Dashboard
Data Cleaning & Validation Script
Run: python notebooks/data_cleaning.py
"""
import pandas as pd
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "candidates.csv")
df   = pd.read_csv(PATH)

print("=" * 55)
print("ANCILE DATASET — VALIDATION REPORT")
print("=" * 55)
print(f"Shape          : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Columns        : {df.columns.tolist()}")
print(f"\nNull values:\n{df.isnull().sum()}")
print(f"\nStatus distribution:\n{df['Status'].value_counts()}")
print(f"\nDomain distribution:\n{df['Domain'].value_counts()}")
print(f"\nExperience stats:\n{df['Experience_Years'].describe()}")
print(f"\nMatch Score stats:\n{df['Match_Score'].describe()}")
print(f"\nSample rows:")
print(df.head(5).to_string())
