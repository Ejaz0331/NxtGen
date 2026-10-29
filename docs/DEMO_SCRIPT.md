# Demo walkthrough script

This narrated walkthrough uses deterministic sample outputs. It is not a browser screen recording.

## Scene 1

Meet NxtGen Demand, a working customer demand dashboard for small retail teams. It brings sales channels into a shared view and helps a team plan the next two weeks. This walkthrough uses synthetic data and computed application outputs.

## Scene 2

A retailer selling through several channels needs to know which products are moving, how revenue compares with channel spending, and whether stock could cover upcoming demand. NxtGen starts from a simple aggregate sales export. The problem is a design hypothesis that still needs customer validation.

## Scene 3

The Overview offers period, channel, and product filters. For the sample period from September twenty ninth to October twenty sixth, the engine calculates 7413 orders and 9481 units sold. The revenue total shown here is in Indian rupees. The same selection drives product rankings and the demand chart.

## Scene 4

Channel insights compares recorded revenue and spending. In this example, Direct has the highest revenue per rupee of recorded spend. The comparison can guide a margin and capacity review, but does not establish profit or marketing attribution. New customer counts can overlap between channels.

## Scene 5

The demand planner projects 5132 units over the next fourteen days. It repeats the latest weekly pattern with a capped trend adjustment. Entering one thousand units available shows a baseline shortage. Ten thousand units shows a surplus. The planning range is illustrative and is not a statistical confidence interval.

## Scene 6

The app runs with Node and a browser, with no API keys or dependency installation. CSV validation checks dates and numeric counts. Imported data stays in memory and resets on refresh. Nine automated tests pass. This video presents computed results rather than a recorded browser session.

## Scene 7

The handoff includes source code, a sample CSV, an action plan export, setup and deployment instructions, a pitch PDF, and an MIT license. Next, we would test with retailers and backtest the forecast before an inventory pilot. NxtGen makes the assumptions visible so teams can review the next decision.
