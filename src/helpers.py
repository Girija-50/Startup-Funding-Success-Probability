"""
helpers.py — Utility functions for Startup Funding Analysis
Task 4 | AI & ML Internship Program
"""

import pandas as pd
import numpy as np
from scipy import stats


# ─── Data Loading & Cleaning ────────────────────────────────────────────────

def load_and_clean(filepath: str) -> pd.DataFrame:
    """
    Load the startup CSV and apply all cleaning steps.
    Returns a clean DataFrame ready for analysis.
    """
    df = pd.read_csv(filepath)
    df.drop_duplicates(inplace=True)

    # Normalise funding amount
    df['Funding Amount (USD)'] = (
        df['Funding Amount (USD)']
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )
    df['Funding Amount (USD)'] = pd.to_numeric(df['Funding Amount (USD)'], errors='coerce')

    # Target variable
    df['Funded'] = df['Funding Amount (USD)'].notna().astype(int)

    # Extract primary industry
    df['Primary Industry'] = df['Industry'].str.split(',').str[0].str.strip()

    # Parse date
    df['Last Funding Date'] = pd.to_datetime(
        df['Last Funding Date'], format='%B %Y', errors='coerce'
    )
    df['Funding Month'] = df['Last Funding Date'].dt.month_name()

    return df


# ─── Probability Functions ───────────────────────────────────────────────────

def prob_funded_by_keyword(df: pd.DataFrame, keyword: str, col: str = 'Industry') -> float:
    """
    P(funded | startup's `col` column contains `keyword`)
    Returns 0.0 if no matching rows.
    """
    subset = df[df[col].str.contains(keyword, na=False, case=False)]
    return float(subset['Funded'].mean()) if len(subset) > 0 else 0.0


def prob_amount_above_threshold(df: pd.DataFrame, stage: str, threshold: float) -> float:
    """
    P(funding amount > threshold | funding type == stage)
    """
    subset = df[df['Funding Type'] == stage]
    if len(subset) == 0:
        return 0.0
    return float((subset['Funding Amount (USD)'] > threshold).mean())


def sector_probability_table(df: pd.DataFrame, sectors: list) -> pd.DataFrame:
    """
    Build a table of P(funded) for each sector keyword.
    """
    rows = []
    base_rate = df['Funded'].mean()
    for s in sectors:
        p = prob_funded_by_keyword(df, s)
        rows.append({
            'Sector': s,
            'P(Funded)': round(p, 4),
            'vs Base Rate': round(p - base_rate, 4),
            'Above Average': p > base_rate,
        })
    return pd.DataFrame(rows).sort_values('P(Funded)', ascending=False)


# ─── Segmentation ────────────────────────────────────────────────────────────

def assign_segment(row) -> str:
    """
    Rule-based startup lifecycle segmentation by funding stage.
    """
    ft = str(row.get('Funding Type', ''))
    if ft in ['Series D', 'Series E', 'Private Equity', 'IPO']:
        return 'High-Growth / Late Stage'
    elif ft in ['Series B', 'Series C']:
        return 'Growth Stage'
    elif ft == 'Series A':
        return 'Early Growth'
    elif ft == 'Seed':
        return 'Early Stage (Seed)'
    elif ft in ['Pre-Seed', 'Angel']:
        return 'Very Early Stage'
    else:
        return 'Other / Undisclosed'


# ─── Hypothesis Testing ──────────────────────────────────────────────────────

def run_anova(df: pd.DataFrame, group_col: str, value_col: str, min_n: int = 3):
    """
    One-way ANOVA across groups defined by group_col.
    Returns (F-statistic, p-value, interpretation string).
    """
    groups = [
        grp[value_col].dropna().values
        for _, grp in df.groupby(group_col)
        if grp[value_col].notna().sum() >= min_n
    ]
    if len(groups) < 2:
        return None, None, 'Not enough groups for ANOVA'
    f_stat, p_val = stats.f_oneway(*groups)
    interpretation = (
        f'REJECT H₀ — {group_col} significantly influences {value_col} (p={p_val:.4f})'
        if p_val < 0.05
        else f'FAIL TO REJECT H₀ — No significant difference (p={p_val:.4f})'
    )
    return round(f_stat, 4), round(p_val, 6), interpretation


def run_chi_square(df: pd.DataFrame, cat_col: str, target_col: str = 'Funded'):
    """
    Chi-Square test of independence between cat_col and target_col.
    Returns (chi2, p-value, dof, interpretation string).
    """
    contingency = pd.crosstab(df[cat_col], df[target_col])
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    interpretation = (
        f'REJECT H₀ — {cat_col} and {target_col} are NOT independent (p={p_val:.4f})'
        if p_val < 0.05
        else f'FAIL TO REJECT H₀ — {cat_col} and {target_col} appear independent (p={p_val:.4f})'
    )
    return round(chi2, 4), round(p_val, 6), dof, interpretation


def run_ttest(df: pd.DataFrame, keyword: str, value_col: str = 'Funding Amount (USD)'):
    """
    Welch T-Test comparing startups mentioning `keyword` in Industry vs others.
    Returns (t-statistic, p-value, interpretation string).
    """
    mask = df['Industry'].str.contains(keyword, na=False, case=False)
    group_a = df[mask][value_col].dropna()
    group_b = df[~mask][value_col].dropna()
    if len(group_a) < 3 or len(group_b) < 3:
        return None, None, 'Insufficient data for T-Test'
    t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)
    interpretation = (
        f'REJECT H₀ — "{keyword}" startups differ significantly in {value_col} (p={p_val:.4f})'
        if p_val < 0.05
        else f'FAIL TO REJECT H₀ — No significant difference (p={p_val:.4f})'
    )
    return round(t_stat, 4), round(p_val, 6), interpretation


# ─── Reporting ───────────────────────────────────────────────────────────────

def descriptive_summary(series: pd.Series, label: str = 'Variable') -> dict:
    """
    Return a dict of key descriptive statistics for a numeric Series.
    """
    return {
        'label'   : label,
        'n'       : int(series.notna().sum()),
        'mean'    : round(series.mean(), 2),
        'median'  : round(series.median(), 2),
        'std'     : round(series.std(), 2),
        'min'     : round(series.min(), 2),
        'max'     : round(series.max(), 2),
        'q25'     : round(series.quantile(0.25), 2),
        'q75'     : round(series.quantile(0.75), 2),
        'q90'     : round(series.quantile(0.90), 2),
    }