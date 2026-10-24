# A3 working notes (Muhammad Bilal Tahir, 24i-3166, SE-B)

Account: signed in by user (FREE plan). Browser: Chrome (Linux, GNOME/Wayland).
Critical form (proposed): Portfolio Backtester.

## Handling rules agreed
- Sign Up / Sign In (forms 1,2): user types passwords themselves; I log responses they report.
- Contact (form 8): Cloudflare Turnstile + real message -> user does submits.
- Roll-number note: user says instructor allowed a digital note; injected as page overlay (window.__note(), re-inject after navigation).
- JS harness __go2/__bg2 (waits for run completion, reads Quasar toasts .q-notification__message + native validationMessage) = reliable. Older __run/__run1 lagged ~1 probe -> DISCARD their results.
- Don't fire runs back-to-back (server hangs "Parsing results"); one at a time, wait for completion.

## Field inventory (DOM) - see forms
- Backtester (/): Start/End Date, Starting Value, Rolling Window, Annual cashflow growth, Cashflow, Cashflow freq/offset/type, Rebalance, Offset, Drag, Ticker(s), Allocation %(s)
- Monte Carlo: Start/End, Number of years, Number of simulations, Starting Value, Min block, Max block, Block sampling, Random seed, Rebalance, Drag, tickers + %
- Safe Withdrawal Rate: Start/End, Min real years, Retirement horizon, Phase1 length, Phase1 withdrawal %, Phase2 length, Phase2 withdrawal %, Rebalance, Drag, tickers + %
- Backtest Optimizer: Tickers, Start/End, Starting Value, Rolling Window, Max holdings, Min weight, Min CAGR/Sharpe/Sortino/UPI/Calmar, Max vol/MaxDD/LongDD/AvgDD/Ulcer
- Efficient Frontier: Tickers, Start/End, Max holdings, Min weight to include
- Contact: Name(max120), Email(max254), Topic select, Subject(max120), Message(max5000), Turnstile
- Lump Sum vs DCA: Start/End, Starting Value, DCA cadence, DCA horizon (months), Money on side, Drag, tickers + %
- Time Value of Money: Starting Value, Monthly contribution, freq/timing selects, X/Y/Color variable selects
- Rebalancing Sensitivity: Start/End, frequencies, Drag, tickers + %

## BACKTESTER VERIFIED findings (harness v2 + screenshots)
Starting Value: <1 (0, 0.99, -5) -> native "Value must be greater than or equal to 1."; 1 accepted; 1,000,000,000,000 accepted; 1,000,000,000,001 -> toast "Starting value is too high"; empty -> toast "Invalid starting value"; 1e15 -> "Starting value is too high".
Rolling Window: 0/-1 -> native >=1; 1.5 -> native "Please enter a valid value. nearest 1 and 2"; 11999 accepted; 12000, 12001 -> toast "Rolling window is too large".
Annual cashflow growth: -100 -> native ">= -99.99"; -99.99 accepted; 100 accepted; 100.01 -> native rejected.
Allocation sum: exactly 100 required. 99.99 and 100.01 and 120 and 0 -> toast "Portfolio 1: Allocation percentages must sum to 100". 100/0 (single asset) runs. -10/110 RUNS (EV $15,590.61) = DEFECT: negative weight accepted.
Dates: End<Start and Start=End -> toast "Start date must be before end date". Start before data (2003-09-25, 1990) -> silently clamped (same result as 2003-09-26; first common date SPY+AGG = 2003-09-26). Future end (2030) -> silently clamped/accepted. 1-month, 2-month, 1-year ranges run OK.
Ticker: "' OR 1=1 --" -> "Invalid ticker ' OR 1=1 --".
Drag: 101 -> runs (16.3s), EV $0.00, CAGR -60.57%, no validation = DEFECT (>100% drag accepted). -1 accepted (EV $78,320).
CORRECTIONS: earlier note "1-month span -> No overlapping" and "Start 1900 -> No overlapping" were lag artefacts - WRONG.
Still to verify: Start 1900 / empty ticker / invalid ticker ZZZZZZ individually; Cashflow amount; Cashflow freq/offset; Rebalance options; future start (2099).

## BACKTESTER extra verified (batch 2)
Ticker: ZZZZZZ -> "Invalid ticker ZZZZZZ"; empty ticker with 60% -> "Portfolio 1: Non-zero allocation has empty ticker"; lowercase spy -> accepted (case-insens.); 50-char ticker, unicode ÄÖÜ, "S PY" -> "Invalid ticker <x>".
Dates: Start 1900-01-01 End 2020 -> RUNS (clamped, same EV $33,672.37); Start 2099-01-01 End 2100-01-01 -> "No overlapping time period found for the specified tickers and start/end dates".
Cashflow: -500 accepted (withdrawal), 1000 accepted (contrib $33,000, EV $135,115).

