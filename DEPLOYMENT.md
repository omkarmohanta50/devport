# Deployment

Production URL: https://shreeman-omkar.pages.dev/
Source repository: https://github.com/omkarmohanta50/devport

## Automatic deployment

GitHub Actions checks pull requests targeting main. Each push or merge to main runs npm ci, type checks, the production build, and link validation. If those pass, Wrangler deploys the resulting dist folder to Cloudflare Pages. Production deployments run serially.

The workflow uses the Node version in .nvmrc. It needs one GitHub repository secret, CLOUDFLARE_API_TOKEN. The Cloudflare account ID is configured in the workflow.

## One-time token setup

1. In Cloudflare, go to My Profile > API Tokens > Create Token > Create Custom Token.
2. Name it devport-github-deploy.
3. Grant Account > Cloudflare Pages > Edit.
4. Restrict Account Resources to the account owning shreeman-omkar.
5. Create the token and copy it directly into the GitHub repository secret. Do not place it in source code or chat.
6. In GitHub, open devport > Settings > Secrets and variables > Actions > New repository secret.
7. Name the secret CLOUDFLARE_API_TOKEN and paste its value.
8. Open Actions > Check and deploy portfolio. Rerun a failed run or choose Run workflow on main to verify the connection.

Use an expiration date appropriate for your deployment access, and rotate the secret when the token expires. Existing production stays live if checks or a deployment fail.

Official setup reference
https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/

## Local development

Use Node 24.22.3, then npm ci and npm run dev. In PowerShell, use npm.cmd if execution policy blocks npm.ps1.

Source changes must be committed and pushed to main to trigger publication. CI uploads the site automatically after that push. GitHub changes alone do not edit files in a local checkout until you pull them.

## Optional manual fallback

With Wrangler logged in locally, npm run deploy runs checks, builds and publishes the site. Normal publishing uses GitHub Actions.
