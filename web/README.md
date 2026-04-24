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

Deployed via Vercel's native Git integration. In the Vercel project:

- **Root Directory**: `web`
- **Framework Preset**: Next.js
- **Environment Variables**: set `NEXT_PUBLIC_SITE_URL` to the production
  domain (used for `metadataBase`, canonical URLs, sitemap, and JSON-LD)

Pushes to `main` trigger a production deploy; PRs get preview deploys
automatically.