## MONTE CARLO VERIFIED (harness __gen: runs ~10-30s each)
Baseline (years15, sims500, SV10000, min1, max5): runs "500 simulations of 15 years" ~9.6s.
Number of years: 0 -> native ">=1" + toast "Number of years must be positive"; 1 runs; 1.5 runs (decimal accepted); 101 -> native "<=100" + toast "Number of years must be <= 100"; 100 -> slow (TIMEOUT 60s, no error); empty -> no response in 60s (silent).
Starting Value: 0 -> native ">=1" + toast "Starting value must be positive"; 1 runs.
Min block: 0.04 -> native ">=0.05"; 0.05 -> slow/timeout no error.
Max block: 20 runs; 21 -> native "<=20"; 0.04 -> native ">=0.05".
Min3/Max2 (min>max): TIMEOUT no message (to re-check visually).
Random seed: -1 -> native ">=0"; 0 runs; 1.5 -> native "valid value... 1 and 2" (integer only).

## HARNESS v3 (reliable): fresh page load per probe; harness stored in localStorage.__h; (0,eval)(localStorage.__h); window.__probe(name, [[label|#idx, value]], runBtnText, maxMs); read window.__res. Avoid invalid->valid in same page (app model keeps stale invalid value).

## SAFE WITHDRAWAL RATE VERIFIED (fresh page each, Calculate button; defaults horizon30, ph1 end10 3%, ph2 5%)
Baseline runs: toast "Withdrawal policy analysis complete".
Retirement horizon: 0 -> toast "Retirement horizon must be greater than 0 and at most 50 years"; 50 runs; 51 -> native "<=50" + same toast. (1 with ph1 end 10 -> "Phase 1 cannot end after the retirement horizon")
Phase 1 end year (#7): 0 -> "Phase 1 end year must be greater than 0 and at most 50"; =horizon(30) -> "Phase 2 must end after the previous phase"; 31 -> "Phase 1 cannot end after the retirement horizon"; valid 1..29.
Phase 1 withdrawal %: 0 runs; 100 runs; 101 -> native "<=100" + toast "Phase 1 withdrawal rate must be between 0% and 100%".
Phase 2 withdrawal %: -1 -> native ">=0" + toast "Phase 2 withdrawal rate must be between 0% and 100%".
Page also has: Mode (Historical/Simulator), Analysis (Safe-rate/Custom withdrawal policy), Policy basis (Time-based/Wealth-based/Guyton-Klinger), Projection select, Min real years select.

## BACKTEST OPTIMIZER VERIFIED (Optimize button; tickers space-separated; run ~1s)
Baseline "SPY AGG GLD": toast "Backtest optimization complete". Comma-separated "SPY,AGG,GLD" -> toast "You must specify at least two tickers" (delimiter is space).
Tickers: SPY (one) -> "You must specify at least two tickers"; empty -> same; "SPY AGG" (two) runs; "SPY ZZZZZZ" -> "Invalid ticker ZZZZZZ".
Starting Value: 0 -> native ">=1"; 1 runs. Rolling Window 0 -> native ">=1".
Max holdings: 0 -> native ">=1"; 1 runs (with 3 tickers).
Min weight to include: -1 -> native ">=0"; 100 RUNS (3 tickers - questionable, min weight 100% accepted); 101 -> native "<=100".
Dates: start 2020-01-01 end 2019-01-01 -> toast "End date must be after start date".
Max vol: 0 -> toast "Optimization failed. Try relaxing constraints." ; -1 -> native ">=0".

## EFFICIENT FRONTIER VERIFIED (Optimize button)
2 tickers "SPY AGG" runs. 3 tickers -> redirected to /pricing?reason=limit&tool=efficient_frontier&limit=max_efficient_frontier_tickers (free plan limit = 2 tickers).
Tickers: SPY (one) / empty -> "You must specify at least two tickers". Max holdings 0 -> native ">=1". Min weight -1 -> native ">=0"; 101 -> native "<=100". Dates reversed -> "End date must be after start date".

## LUMP SUM vs DCA (Analyze button) - PREMIUM GATED on free plan
Valid run (SPY60/AGG40) -> redirected to /pricing?reason=premium_tool&tool=lumpsum_dca_sensitivity. Alloc sum 99 and invalid ticker ZZZZZZ ALSO redirect (premium gate precedes server validation). Only native validation observable:
Starting Value: 99 -> native ">=100". DCA horizon (months): 0 -> native ">=1"; 121 -> native "<=120".

## REBALANCING SENSITIVITY (Analyze button) - PREMIUM GATED
Baseline, reversed dates (2020-01-01 / 2019-01-01), alloc sum 90 -> all redirected to /pricing?reason=premium_tool&tool=rebalancing_sensitivity. No visible validation on free plan. Fields: dates, frequencies multiselect (default all 8), abs/relative sweep, Drag, tickers + %.

## TIME VALUE OF MONEY (Calculate button; toasts)
Baseline SV10000 contrib1000 runs. Starting Value: 0 runs; 0.5 runs; -1 -> toast "Starting Value must be between $0 and $5,000,000."; 5,000,000 runs; 5,000,001 -> same toast; empty -> same toast.
Monthly contribution: -1 -> toast "Contribution must be between $0 and $100,000."; 0 runs; 100,000 runs; 100,001 -> same toast.
Selects: Contribution Frequency (Monthly default), Contribution timing (End of period), X/Y/Color variable. Checkboxes: Specify Years range / Ending Value range / CAGR levels (not probed).

## STILL NEEDS USER: Sign Up (testfol.io/start modal), Sign In (testfol.io/login), Contact (Turnstile + real message).

## ===== BACKTESTER FINAL VERIFIED (harness v3, fresh page per probe) - USE THESE =====
IMPORTANT CORRECTION: Starting Value upper: 999,999,999,999 RUNS; 1,000,000,000,000 -> "Starting value is too high"; 1,000,000,000,001 -> same. (earlier "1e12 accepted" was lag error)
SV: empty -> "Invalid starting value"; 0.99 -> native ">=1"; 1 RUNS (EV $6.22); 2 RUNS (EV $12.44); 999,999,999,999 RUNS (EV $6,222,004,217,219.58).
RW: 0 -> native ">=1"; 1 RUNS; 2 RUNS; 11998 RUNS; 11999 RUNS; 12000 -> "Rolling window is too large".
Growth: -100 -> native ">= -99.99"; -99.99 RUNS; -99.98 RUNS; 99.99 RUNS; 100 RUNS; 100.01 -> native "<= 100".
Alloc total: 99.99 / 100.01 -> "Portfolio 1: Allocation percentages must sum to 100". 100/0 single asset RUNS (history from 1993-01-29, SPY only). -10/110 RUNS EV $15,590.61 (DEFECT negative weight).
Dates: 2020-01-01..2021-01-01 RUNS EV $11,401.48 but result header shows "2019-12-31 - 2020-12-31" (DEFECT: one-day shift). start>end and start=end -> "Start date must be before end date". 2099..2100 -> "No overlapping time period found for the specified tickers and start/end dates". 1990-01-01..2020-01-01 RUNS, clamped to 2003-09-26 - 2019-12-31 (silent clamp). 2020-01-01..2030-01-01 RUNS, clamped end 2026-10-19. No dates (baseline) RUNS 2003-09-26 - 2026-10-19 EV $62,220.04 CAGR 8.25%.
Ticker: ZZZZZZ -> "Invalid ticker ZZZZZZ"; empty w/60% -> "Portfolio 1: Non-zero allocation has empty ticker"; "spy" RUNS; "' OR 1=1 --" -> "Invalid ticker ' OR 1=1 --"; "ÄÖÜ" -> "Invalid ticker ÄÖÜ".
Drag: -1 RUNS EV $78,320.13 (DEFECT); 100 RUNS EV $0.00 CAGR -60.17%; 101 RUNS EV $0.00 CAGR -60.57% 16.3s (DEFECT no upper validation).
Cashflow: -500 RUNS; 1000 RUNS EV $135,115.00 contrib (33,000).
STRONG EP: S1 all valid (2015-01-01..2020-01-01, SV 50000, RW 36, growth 2, cashflow 100, SPY60/AGG40, drag 0.5) RUNS EV $72,951.87 CAGR 7.69% (2014-12-31 - 2019-12-31).
 S2 SV=0+RW=0+growth=-100 -> three native messages (all 3 fields flagged). S3 valid numerics + ticker ZZZZZZ + alloc 60/30 -> only "Allocation percentages must sum to 100" shown (ticker error not shown = first-error-wins).
 S4 start>end + SV empty + ZZZZZZ + alloc 60/60 -> three toasts: alloc sum, "Invalid starting value", "Start date must be before end date" (ticker error not reported).

## MONTE CARLO FINAL (harness v3) + FREE PLAN LIMITS
Free plan: max 15 years, 500 simulations (dialog "Upgrade for higher Monte Carlo limits: Free supports up to 15 years and 500 simulations. Pro 70y/5,000; Pro+/Max 100y/13,000").
Years=1 RUNS (500 simulations of 1 years); Years=0 -> native ">=1" + toast "Number of years must be positive"; 15 (default) RUNS (9.6s); 16 -> upgrade dialog (plan limit); 100 -> upgrade dialog; 101 -> native "<=100" + toast "Number of years must be <= 100". 1.5 accepted (decimal).
Starting Value=1 RUNS; 0 -> native ">=1" + "Starting value must be positive". Min block=0.05 RUNS; 0.04 -> native ">=0.05". Max block=20 RUNS; 21 -> native "<=20"; 0.04 -> native ">=0.05". Random seed=0 RUNS; -1 -> native ">=0"; 1.5 -> native integer only.
NB harness classifies upgrade-dialog as RAN -> always check modal.

## SWR extra: Horizon=2 Ph1 end=1 RUNS; Horizon=1 Ph1 end=1 RUNS (inconsistent w/ Horizon30 Ph1end30 rejected "Phase 2 must end after the previous phase"); Ph1 end=29 RUNS.
## OPTIMIZER extra: Min weight=0 RUNS; Rolling Window=1 RUNS. EF extra: Min weight=0 RUNS; 100 RUNS (2 tickers).
