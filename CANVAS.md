# Agentic Data Science Canvas

**Project:** Team 15: Bakery Sales Prediction
**Team:** Julian, Niklas, Jasper
**Version:** 2026-11-17

> Owners: 👤 human decides · 🤖 agent drafts, human approves.
> Keep each block short. Details go in linked files; decisions go in `DECISIONS.md`.

---

## Problem

### 1. Decision 👤
<!-- Who decides what, when and how often? What happens today without this analysis? -->
- **Who / what:** The bakery's operations manager decides how much of each product group (1–6) to bake for the next day.
- **When / how often:** Every evening after closing, for the next opening day only (horizon: 1 day). Today's sales are complete at that moment.
- **Output we deliver:** Forecast **turnover** per product group. Converting turnover into pieces stays with the manager (we have no prices).
- **Which days:** Only days the branch is open; closed days (public holidays) are known in advance and get no forecast. Seasonal bread only October–January.
- **Today, without the analysis (assumption):** The manager bakes about what sold on the same weekday last week, adjusted by gut feeling.

### 2. Questions 👤
<!-- The analysis questions that would change the decision. For each: what the data can answer, and what it cannot. -->
- **Main question:** What turnover will each product group (1–6) have on the next opening day? Answer = one number **plus a range** per group (e.g. "most likely 160, usually 130–190").
- **Q2a Weekday & season:** How do weekday and time of year shift turnover per group? Well covered (5 years of daily data).
- **Q2b Weather:** How much do temperature, rain and clouds shift turnover? *Limit:* we only have observed weather, but the manager only knows tomorrow's forecast, so our effect is an upper bound.
- **Q2c Kiel Week:** How much does Kiel Week shift turnover? *Limit:* only 5 Kiel Weeks (2014–2018) = 5 independent cases; rough estimate.
- **Q2d Days around public holidays** (e.g. Christmas Eve, day before Good Friday): *Limit:* about 5 cases per holiday; needs an added holiday calendar.
- **Seasonal bread (group 6):** Forecast like the other groups, with low confidence stated (about 5 seasons, Oct 2013 – Dec 2017).
- **Cannot answer (settled):** The data records *sales*, not *demand*. On days a product sold out, true demand was higher, and there is no data on sell-outs or leftovers. We forecast sales and name this as a limit.

### 3. Audiences 👤
<!-- Who receives which result, in which form? At least: the decision-maker and the technical reader. -->
- **Operations manager (decision-maker):** one-page summary with a daily table per product group (forecast + range) and the four effects (Q2a–d) in plain words, each with its limit.
- **Technical readers (course instructor, other teams):** notebooks + README in the repo; the 8–10 min course presentation with MAPE per product group.

### 4. Success 👤
<!-- Metric(s), the baseline to beat, what is good enough to act on. Which errors are worse than others? -->
- **Main metric:** MAPE per product group (course requirement), on the validation year.
- **Range:** 80 % prediction interval; coverage (share of actual days inside the range) should be close to 80 %.
- **Baselines:** (1) "same weekday last week" rule. Validation-year MAPE: Bread 26.6 %, Rolls 13.5 %, Croissants 21.0 %, Confectionery 26.3 %, Cakes 19.8 %, Seasonal bread 43.1 %, overall 22.0 % (1,799 of 1,841 rows; 42 have no value a week earlier). (2) Course linear regression (to be built).
- **Good enough to act:** beat the weekday rule in **each of groups 1–5**; group 6 is reported only (≈ 5 seasons, too few for pass/fail). No fixed margin.
- **Costly errors:** forecasting too high (→ waste) is worse than too low. Report the direction of errors (over/under) besides MAPE. Experiment: an asymmetric loss that penalises over-forecasts vs. the symmetric one.
- **Segments reported separately:** product group, weekday, Kiel Week, days around public holidays, December.
- **Split:** by time. Train 2013-07-01 – 2017-07-31, validate 2017-08-01 – 2018-07-31. Test = Kaggle year 2018-08-01 – 2019-07-31: submit only to check the file format and once at the end with the model chosen on validation.

---

## Data and method

### 5. Data 🤖
<!-- Sources, unit of observation, period covered, keys, known gaps. Link the data fact sheet. -->
Details: [`docs/data-fact-sheet.md`](docs/data-fact-sheet.md).
- **Sales:** 9,334 rows, one per product group and open day, 2013-07-01 – 2018-07-31; key `Datum` + `Warengruppe` (unique). No missing values. 38 closed days; confectionery is absent on 53 open days (2013–2016); seasonal bread only in 5 seasons. Extremes: 31 Dec cakes (5×), 2014-05-05.
- **Weather:** one row per day, 2012-01-01 – 2019-08-01. 3 days missing in the sales period, 13 in the test year. `Bewoelkung` missing 10 days (Oct/Nov 2017); `Wettercode` missing 26 %, not at random and less often in later years.
- **Kiel Week:** 9 days per year, 2012–2019; 4 festivals in training, 1 in validation.
- **Joins** on `Datum` keep the row count; 99.8 % of sales rows get weather.
- **Planned addition:** Schleswig-Holstein public and school holidays (source open).

