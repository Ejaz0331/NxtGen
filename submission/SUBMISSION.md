# NxtGen submission pack

## Copy into the form

**Team name:** NxtGen

**Track:** Track B2 - Customers, Channels & Demand

**Project title:** NxtGen Demand

**Public GitHub repository:** https://github.com/Ejaz0331/NxtGen

**One-line description:** A customer demand dashboard that turns aggregate sales exports into channel comparisons, a transparent two-week stock scenario, and a downloadable action plan.

**Problem statement:** Small retail teams selling through direct orders, marketplaces, social channels, and shops often review separate sales exports. This makes it harder to compare channel performance and assess whether available stock could cover near-term demand. NxtGen provides a shared view of aggregate sales with a transparent demand baseline. This is a design hypothesis; customer research and measured business outcomes are future work.

**Solution:** Import a daily sales CSV or explore the synthetic example. Filter by period, channel, and product. Review revenue, orders, demand trends, channel spending ratios, and product rankings. Use the demand planner to compare available stock with a 14-day baseline, then export an action plan with the assumptions attached. Imported data stays in the browser session.

**Track fit:** NxtGen addresses fragmented sales visibility across channels and helps teams review potential shortages before the next planning period. It focuses on aggregate demand and channel comparison within Track B2. Customer identity resolution and support-ticket analysis are outside the current scope.

**Technical implementation:** Static HTML, CSS, and JavaScript ES modules. A dependency-free Node.js server supports local use. Forecasting repeats the latest seven daily totals with a capped trend adjustment. It is a transparent baseline, not a trained AI model. The app needs no API keys or database. Nine automated tests cover core data logic.

**What is demonstrated:** 672 synthetic sales rows over 56 days, covering four sales channels and three products. The default 28-day selection produces INR 7,975,680 in revenue, 7,413 orders, and 9,481 units sold. The example 14-day projection is 5,132 units. These results illustrate functionality and do not represent real business traction or verified forecast accuracy.

**Impact and next steps:** The intended benefit is a faster, more consistent weekly review of channel sales and stock scenarios. Validate that benefit through retailer interviews and task comparisons. Backtest forecast error against a seasonal-naive baseline before using it for inventory decisions. Add product-level inventory and supplier lead times for a future pilot.

## Uploads and links

| Requirement | File or link |
| --- | --- |
| Problem statement | `docs/PROBLEM_STATEMENT.md` |
| Public code | https://github.com/Ejaz0331/NxtGen |
| Pitch PDF | `submission/NxtGen-Pitch.pdf` |
| Pitch browser link | https://github.com/Ejaz0331/NxtGen/blob/main/submission/NxtGen-Pitch.pdf |
| Demo video | `submission/NxtGen-Demo.mp4` |
| Demo download link | https://github.com/Ejaz0331/NxtGen/raw/refs/heads/main/submission/NxtGen-Demo.mp4 |
| Demo duration | 2 minutes 17 seconds (approximately) |
| Captions | `submission/NxtGen-Demo.srt`, also embedded in the MP4 |
| README / setup / usage | `README.md` |
| Deployment and run guide | `docs/DEPLOYMENT.md` |
| Open-source license | `LICENSE` (MIT) |

The video is a narrated product walkthrough using real computed outputs from the synthetic dataset. It is not a browser screen recording. If the competition requires a live UI recording specifically, record the README judge flow before submission.

## Hosted owner preview

https://nxtgen-demand-ejaz.lovelydell257.chatgpt.site

Deployment succeeded. This Site currently has owner-only access and is not a public judge link. Judges can run the public source locally. GitHub Pages deployment instructions are included if a public live demo is required.

## Final checks before handing in

- Confirm team members, contact details, competition eligibility, deadline, and any declarations in the actual portal. Those fields were not supplied.
- Manually run the browser smoke check in `docs/DEPLOYMENT.md`. Automated data tests and HTTP delivery passed, but saved browser permissions prevented visual and interaction verification during preparation.
- Play the full narrated demo and decide whether the competition accepts this walkthrough format.
- Use the public repository and file links, rather than the private owner preview, for judge access.
- Upload the PDF and MP4 when the portal asks for files. Verify that every submitted link opens while signed out.
- Submit the final form yourself after reviewing its declarations. The portal has not been submitted by this task.
