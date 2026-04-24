# PhotoPick — Web

Marketing / introduction site for [PhotoPick](https://github.com/derekdylu/PhotoPick).
Built with Next.js 14 (App Router), TypeScript, and Tailwind CSS. Renders on the
server (RSC) for the best SEO.

## Local development

```bash
cd web
npm install
npm run dev
```

Visit http://localhost:3000.

## Build & run production

```bash
npm run build
npm start
```

Verify SSR output has meta + JSON-LD baked into the first byte:

```bash
curl -s http://localhost:3000 | grep -E 'SoftwareApplication|og:title'
```

Also confirm `/sitemap.xml` and `/robots.txt` return 200.

## Environment

Copy `.env.example` to `.env.local` and set `NEXT_PUBLIC_SITE_URL` to the
production URL once the Vercel domain is decided. This value is used for
`metadataBase`, canonical URLs, the sitemap, and JSON-LD.

## Deployment

The GitHub Actions workflow at `.github/workflows/web-deploy.yml` builds and
deploys to **Vercel** on every push to `main` that touches `web/**` (production
deploy) and on PRs touching `web/**` (preview deploy).

### One-time setup

1. Create a Vercel project for this site:
   ```bash
   cd web
   npx vercel link
   ```
   Accept defaults; Vercel will create `.vercel/project.json` locally (gitignored).
2. Grab the org and project IDs from `.vercel/project.json`.
3. Create a Vercel token at https://vercel.com/account/tokens.
4. In GitHub repo settings → **Secrets and variables → Actions**, add:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
5. In the Vercel project settings, set `NEXT_PUBLIC_SITE_URL` as an environment
   variable pointing to the production domain.

That's it — subsequent pushes to `web/**` deploy automatically.