### 6. Known in advance 👤
<!-- What information is available at the moment the result is needed? Everything else is leakage. -->
- **Moment:** evening after closing, forecast for the next opening day.
- **Allowed in the main model:** calendar (date, weekday, month, season), public and school holidays, Kiel Week dates, weather of the forecast day.
- **Weather:** observed weather of the forecast day stands in for the weather forecast the manager would have. *Limit:* effects and accuracy look somewhat better than in real use.
- **Not in the main model:** sales history (today, last week, rolling means). Real daily use would have it, but the Kaggle test year hides its sales. May be tested as a separate experiment, evaluated only on the validation year, with `shift` before any rolling.
- **Never:** same-day or future sales of any product group; aggregates that include the forecast day.
- **Additional data:** allowed if it would be known the evening before the forecast day (e.g. calendars, event dates); check each new source against this block.

### 7. Data decisions 👤
<!-- Joins, missing values, encodings, exclusions, each with a reason. Link the entries in DECISIONS.md. -->
All 2026-11-20, see `DECISIONS.md`.
- **D1 Special days:** flags for New Year's Eve (31 Dec) and Christmas Eve (24 Dec).
- **D2 Exclusion:** 2014-05-05 removed from training (all groups 2.8–4.1 × normal, after a 3-day closure; see the outlier analysis in the fact sheet).
- **D3 Missing confectionery rows:** not filled; no row = no target.
- **D4 Missing weather** (days and cloud cover): filled with the month's average from the training period only.
- **D5 `Wettercode`:** reduced to a precipitation flag (codes 50–99 = 1; other or missing = 0).
- **D6 Encodings:** weekday (Mon–Sun), month and product group one-hot; temperature, wind, cloud cover numeric.
- **D7 Holidays:** public holidays from the `holidays` package (SH); school holidays as a CSV in the repo from the official SH dates. Both are checked for consistency.
- **Joins:** left join of weather, Kiel Week and holidays onto sales on `Datum`; Kiel Week / holiday flags missing → 0.

### 8. Checks 🤖
<!-- Checkpoints and the invariants that must hold at each (row counts, keys, date ranges, IDs, baseline). Link checks/. -->
Confirmed 2026-11-20, all 15. They are implemented in [`checks/`](checks/) (run `uv run pytest checks/`); so far only the smoke check exists.
- **Raw data:**
  - C3 `id` = `YYMMDD` × 10 + group
  - C11 no `Umsatz` = 0; group 4 has 1,766 raw rows
  - C13 every closed day is a public holiday or one of the 12 known unplanned closures; 25/26 Dec, 1 Jan, Good Friday always closed
  - C14 school-holiday CSV: no overlaps, summer holidays 5–7 weeks every year, dates in 2013–2019
- **After joins / feature building:**
  - C1 one row per `Datum` + `Warengruppe`
  - C2 row count unchanged by joins
  - C5 no missing feature values
  - C6 Kiel Week = 1 on exactly 9 consecutive days per year
  - C7 plausible ranges (`Umsatz` > 0, cloud 0–8, temperature −20 to 40 °C, group 1–6)
  - C12 New Year's Eve / Christmas Eve flags only on 31 Dec / 24 Dec
  - C15 precipitation flag ∈ {0, 1}, missing `Wettercode` → 0
- **Split:**
  - C4 train ≤ 2017-07-31 < validation, no overlap
  - C8 weather fill values computed from training dates only
  - C10 2014-05-05 not in training
- **Baseline:** C9 "same weekday last week" = 22.0 % overall MAPE on the validation year.

---

## Evidence and action

### 9. Experiments 🤖
<!-- Experiment cards and their status; best result so far vs. baseline. Link experiments/LOG.md. -->

### 10. Findings 🤖
<!-- What we learned, how sure we are, and what the data cannot tell. -->

### 11. Recommendation 👤
<!-- What the decision-maker should do, under which conditions. Signed off by the team. -->

---

## Open questions
<!-- Parking lot. Each item names who resolves it. -->
- School holiday CSV for Schleswig-Holstein 2013–2019: build it from the official dates, record the link, then run its consistency check. Resolves: team, during data preparation.
- Use the side findings as features? First open day after a closure (≈ 1.35 × normal), Valentine's effect on confectionery (only until 2016), 29–30 Dec. Resolves: team, during feature engineering.
- How much worse is over-forecasting (waste) than under-forecasting (e.g. 2×)? Needed before the asymmetric-loss experiment. Resolves: team, before that experiment.
- Which further data sources (if any) to add? Each must pass block 6. Resolves: team, during data preparation.

## Decision log
See `DECISIONS.md`.
