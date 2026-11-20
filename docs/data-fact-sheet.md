# Data fact sheet

Profile of the three course files as of 2026-11-20. Source: [course dataset README](https://github.com/opencampus-sh/intro-to-data-science-and-ml/blob/main/data/bakery/README.md), provided by meteolytix GmbH for the course; license not stated. All numbers below come from running the profiling code on the raw files (read-only, loaded from the course URL).

## Sales – `umsatzdaten_gekuerzt.csv`

- **Shape / grain:** 9,334 rows × 4 columns (`id`, `Datum`, `Warengruppe`, `Umsatz`). One row = one product group on one day **with sales**.
- **Keys:** `id` is unique; `Datum` + `Warengruppe` is unique. `id` always equals `YYMMDD` × 10 + product group.
- **Time coverage:** 2013-07-01 – 2018-07-31 (1,857 calendar days). 1,819 days have sales; the 38 days without any sales are mostly public holidays (25/26 Dec, 1 Jan, Good Friday, 1 May) plus some single days (e.g. 2016-07-07, 2017-10-23).
- **Open days per weekday:** Mon 258 · Tue 262 · Wed 263 · Thu 259 · Fri 256 · Sat 261 · Sun 260 (the branch opens on Sundays).
- **Missing values:** none in any column.
- **Range:** `Umsatz` 7.05 – 1,879.46, median 161.9; no zero or negative values.

| Group | Rows | Mean | Median | Min | Max |
|---|---|---|---|---|---|
| 1 Bread | 1,819 | 122.1 | 120.1 | 23.1 | 416.8 |
| 2 Rolls | 1,819 | 402.5 | 370.8 | 175.0 | 1,203.4 |
| 3 Croissants | 1,819 | 163.3 | 142.8 | 37.7 | 565.9 |
| 4 Confectionery | 1,766 | 88.0 | 80.0 | 27.4 | 430.5 |
| 5 Cakes | 1,819 | 276.8 | 266.0 | 121.5 | 1,879.5 |
| 6 Seasonal bread | 292 | 66.9 | 62.9 | 7.1 | 172.9 |

### Findings

- **New Year's Eve (31 Dec) is extreme for cakes:** 1,432–1,879 in each of the 5 years (median day: 266). These are the 5 largest values in the whole dataset. 31 Dec is not a public holiday, so a public-holiday calendar does not mark it.
- **2014-05-05 (Monday) is a one-off peak:** rolls 1,203, cakes 749, croissants 566, the highest values for rolls and croissants. No explanation in the data.
- **46 rows are extreme** (more than 3 × IQR from the quartiles of their group), led by the two points above.
- **Confectionery (4) has no row on 53 open days:** 16 in 2013, 23 in 2014, 10 in 2015, 4 in 2016, **none after 2016**; 16 of them in December. The validation year has group 4 on all 357 open days.
- **Seasonal bread (6):** 5 seasons. Start varies 24 Oct – 3 Nov, end 27 Dec – 6 Jan. 15 open days inside a season have no group-6 row. Training covers 4 seasons (2013–2016), validation 1 (2017: 30 Oct – 27 Dec, 56 days).
- **Split sizes (decided in block 4):** training (to 2017-07-31) 7,493 rows; validation (2017-08-01 on) 1,841 rows.

## Weather – `wetter.csv`

- **Shape / grain:** 2,601 rows × 5 columns. One row = one day in Kiel. `Datum` is unique.
- **Time coverage:** 2012-01-01 – 2019-08-01, with 169 days missing (2012: 33, 2013: 120, 2016: 1, 2017: 2, 2018: 12, 2019: 1).
  - Missing inside the sales period: **2016-12-11, 2017-10-04, 2017-10-05** (16 sales rows).
  - Missing inside the Kaggle test year: **13 days**.
- **Columns and ranges:**
  - `Bewoelkung` (cloud cover): 0–8 octas; 10 missing, all **consecutive 2017-10-30 – 2017-11-08** (validation year).
  - `Temperatur`: −10.25 to 32.67 °C; none missing.
  - `Windgeschwindigkeit`: 3–35 m/s; none missing.
  - `Wettercode` (WMO code): 41 distinct codes, most common 61 (slight rain, 594 days); **669 missing (26 %)**.
- **`Wettercode` is not missing at random:**
  - Days without a code are clearer (mean cloud 3.3 vs 5.3 octas) and warmer (15.4 vs 10.9 °C), consistent with "no notable weather reported".
  - The missing share **falls over time**: 39 % (2012), 36 %, 35 %, 27 %, 24 %, 18 %, 11 % (2018). The reporting practice changed, so the same weather may be coded differently in early and late years.

## Kiel Week – `kiwo.csv`

- 72 rows, one per festival day; `Datum` unique; `KielerWoche` always 1.
- 9 consecutive days per year, 2012–2019 (late June).
- All 45 festival days inside the sales period are open days. In **training: 4 Kiel Weeks** (2014–2017; the 2013 one is before the data starts); **validation: 1** (2018-06-16 – 06-24); test year: 2019-06-22 – 06-30.

## Joins (on `Datum`, left join onto sales)

| Join | Rows before → after | Sales rows matched |
|---|---|---|
| Sales ← weather | 9,334 → 9,334 | 99.83 % (16 rows from the 3 missing weather days) |
| Sales ← Kiel Week | 9,334 → 9,334 | 223 rows flagged; all others missing → set to 0 |

Neither join changes the row count (weather and Kiel Week dates are unique).

## Outlier analysis (2026-11-20)

**Method:** For every row, divide turnover by the median turnover of the same product group on the same weekday within ±28 days (the day itself excluded). Ratio 1 = normal; flagged if ≥ 2 or ≤ 0.4. Each flagged day is labelled by known calendar causes (public holidays SH via the `holidays` package, Kiel Week, 24/31 Dec).

**Result:** 148 of 9,334 rows flagged.
- **60 explained** by the calendar: New Year's Eve 14, Easter Monday 9, day after Good Friday 7, Whit Monday 6, Christmas Eve 5, day before Good Friday 5, 3 Oct 3, Kiel Week 3, others 8.
- **88 unexplained**, mostly in low-volume groups:
  - Seasonal bread (6) at season start/end and on single days (e.g. 6 Dec: 2014 ratio 4.6, 2016 ratio 2.6): small numbers, high relative swings.
  - Confectionery (4) around **Valentine's Day**: mean ratio 10–16 Feb 1.67 (2014), 1.66 (2015), 2.07 (2016), but 1.09 (2017) and 1.03 (2018). The effect disappears after 2016.
  - Bread/rolls on the days between Christmas and New Year (29–30 Dec), ratio 2.0–2.6.

**2014-05-05 (Monday):** the only day on which **all five** regular groups are 2.8–4.1 × normal (rolls 1,203 vs. ~400 on the surrounding days). The branch was **closed on 1 May (Thu) and on 3 and 4 May (Sat/Sun)**. On the first open day after any other closure, groups 1–5 average 0.9–1.9 × normal (30 cases, median ≈ 1.35); 2014-05-05 reaches 3.41 × normal. Most likely explanation: the turnover of the closed weekend was booked on Monday, or a one-off event. Either way it does not represent a normal day. **Excluded from training (decision D2).**

**Side finding:** the first open day after a closure is regularly higher than normal (median ≈ 1.35 ×), which is a candidate feature (known in advance).

## Holiday calendar consistency (public holidays, `holidays` 0.109, Germany/SH)

- 46 public holidays fall into the sales period. The branch was **closed** on 25/26 Dec, 1 Jan, Good Friday and (except 2016) 1 May, and **open** on Easter Monday, Ascension Day, Whit Monday and 3 Oct (20 open public holidays). So "public holiday" ≠ "closed day".
- 2017-10-31 (Reformation Day, a one-off holiday in 2017) is in the package and was a closed day: consistent.
- **12 closed days are not public holidays** (unplanned closures): 2013-12-28, 2014-05-03, 2014-05-04, 2014-08-17, 2016-03-24, 2016-07-07, 2016-07-18, 2016-08-14, 2016-08-15, 2016-12-17, 2017-07-04, 2017-10-23.
- School holidays: not checked yet (CSV still to be built).
