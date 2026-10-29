# Deployment and run guide

## Local run

Requirements: Node.js 20+ and a modern browser. No installation, keys, secrets, database, or build step.

```sh
git clone https://github.com/Ejaz0331/NxtGen.git
cd NxtGen
node --test tests/engine.test.mjs
node tools/serve.mjs
```

Visit http://127.0.0.1:4173. The server binds to loopback. It is for local use, not an internet-facing production service.

Windows PowerShell alternate port:

```powershell
$env:PORT = '4180'
node tools/serve.mjs
```

macOS/Linux alternate port:

```sh
PORT=4180 node tools/serve.mjs
```

## Static hosting

Publish the **contents of `app/dist`** on any static host that serves `.js` as JavaScript. Entry file: `index.html`. All asset URLs are relative, so deployment works at a subpath such as `/NxtGen/`. No server-side runtime or environment variables are required. Keep HTTPS enabled on the chosen host.

## GitHub Pages

The repository includes `.github/workflows/pages.yml`, triggered manually to avoid silently changing repository settings. In GitHub, open **Settings > Pages**, choose **GitHub Actions** as the source, then run **Actions > Deploy dashboard to GitHub Pages > Run workflow** on the main branch. The workflow tests the engine and uploads `app/dist`. Use the URL reported by the successful deployment. The expected default URL is `https://ejaz0331.github.io/NxtGen/`, but it is not live until GitHub confirms deployment.

## Sites hosting

`app/.openai/hosting.json` stores the registered Site ID and `dist` static directory. Use the Sites source workflow from `app` to package and publish exactly the pushed source commit. New Sites default to private. A private preview requires the owner's access and is unsuitable as a judge-facing link unless access is changed deliberately. Repository files and local startup remain independently usable.

## Smoke check after deployment

1. Load the page in a fresh browser and confirm the synthetic demo appears.
2. Switch all four navigation views and change filters.
3. Import `app/dist/sample.csv` and confirm 672 accepted rows.
4. Import a malformed CSV and confirm an error appears without replacing working data.
5. Set stock to a low value, then a high value, and compare the scenario message.
6. Download the action plan and inspect its selected dates and totals.
7. Test a narrow/mobile viewport and keyboard navigation.

## Troubleshooting

- Blank page when opening a file directly: use the HTTP server instead of `file://`.
- Port in use: stop the earlier server or choose another `PORT`.
- Import error: use the exact eight sample column names, valid calendar dates, and nonnegative numeric values.
- No forecast: supply at least 14 distinct observation dates within the latest 28 days for the selected filters.
- Unexpected totals: remove duplicate exports and check that the data uses INR throughout.
- Changed data disappeared: imported data intentionally stays in memory only and resets on refresh.
