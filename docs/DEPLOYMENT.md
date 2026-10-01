# Free hosting and recovery

All five deployments use free plans. The portfolio links CampusTrack's browser edition as its long-term public demo.

| Application | URL | How it stays available |
| --- | --- | --- |
| Portfolio | https://vishnu-portfolio-1ijm.onrender.com | Static hosting; no sleeping server or scheduled database expiry |
| CampusTrack browser edition | https://vishnu-campustrack-browser.onrender.com | Static hosting; records in the visitor's browser; JSON backup/restore |
| NoteLens | https://vishnu-notelens.onrender.com | Free Python service; sleeps when idle and wakes when visited |
| RepoCheck | https://vishnu-repocheck.onrender.com | Free Python service; sleeps when idle and wakes when visited |
| CampusTrack account edition | https://vishnu-campustrack.onrender.com | Free Python service with a trial PostgreSQL database expiring 31 October 2026 |

## What to do when you return

For a sleeping NoteLens, RepoCheck or account edition, just open its link and allow about a minute for startup. You do not need to start it manually. Avoid repeatedly refreshing while it wakes.

The portfolio and CampusTrack browser edition are static and do not have a Python startup delay. CampusTrack's browser edition saves records on the same browser/device. Clearing browser data, private browsing, changing devices or changing domains can lose that board. Download **Backup JSON** and keep the file safely; use **Restore backup** to bring it back. It has no cloud accounts or cross-device sync. Other people using the same browser profile can see the board.

NoteLens intentionally keeps notes temporarily: they disappear on restart or workspace expiry. Reload the sample or upload your notes again. RepoCheck does not intentionally save uploaded source.

## Staying within free limits

Render's free Python services share 750 runtime hours per workspace per calendar month. Idle sleeping conserves those hours. Do not add artificial keep-alive traffic: it uses the shared allowance and can cause all free Python services to be suspended until the next month.

Free services and static sites also have bandwidth and build limits. No paid service was created or upgraded. Check the Render Billing page for account-level usage and payment settings; the connector cannot read or set those account-wide billing controls. If a payment method is attached, review spending controls to avoid usage charges. If no payment method is attached, Render may suspend free services on quota exhaustion.

The free plan has no forever uptime promise. Keep source repositories and backups; they allow redeployment if a provider changes its terms. Static hosting has no current 30-day expiry, but remains subject to provider/account availability and usage limits.

## The original account edition

The original Python/PostgreSQL implementation is preserved. Its database expires on **31 October 2026 at 05:41 UTC / 11:11 India time**. It cannot be kept permanently by waking or manually restarting it. Export any useful account records before expiry. The browser edition remains available independently of that database.

Maintaining cloud accounts for free after the trial requires a separate non-expiring free database account and a secure connection migration. That is optional; it does not affect the browser edition's board.

## Publishing and recovery

For a manually suspended service, inspect its dashboard status and available resume controls. For an exhausted free runtime allowance, wait for the monthly reset; restarting does not replenish it.

For a failed deployment, review Render logs and GitHub Actions and restore the last good release. If a static service is unchanged after a source update, use **Manual Deploy → Deploy latest commit**. Its public-repository URL does not enable automatic updates without a connected Git provider. CampusTrack's account edition was deployed through a Blueprint with checks-pass auto-deploy.

A free site usually requires no periodic manual redeployment simply to remain hosted. Visit it when needed; use deployment actions for source/configuration changes or recovery.

## Validation

`scripts/check_live.py` exercises the public pages and APIs, including CampusTrack's original account edition and its free static edition. CampusTrack's **Browser edition checks** additionally cover real Chromium create/edit/delete, persistence after reload, sample isolation, backup/restore, rejection of invalid backups, CSV formula handling, filters, safe text rendering, device isolation and mobile layout.

Provider references: [Render free limits](https://render.com/docs/free), [deployment behavior](https://render.com/docs/deploys).
