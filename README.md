# NxtGen Demand

**Customer demand, made clear.** A working browser application that helps small retail teams compare sales channels and plan the next two weeks of demand.

Team: **NxtGen**  
Track: **Customers, Channels & Demand**  
License: **MIT**

## The problem

Small retailers who sell through direct orders, marketplaces, social channels, and shops often work with separate sales exports. Without a shared view, they struggle to see which products drive demand, compare recorded channel spending, and estimate how much stock they may need next. NxtGen combines these tasks in one dashboard using a simple aggregate CSV. This problem statement is a design hypothesis, not a claim from customer research.

## What works

- Overview with revenue, orders, units sold, and supplied new-customer counts, compared with the previous period.
- Date-window, channel, and product filters, daily demand chart, channel revenue mix, and product ranking.
- Channel table with revenue / spend and cost per supplied new-customer count, including zero-denominator handling.
- A 14-day demand baseline based on recent weekday patterns, with an editable stock scenario and visible assumptions.
- Validated CSV import, downloadable sample data, reset, and an exported text action plan.
- Responsive layout and labeled form controls. No account, API key, database, or paid service is needed.

The included dataset has **672 synthetic rows over 56 days**, four channels, and three products. Every demo result is illustrative. No real customer data or measured business impact is claimed.

## Run locally

Install Node.js 20 or later, then run from the repository root:

```sh
node tools/serve.mjs
```

Open **http://127.0.0.1:4173**. Keep the terminal running. Press Ctrl+C to stop. There are no dependencies to install. Opening `index.html` directly with `file://` will not load the JavaScript modules.

Alternative:

```sh
cd app
npm start
```

To change ports, set the `PORT` environment variable before starting. See [deployment instructions](docs/DEPLOYMENT.md) for static hosting and GitHub Pages.

## Three-minute judge run guide

1. Start the app. The synthetic dataset loads automatically.
2. In **Overview**, inspect the four totals and revenue mix. Change the period to 14 days, then filter to **Direct**. All displayed totals and charts update.
3. Open **Channel insights**. Compare revenue / spend and cost / new customer. These ratios do not measure profit or causal marketing attribution.
4. Open **Demand planner**. Set units available to **1000** to see a projected shortage, then **10000** to compare a higher-stock scenario. This is an aggregate illustration, not a purchase recommendation.
5. Open **Your data**, download the sample CSV, and import it again. A success message confirms the row count. An invalid file produces an error and preserves the prior dataset.
6. Choose **Export action plan**. The text file includes the active selection, totals, channel comparison, forecast, and limitations.

## CSV format

Use exactly these eight columns in any order:

```csv
date,channel,product,orders,units,revenue,spend,new_customers
2026-10-01,Direct,Everyday tee,10,13,5850,410,3
```

- `date`: valid `YYYY-MM-DD` date.
- `channel`, `product`: nonempty labels, 1 to 80 characters each.
- `orders`, `units`, `new_customers`: nonnegative whole numbers. Units must be at least orders. New customers must not exceed orders.
- `revenue`, `spend`: nonnegative numbers in **INR**. This version does not convert currencies.
- Maximum 5 MB and 50,000 rows. Include zero-sale records when the absence of a record should not mean missing data.
- Rows add together. Export each transaction aggregate once to avoid double counting. Quoted commas and escaped quotes are supported.
- Do not include personal information. Import is held in memory only and disappears on refresh. The app does not upload the file, use analytics, or persist data to local storage.

## Forecast and metric definitions

The data's latest date anchors all periods. The prior period has the same number of calendar days and does not overlap. Missing dates count as zero, so absent source data can distort comparisons.

The forecast requires at least 14 distinct observed dates in the latest 28 days for the selected channel/product. It repeats the most recent seven daily unit totals. Growth from the previous week is capped to -25% to +25%, then applied proportionally over the next 14 days. The shaded +/-20% range is a planning scenario, **not a statistical confidence interval**. There is no trained machine learning model or external AI API.

Revenue / spend = recorded revenue divided by recorded channel spend. Cost / new customer = spend divided by the supplied count. A zero denominator displays N/A. New-customer totals are sums of supplied counts and can overlap across channels. No individual customer tracking or deduplication occurs.

## Tests

```sh
node --test tests/engine.test.mjs
```

Tests cover CSV round trips, quoted data, invalid inputs, calendar windows, aggregation, missing dates, forecast arithmetic, growth caps, insufficient history, and zero denominators.

## Repository map

```text
app/dist/             Static app: HTML, CSS, ES modules, sample CSV
app/.openai/          Sites hosting identity and static directory
docs/                 Deployment, problem statement, and demo guide
submission/           Pitch PDF, walkthrough video, copy-ready form text
tests/                Node built-in test suite
tools/                Local HTTP server and artifact generation sources
.github/workflows/    Automated tests and manually triggered Pages deployment
```

## Submission materials

- [Problem statement](docs/PROBLEM_STATEMENT.md)
- [Pitch deck](submission/NxtGen-Pitch.pdf)
- [Demo walkthrough](submission/NxtGen-Demo.mp4)
- [Demo script](docs/DEMO_SCRIPT.md)
- [Deployment instructions](docs/DEPLOYMENT.md)
- [Copy-ready submission text and checklist](submission/SUBMISSION.md)

## Current scope

NxtGen is a working prototype. It does not connect to commerce platforms, model margins or returns, optimize budgets, issue purchase orders, or provide SKU-specific stock recommendations. Forecast accuracy has not been measured on real business data. Before a production pilot, validate the data contract with retailers, backtest against a seasonal-naive baseline, and add inventory/lead-time data. The public demo should contain synthetic data only.
