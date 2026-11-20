# Decisions

Newest first. One entry per decision taken at a stop point.

## 2026-11-20: Main model uses no sales history; observed weather stands in for the forecast
**Canvas block:** 6
**Decision:** Main model features: calendar, holidays, Kiel Week, weather of the forecast day (observed, as stand-in for the forecast). Sales-history features only in a separate experiment on the validation year. New data sources allowed if known the evening before.
**Reason:** The Kaggle test year hides its sales, so history features could not be computed there; one model gives one consistent evaluation. Only observed weather is available.
**Alternatives considered:** Main model with sales history plus a separate Kaggle model (two models, two evaluations); no weather at all (loses a likely effect).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Time-based validation split, test set used once
**Canvas block:** 4
**Decision:** Train 2013-07-01 – 2017-07-31, validate 2017-08-01 – 2018-07-31. Kaggle test year: submit only to check the format and once at the end.
**Reason:** A full validation year covers every season, one Kiel Week and one Christmas and mirrors the test year; repeated test looks would make the test score optimistic.
**Alternatives considered:** Last 6 months as validation (misses half the seasons); random split (leaks the future).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Over-forecasting is the costlier error
**Canvas block:** 4
**Decision:** Waste (forecast too high) is worse than forecasting too low. MAPE stays the main metric; error direction is reported; an asymmetric loss is compared with the symmetric one as an experiment.
**Reason:** Unsold bread and rolls are lost; the course still scores with MAPE.
**Alternatives considered:** Treat both errors the same only (ignores the cost difference); switch the main metric to an asymmetric one (cost ratio not known yet; breaks comparison with the course).
**Decided by:** Team 15 (grill-question session). Cost ratio still open.

## 2026-11-20: Metrics, baselines and the bar for "good enough"
**Canvas block:** 4
**Decision:** MAPE per product group; 80 % range with coverage check. Model must beat the "same weekday last week" rule in each of groups 1–5; group 6 reported only; no fixed margin. Also compare to the course linear regression.
**Reason:** MAPE is required by the course; the weekday rule is the assumed current practice; group 6 has too few seasons for a firm verdict.
**Alternatives considered:** A fixed improvement margin; one overall MAPE only (hides weak groups).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Two audiences
**Canvas block:** 3
**Decision:** Operations manager gets a one-page summary (daily table + effects with limits); technical readers get repo notebooks/README and the course presentation.
**Reason:** The manager needs an actionable table; the course needs reproducible work and MAPE per group.
**Alternatives considered:** One combined report for both (too technical for the manager, too thin for the course).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Seasonal bread is forecast like the other groups
**Canvas block:** 2
**Decision:** Group 6 gets the same forecasting approach as groups 1–5; low confidence (about 5 seasons) is stated.
**Reason:** It is part of the course test set; whether a simpler rule beats it is a question for the experiments.
**Alternatives considered:** A separate seasonal-average rule (may be tested later as an experiment); leaving group 6 out.
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Add a public and school holiday calendar
**Canvas block:** 2 (affects 5, 7)
**Decision:** We add Schleswig-Holstein public and school holidays as an extra data source.
**Reason:** Holidays are known years in advance (no leakage) and are needed to answer Q2d; the given files do not mark them.
**Alternatives considered:** Infer holidays from days without sales (misses the days around holidays and all school holidays).
**Decided by:** Team 15 (grill-question session). Source still open.

## 2026-11-20: Four effects are analysed explicitly
**Canvas block:** 2
**Decision:** Besides the forecast we answer: weekday & season, weather, Kiel Week, days around public holidays, each with its limit.
**Reason:** All four plausibly change how much the manager bakes.
**Alternatives considered:** Only the forecast without explained effects; a subset of the effects.
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Forecast is a number plus a range
**Canvas block:** 2
**Decision:** For each product group we deliver a point forecast and a range (prediction interval).
**Reason:** The range helps the manager choose how much buffer to bake.
**Alternatives considered:** Point forecast only (enough for the course metric, less useful for the decision).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Current practice assumed to be "same weekday last week"
**Canvas block:** 1
**Decision:** We assume the manager today bakes about what sold on the same weekday last week.
**Reason:** The client gave no information about current practice; this rule is simple, realistic and computable, so it can serve as the baseline to beat.
**Alternatives considered:** Ask the client (not possible in the course setting); assume no planning rule (gives no baseline).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Forecast only opening days
**Canvas block:** 1
**Decision:** Forecasts are made only for days the branch is open; seasonal bread only October–January.
**Reason:** Closing days (public holidays) are known in advance, so the manager needs no forecast for them.
**Alternatives considered:** Forecast every calendar day with 0 for closed days (adds trivial predictions and distorts the error metric).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: We forecast sales, not demand
**Canvas block:** 2
**Decision:** The target is recorded turnover. That sales are capped on sold-out days is stated as a limit, not corrected.
**Reason:** The data has no information on sell-outs or leftovers, so no correction is possible.
**Alternatives considered:** Estimate and correct for censored demand (no data to do it).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Forecast unit is turnover per product group
**Canvas block:** 1
**Decision:** The model forecasts turnover (`Umsatz`) per product group; the manager converts it into pieces.
**Reason:** The data contains only turnover, no prices or piece counts; the course evaluation also uses turnover.
**Alternatives considered:** Collect prices and forecast pieces (no source for prices).
**Decided by:** Team 15 (grill-question session)

## 2026-11-20: Decision is made in the evening after closing
**Canvas block:** 1
**Decision:** The manager fixes tomorrow's baking amounts after closing, when today's sales are complete.
**Reason:** Team's choice of the decision setting; it means today's turnover can be used for tomorrow's forecast.
**Alternatives considered:** Early afternoon the day before (today's sales incomplete; only data up to yesterday usable).
**Decided by:** Team 15 (grill-question session)

<!--
## YYYY-MM-DD: <short title>
**Canvas block:** <number>
**Decision:** <what was decided>
**Reason:** <why>
**Alternatives considered:** <what else, and why not>
**Decided by:** <names>
-->
