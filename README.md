# Oraculum Digital Labs — corporate website

Public site: https://oraculumlabs.eu

## Production deployment

- **Authoritative source:** `main` branch in `Taxxmaster-Dev/oraculumlabs-website`.
- **Production host:** Render static site named `oraculumlabs-website` (service ID `srv-db2u3tqjnfac7381tj90`).
- **Production domain:** `oraculumlabs.eu` (DNS resolves to Render, not to GitHub Pages).
- **Deployment:** `.github/workflows/deploy-render.yml` runs on every push to `main` (and manually), validates site files, triggers a Render deploy through a *secret* Deploy Hook, and compares all eight public website assets with the committed files.
- **Troubleshooting:** `.github/workflows/hosting-diagnostics.yml` can be started manually to inspect production DNS and HTTP responses.

GitHub Pages publishing is retired from this repository. The previous Pages workflow and `CNAME` file were removed. Render is the sole intended production host. The existing GitHub Pages site should also be disabled in the repository's **Settings → Pages** when possible.

### One-time setup (do not commit or share the secret value)

1. In the Render dashboard, open **oraculumlabs-website → Settings → Deploy Hook**. Copy the full private deploy-hook URL.
2. In GitHub, open **Settings → Secrets and variables → Actions → New repository secret**. Set **Name** to `RENDER_DEPLOY_HOOK_URL`, paste the URL as **Secret**, and save.
3. In Render, under **Settings → Auto-Deploy**, set **Off** once the GitHub Actions hook is installed, avoiding duplicate deploy triggers.
4. Open **GitHub → Actions → Deploy Oraculum production to Render → Run workflow**. Wait for a green result and inspect the homepage and legal pages at the custom domain.
5. In GitHub **Settings → Pages**, disable Pages publishing (the old Pages deployment is no longer used by production DNS).

If the hook is missing or a deployment fails, the GitHub Actions workflow fails visibly instead of silently leaving an outdated page online. The last successful live Render site remains online while the issue is fixed.

Do **not** add the Render Deploy Hook URL or a Render API key to this public repository.
