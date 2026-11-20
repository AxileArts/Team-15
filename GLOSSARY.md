# Glossary

One entry per term, variable or code the project uses. Keep the canonical name, the meaning, the unit and anything that is easy to get wrong.

| Term | Meaning | Unit / values | Notes |
|---|---|---|---|
| `Umsatz` (turnover) | Sales revenue of one product group in the branch on one day. Target variable. | Money, currency not stated (≈ 7 to 1,880 per day) | Revenue, **not** pieces baked or pieces sold. Recorded only on days with sales. |
| `Warengruppe` (product group) | Product category code | 1 Bread · 2 Rolls · 3 Croissants · 4 Confectionery · 5 Cakes · 6 Seasonal bread | Group 4 has no rows on 53 days; group 6 is only sold October–January (292 days). |
| `Datum` (date) | Calendar day of the sale | 2013-07-01 to 2018-07-31 in the training data | 38 days have no sales at all (mostly public holidays). |
| Kiel Week (`KielerWoche`) | Kiel's annual sailing festival | 1 on festival days, 0 otherwise | 9 days per year; the file only lists festival days, so set the others to 0 after merging. |
| Forecast day | The next opening day after the decision; the day the forecast is for | Date | Decision is made the evening before, after closing; closed days get no forecast. |
| Same-weekday-last-week rule | Assumed current practice: tomorrow's turnover = turnover of the same weekday 7 days earlier | Turnover | Used as the baseline to beat. |
| Sales vs. demand | Sales = what was actually sold (recorded). Demand = what customers would have bought. | – | Sales ≤ demand on sold-out days; the data only has sales. |
| Range (prediction interval) | Interval around the point forecast in which turnover usually falls | Turnover, e.g. 130–190 | Coverage level (e.g. 80 %) still to be set in block 4. |
| MAPE | Mean absolute percentage error: average of abs(actual − forecast) / actual | % (lower is better) | Main metric, per product group. Undefined when actual = 0 (closed days are not forecast). |
| Coverage | Share of actual days whose turnover falls inside the 80 % range | % (target ≈ 80 %) | Too high = range too wide to help; too low = range promises too much. |
| Validation year | 2017-08-01 – 2018-07-31; used to compare models | Dates | Training data ends 2017-07-31. |
| Test year | 2018-08-01 – 2019-07-31; Kaggle, sales hidden | Dates | Used once at the end (plus format checks). |
| Over-forecast | Forecast higher than actual turnover → waste | – | Considered the costlier error. |
