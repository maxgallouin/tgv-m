# TGV M — lignes et horaires

A French Jekyll site with a line directory, dedicated directional timetable pages, date filters, and a JSON endpoint. All departure tables are rendered by Jekyll and remain readable without JavaScript.

## Deploy

1. Put this folder's contents at the root of your GitHub repository, including `.github/workflows/pages.yml`.
2. In repository Settings → Pages, select **GitHub Actions** as the build source.
3. Run the “Deploy Jekyll to GitHub Pages” workflow manually from Actions when publication is intended. Pushing to `main` does not deploy the site.

Repository: https://github.com/maxgallouin/tgv-m (private). A private repository does not by itself make a deployed Pages website private. Publication and the custom domain remain to be configured separately.

The site uses `relative_url` for links and assets and works at a project subpath as well as a domain root. No API keys or server are required.

## Run locally

```sh
bundle install
bundle exec jekyll serve
```

## Refresh the data

The single source of truth is `_data/journeys.json`. Jekyll renders the page and `/api/journeys.json` from this file.

After the existing Monday Codex workflow finishes all eight searches, import its complete export:

```sh
python3 scripts/update-data.py /absolute/path/to/outputs/journeys.json
```

Commit and push `_data/journeys.json` to save refreshed data, then run the deployment workflow manually if publication is intended. The browser-based extraction runs in Codex, not GitHub Actions; automatic commits and pushes from that extraction have not been configured. The page displays the observation date rather than implying live equipment availability.

The saved data covers 9–15 November 2026 in both directions: 194 inspected journeys, 14 matches. This is an accessibility indicator from SNCF Connect route details, not independently confirmed TGV-M rolling stock.

Deployment workflow follows GitHub's official Jekyll Pages actions: https://github.com/actions/jekyll-build-pages.
