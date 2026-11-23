# Omkar Mohanta — portfolio implementation plan

Build a single-page public profile for recruiters hiring DevOps engineers. A visitor should recognize Omkar’s role, understand his work in deployment automation and AI agent development, and reach his résumé or email from the opening screen.

## 1. Establish the public content

- Start from [Omkar’s 2026 résumé](../resume/Omkar_Mohanta_Resume_2026.pdf), [LinkedIn](https://www.linkedin.com/in/omkarmohanta/), [work GitHub](https://github.com/omkarmohanta09), and [personal GitHub](https://github.com/omkarmohanta50). The relative résumé path is specific to the original workspace. If implementing elsewhere, request the source PDF if needed.
- Verify the exact VegaStack employment title and dates, degree wording, credential titles and issuers, and preferred public email. “DevOps Engineer” is the hiring headline. Use the verified employment title in the background row. Leave unresolved dates out of the preview and flag them for review.
- Public contributions support descriptions of deployment recovery, container delivery, and operator tooling. Representative sources include [deployment recovery](https://github.com/vegastack/vegastack-labs/pull/399), [signed publication](https://github.com/vegastack/vegastack-labs/pull/387), and [health reporting](https://github.com/vegastack/vegastack-labs/pull/406). Use these for editorial verification only.
- Omkar personally confirmed building AI agents and working with **Vercel Eve**. Use that spelling. Keep claims about agent responsibilities at this level unless Omkar supplies further detail.
- Apply the project-free brief to every public surface, including hero copy, illustrations, expertise, employment history, PDF, and social preview. Omit project cards, case studies, repository excerpts, named builds, PR counts, and architecture diagrams. Profile-level GitHub links are intentional.

## 2. Set up the site

1. Inspect the target checkout and preserve existing work. At handoff the portfolio workspace contained only this plan.
2. Use Astro, TypeScript in strict mode, and custom CSS. Check the [current stable Astro release](https://astro.build/blog/) and its [installation requirements](https://docs.astro.build/en/install-and-setup/) at implementation time. Select a supported Node version, record it for local development and CI, and commit one package-manager lockfile.
3. Configure static output to `dist/`. Suggested structure: `src/pages/index.astro` for composition, `src/data/profile.ts` for typed content and URLs, `src/layouts/Base.astro` for metadata and document structure, `src/styles/global.css` for layout and tokens, and `public/` for static assets. Keep the primary experience usable with JavaScript disabled.
4. Provide scripts for local development, type checking, production build, and production preview. A clean checkout must build with a frozen lockfile.

## 3. Design the opening screen

Use [Dev Jhawar](https://devjhawar.com/) for typographic hierarchy, [Dhruv Jaradi](https://jdhruv.dev/) for reading width and contact grouping, and [Alok Mishra](https://heyalok.com/) for compact experience rows. These are composition references. Create an original layout and use Omkar’s own assets.

- **Header.** Place a custom OM monogram linking home on the left. Keep Expertise, Background, and Résumé visible on desktop and mobile.
- **Hero.** Give Omkar’s name the largest type size, followed by “DevOps Engineer.” Proposed introduction: “I build deployment automation, tools for infrastructure teams, and AI agents. At VegaStack, I work on how software gets released, how interrupted deployments recover, and how operators see what needs their attention.”
- **Actions.** Place “View résumé” and “Email me” directly beneath the introduction. Use native links to the PDF and verified email address.
- **Composition.** Default to an intentional type-led layout. If Omkar supplies a portrait approved for public use, place a tightly cropped monochrome version to the right on desktop and after the primary actions on mobile. Avoid an empty image slot.
- **Visual system.** Use paper `#F8F9F7`, ink `#17201D`, secondary text `#47534E`, and cobalt `#214FCC` for links, focus, and the primary action. Self-host Archivo Narrow for headings and Geist for body text, retaining their licenses. Use a maximum layout width around 1,150 px, body text around 17–18 px, and a reading measure near 65 characters.
- **Details.** Use thin rules, aligned columns, and generous spacing. Use individual Lucide FileText and Mail icons next to visible labels. Hide decorative icons from assistive technology. Use native scrolling, visible focus, and immediate hover feedback. Omit decorative animation.

## 4. Implement the body and navigation

1. **Expertise** at `/#expertise`. Create three editorial rows. Platform engineering covers cloud infrastructure, containers, and infrastructure as code. Release engineering covers CI/CD, recovery, and tools for operators. AI agents covers hands-on agent development, including Vercel Eve. Write one plain-language sentence per row. Select a few résumé-supported tools where they add specificity.
2. **Background** at `/#background`. Lead with VegaStack, followed by B.Tech education and selected credentials. Align dates in a separate column on wide screens and stack them beneath the corresponding entry on phones. Identify coursework using its issued title.
3. **Contact.** Show Email, LinkedIn, Work GitHub, and Personal GitHub as readable links. Use the account mapping in step 1. Provide comfortable tap targets and meaningful focus order.
4. Use one main heading, semantic landmarks, descriptive links, a skip link, and stable section IDs. Keep headings visible when following anchor links.

## 5. Prepare recruiter-facing assets

- Create a separate public edition at `/resume.pdf`, preserving the source résumé. Include a concise summary, verified responsibilities, skills, education, credentials, and approved contact details. Check selectable text, legibility, working links, and agreement with the homepage.
- Create an OM favicon and a 1200 × 630 share image containing Omkar’s name and role. Check legibility at small preview sizes.
- Set the page title to “Omkar Mohanta — DevOps Engineer.” Write a short description mentioning platform work, deployment automation, and AI agents. Configure canonical URL, Open Graph metadata, sitemap, and robots file against the final public origin.

## 6. Deliver the first preview

Serve the complete homepage locally with the actual copy, contact actions, and working résumé link. Show a desktop and a phone-sized view. Identify any unresolved factual fields. Let Omkar review the design and public-facing materials before public launch.

## 7. Verify the release candidate

- Run a clean install, Astro type checks, and a production build. Preview the built output. In GitHub Actions, run the same checks plus internal link and asset validation on pull requests.
- Test at narrow phone, tablet, and desktop widths. Check the name, header links, long titles, and contact row for wrapping and horizontal overflow. Test at 200% zoom.
- Complete the recruiter journey using keyboard only and again with JavaScript disabled. Verify logical focus order, visible focus, readable contrast, correct anchor targets, and PDF access from the opening screen.
- Open each profile link and verify its identity. Check the email destination without sending mail. Review the rendered PDF, social image, and mobile layout. Confirm every public surface meets the project-free brief.

## 8. Publish and hand off

1. After preview review, deploy the verified static build to public HTTPS hosting. Use the host-provided address unless Omkar supplies a domain. Set the final public origin, rebuild metadata, and deploy the matching artifact.
2. In a signed-out session, open the homepage and PDF directly. Check the favicon, share image, canonical URL, sitemap, robots file, and social preview. Verify that the production site is publicly accessible and indexable.
3. Deliver the live URL, source location, commit or deployment identifier, build and preview commands, and the location of editable profile data. Record checks performed and any outstanding verification. Retain the previous successful deployment for rollback on subsequent releases.

**Completion condition:** a recruiter can open the public link on a phone, identify Omkar as a DevOps engineer who also builds AI agents, read his professional background, open a project-free résumé, and contact him directly.

## Deferred music integration

Omkar deferred the listening card on November 23, 2026. The public website has no music card. The local server exposes no music endpoint. YouTube Music connection notes and prototype scripts are retained for future work. Resume only when requested. No account authorization has been completed.
