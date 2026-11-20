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

### 8. Checks 🤖
<!-- Checkpoints and the invariants that must hold at each (row counts, keys, date ranges, IDs, baseline). Link checks/. -->

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
- Which source for the Schleswig-Holstein public and school holiday calendar (link, period 2013–2019)? Once chosen, list it in `AGENTS.md` → Additional data sources. Resolves: team, during data preparation.
- How much worse is over-forecasting (waste) than under-forecasting (e.g. 2×)? Needed before the asymmetric-loss experiment. Resolves: team, before that experiment.
- Which further data sources (if any) to add? Each must pass block 6. Resolves: team, during data preparation.

## Decision log
See `DECISIONS.md`.
