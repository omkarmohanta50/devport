# Manual deployment to Cloudflare Pages

The GitHub source repository remains devport. The Cloudflare project is shreeman-omkar, giving https://shreeman-omkar.pages.dev if that name is available. Deployments are manual. The visitor counter is removed and the site is fully static.

## 1. Open this folder in PowerShell

    cd C:\Users\omkar\Dcode\portfolio
    node --version

Use the Node version in .nvmrc (24.22.3) or another Astro-supported version, at least 22.23.4. The default Node installed on this computer was 22.14.0 during preparation, so it needs updating or selecting before running npm commands.

For this computer, the Codex bundled Node 24.22.3 can also be selected for the current PowerShell session:

    $env:Path = 'C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt\dependencies\node\bin;' + $env:Path
    node --version

## 2. Install the locked dependencies

    npm ci

This installs Astro and the project-local Wrangler CLI from package-lock.json.

## 3. Sign in to Cloudflare

    npx wrangler login
    npx wrangler whoami

Login opens Cloudflare authorization in a browser. Approve it with your own account. whoami verifies the account before publishing. If several accounts appear, select the intended one when Wrangler asks. Never commit API tokens.

## 4. Create the Pages project once

    npx wrangler pages project create shreeman-omkar --production-branch main

This creates the Cloudflare Pages container for deployments. If the project already exists in your account, skip creation. If the desired address is unavailable, choose another name and update wrangler.jsonc, package.json's deploy command, astro.config.mjs, and public/robots.txt to the confirmed address before building.

This uses Direct Upload through Wrangler. Git pushes alone do not publish the website.

## 5. Build, check, and publish

    npm run deploy

This command runs type checks, builds static pages into dist, validates local links/assets, and finally uploads dist to Cloudflare. Earlier failures prevent publishing. The last Wrangler step is the actual public deployment.

To review without publishing, run these steps instead:

    npm run check
    npm run build
    npm run validate
    npm run preview

Review the Local URL printed by Astro. Stop preview with Ctrl+C. Then use npm run deploy when ready.

## 6. Verify the result

Open the exact production URL printed by Wrangler. Check Home, Blog, Books, Favourites, the résumé PDF, hover previews, theme switching, and the avatar switcher. Check from a signed-out browser and a phone.

The GitHub contribution map is a stored snapshot. Updating the website requires a fresh local build and another manual deployment.

## Later deployments

    git pull
    npm ci
    npm run deploy

Run from the project folder with the supported Node version selected. Commit and push source changes separately when appropriate. To roll back, use Cloudflare's previous production deployment in the dashboard or redeploy a previously verified source version.

Official documentation
https://developers.cloudflare.com/pages/get-started/direct-upload/
https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/
