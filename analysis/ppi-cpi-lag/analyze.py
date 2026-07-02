import csv, math

def load(path, col):
    d = {}
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            v = row[col].strip()
            d[row['observation_date']] = float(v) if v else None
    return d

cpi = load('cpi.csv', 'CPIAUCSL')
ppi = load('ppi.csv', 'PPIFIS')

dates = sorted(cpi.keys())

# Interpolate a single missing CPI value (2025-10 is blank in source)
for i, dt in enumerate(dates):
    if cpi[dt] is None:
        prev = cpi[dates[i-1]]; nxt = cpi[dates[i+1]]
        cpi[dt] = round((prev+nxt)/2, 3)
        print(f"NOTE: interpolated missing CPI {dt} = {cpi[dt]}")

def mom(series, dates):
    out = {}
    for i in range(1, len(dates)):
        a, b = series[dates[i-1]], series[dates[i]]
        out[dates[i]] = (b/a - 1)*100
    return out

def yoy(series, dates):
    out = {}
    for i in range(12, len(dates)):
        a, b = series[dates[i-12]], series[dates[i]]
        out[dates[i]] = (b/a - 1)*100
    return out

cpi_mom, ppi_mom = mom(cpi, dates), mom(ppi, dates)
cpi_yoy, ppi_yoy = yoy(cpi, dates), yoy(ppi, dates)

# last 24 months
recent = dates[-24:]
print("\n=== Last 24 months: index levels + YoY% + MoM% ===")
print(f"{'month':<9}{'PPI_idx':>9}{'CPI_idx':>9}{'PPI_yoy':>9}{'CPI_yoy':>9}{'PPI_mom':>9}{'CPI_mom':>9}")
for dt in recent:
    m = dt[:7]
    print(f"{m:<9}{ppi[dt]:>9.2f}{cpi[dt]:>9.2f}"
          f"{ppi_yoy.get(dt,float('nan')):>9.2f}{cpi_yoy.get(dt,float('nan')):>9.2f}"
          f"{ppi_mom.get(dt,float('nan')):>9.2f}{cpi_mom.get(dt,float('nan')):>9.2f}")

def pearson(xs, ys):
    n = len(xs)
    if n < 3: return float('nan')
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    sx = math.sqrt(sum((x-mx)**2 for x in xs))
    sy = math.sqrt(sum((y-my)**2 for y in ys))
    return cov/(sx*sy) if sx and sy else float('nan')

def lagcorr(ppi_series, cpi_series, dates, maxlag=6):
    # positive lag = PPI leads CPI by `lag` months
    res = []
    for lag in range(0, maxlag+1):
        xs, ys = [], []
        for i in range(len(dates)):
            di = dates[i]
            if i-lag < 0: continue
            dp = dates[i-lag]  # PPI at earlier month
            if dp in ppi_series and di in cpi_series:
                xs.append(ppi_series[dp]); ys.append(cpi_series[di])
        res.append((lag, pearson(xs, ys), len(xs)))
    return res

# Use full available window for statistical power
print("\n=== Cross-correlation: PPI(t-lag) vs CPI(t), YoY changes (full window from 2022) ===")
yoy_dates = [d for d in dates if d in cpi_yoy and d in ppi_yoy]
for lag, r, n in lagcorr(ppi_yoy, cpi_yoy, yoy_dates):
    print(f"  lag {lag} mo: r = {r:+.3f}  (n={n})")

print("\n=== Cross-correlation: PPI(t-lag) vs CPI(t), MoM changes (last 24 mo) ===")
mom_dates = [d for d in dates if d in cpi_mom and d in ppi_mom][-24:]
for lag, r, n in lagcorr(ppi_mom, cpi_mom, mom_dates):
    print(f"  lag {lag} mo: r = {r:+.3f}  (n={n})")

print("\n=== Cross-correlation: PPI(t-lag) vs CPI(t), MoM 3-mo smoothed (full) ===")
def smooth3(series, dates):
    out={}
    for i in range(2,len(dates)):
        d=dates[i]
        vals=[series.get(dates[i-k]) for k in range(3)]
        if all(v is not None for v in vals): out[d]=sum(vals)/3
    return out
cpi_s, ppi_s = smooth3(cpi_mom, dates), smooth3(ppi_mom, dates)
s_dates=[d for d in dates if d in cpi_s and d in ppi_s]
for lag, r, n in lagcorr(ppi_s, cpi_s, s_dates):
    print(f"  lag {lag} mo: r = {r:+.3f}  (n={n})")
