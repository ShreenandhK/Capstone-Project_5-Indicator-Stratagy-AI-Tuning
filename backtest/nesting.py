"""Nesting + attribution check for a monotone filter sweep: loose ⊇ mid ⊇ tight (by entry_time, direction).

usage (from backtest/): python nesting.py 11 18 17     -> loose=run 11 (±53), mid=run 18 (±45), tight=run 17 (±40)
"""
import sys

import pandas as pd

loose, mid, tight = sys.argv[1:4]


def load(r):
    return pd.read_csv(f"results/run_{r}/trades.csv").set_index(["entry_time", "direction"])


L, M, T = load(loose), load(mid), load(tight)
for name, small, big in ((f"{tight}⊆{mid}", T, M), (f"{mid}⊆{loose}", M, L), (f"{tight}⊆{loose}", T, L)):
    inside = small.index.isin(big.index).sum()
    print(f"{name}: {inside} of {len(small)} inside ({'NESTED' if inside == len(small) else 'NOT nested'}); "
          f"extra in small not in big: {len(small) - inside}")

sh = M.index.intersection(L.index)
same_exit = ((L.loc[sh, "exit_time"] == M.loc[sh, "exit_time"]) & ((L.loc[sh, "exit_price"] - M.loc[sh, "exit_price"]).abs() < 1e-9)).sum()
print(f"run {mid} vs {loose}: shared {len(sh)}, identical exits {same_exit}")

band_outer = L.index.difference(M.index)          # removed going loose -> mid
band_inner = M.index.difference(T.index)          # removed going mid -> tight
print(f"removed {loose}->{mid}: {len(band_outer)} trades, pnl(in {loose}) {L.loc[band_outer, 'pnl'].sum():.2f}, "
      f"median {L.loc[band_outer, 'return_pct'].median():.3f}%")
print(f"removed {mid}->{tight}: {len(band_inner)} trades, pnl(in {mid}) {M.loc[band_inner.intersection(M.index), 'pnl'].sum():.2f}, "
      f"median {M.loc[band_inner.intersection(M.index), 'return_pct'].median():.3f}%")
for r, t in ((loose, L), (mid, M), (tight, T)):
    p = t["pnl"].sort_values(ascending=False)
    gw, gl = p[p > 0].sum(), -p[p < 0].sum()
    ex2 = p.iloc[2:]
    print(f"run {r}: trades {len(t)} net {p.sum():.2f} ex-top-2 {ex2.sum():.2f} "
          f"PF {gw / gl:.3f} PF-ex-top-2 {ex2[ex2 > 0].sum() / -ex2[ex2 < 0].sum():.3f} median {t['return_pct'].median():.3f}%")
