# Live deployment status

Verified on **1 October 2026**.

| Project | Public URL | Status |
| --- | --- | --- |
| Portfolio | https://vishnu-portfolio-1ijm.onrender.com | Live; page, scripts, styles, images and PDF checked |
| NoteLens | https://vishnu-notelens.onrender.com | Live; upload, three search modes, sessions and clearing checked |
| RepoCheck | https://vishnu-repocheck.onrender.com | Live; sample, JSON/ZIP scans and invalid-input rejection checked |
| CampusTrack | No public app URL yet | Database available; Blueprint deployment still required |

[Verification run](https://github.com/me-vishnurnair/portfolio/actions/runs/36832848807) · [Repeatable check script](../scripts/check_live.py) · [Check workflow](../.github/workflows/live-checks.yml)

These are point-in-time results, not continuous uptime monitoring. The earlier local checks also covered keyboard dialogs and responsive layouts.

## Complete CampusTrack

[Open its prepared deployment](https://render.com/deploy?repo=https://github.com/me-vishnurnair/campustrack), select **My Workspace**, review the one free web service, and click **Deploy Blueprint**. It references the existing **vishnu-campustrack-db** database and uses Render's assigned HTTPS origin. No credential needs to be copied to GitHub or chat.

The connector cannot create a Blueprint or retrieve PostgreSQL connection credentials. That dashboard action is the remaining deployment requirement. See the [CampusTrack deployment guide](https://github.com/me-vishnurnair/campustrack/blob/main/docs/DEPLOYMENT.md). Verify the resulting app before adding its URL to `app.js`.

## Publishing updates

The three current services were created from public repository URLs. The Render API displays an auto-deploy setting, but automatic deployments require a connected Git provider. Without that connection, a push alone does not publish an update.

1. Review changes and wait for the relevant GitHub Actions checks.
2. If GitHub is connected to the Render service, wait for its automatic deployment; do not trigger a duplicate.
3. Otherwise choose **Manual Deploy → Deploy latest commit** in Render.
4. Confirm the deployed commit and run **Live deployment checks** from the portfolio's GitHub Actions page.

For reliable future automatic updates, connect the relevant repositories through Render's GitHub integration and choose **After CI Checks Pass** for the Python apps. This requires a Render dashboard action; no repository access tokens should be committed.

The portfolio build is:

```sh
mkdir -p public && cp index.html style.css app.js favicon.svg public/ && cp -r assets public/
```

Publish directory: `public`. The standalone website has no build dependency installation.

## Free hosting and long-term operation

- The portfolio uses static hosting and has no scheduled database-style expiry.
- NoteLens and RepoCheck use free Python services in Singapore. They sleep after 15 idle minutes and can take about a minute to start on the next visit.
- Free services share 750 runtime hours per workspace each calendar month. This is insufficient to keep three apps continuously running all month.
- The CampusTrack free database expires on **31 October 2026 at 05:41 UTC (11:11 India time)** and has no backups. Upgrade or migrate it before expiry and export important records.
- NoteLens notes are intentionally temporary and disappear on restart or after workspace expiry. RepoCheck does not intentionally save uploaded source.

An entry-level always-on budget for the three Python apps is **US$27.30/month before tax and additional usage**: three `0.5c-512mb` services at $7 each, one `0.1c-256mb` PostgreSQL instance at $6, and 1 GB database storage at $0.30. This is an estimate from current published rates, not a fixed quote or a guarantee of uptime. The static portfolio remains on the free option. No paid upgrade has been authorized or applied.

Provider references: [free-plan limits](https://render.com/docs/free), [deploy behavior](https://render.com/docs/deploys), [pricing](https://render.com/pricing). Check the dashboard's final price and billing settings before approving any upgrade.

## Recovery

A failed build should leave the previous successful release serving traffic. Check Render's deployment logs and GitHub Actions, fix the identified failure and redeploy. Use Render's rollback controls for a regression after a successful deployment.

For a database failure, check PostgreSQL status and connection settings without printing credentials. Keep CampusTrack's secure production checks enabled. Before a schema change, establish and verify backups and use reviewed migrations; the current `create_all` initialization is not a migration system.
