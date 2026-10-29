# Problem statement

## Who has the problem?

Small retail operators and channel managers who sell the same products through direct sales, marketplaces, social channels, and physical shops.

## What is difficult?

Their channel exports can show different parts of the business. Reviewing separate files makes it harder to answer which products sell most, how recorded revenue compares with channel spending, and whether available stock could cover near-term demand.

## Why does it matter?

Poor visibility can contribute to avoidable stockouts, excess inventory, or spending decisions made without a comparable baseline. These are plausible risks that motivate this prototype. We have not measured their frequency or cost for customers.

## Proposed response

NxtGen accepts one aggregate sales CSV and provides a shared demand overview, channel comparison, a transparent 14-day projection, and an exported action plan. It makes the assumptions visible and keeps imported data inside the browser session.

## Track fit

**Customers:** supplied new-customer counts and acquisition-cost ratios.  
**Channels:** revenue mix and recorded revenue/spend comparisons.  
**Demand:** product momentum, daily sales, and a stock scenario using recent demand.

## Validation plan

Interview small retailers about their existing weekly planning process. Ask participants to complete the same channel comparison and stock review with their existing tools and with NxtGen. Measure task completion time and decision errors without promising improvements in advance. Backtest the demand baseline on held-out daily sales, report mean absolute error and WAPE where defined, and compare with a seasonal-naive baseline. Investigate errors around promotions and stockouts before piloting inventory decisions.
