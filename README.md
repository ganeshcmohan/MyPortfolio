# Ganesh C — Portfolio

Personal portfolio site built with [Astro](https://astro.build) and Tailwind CSS.

## Node.js version

- **Minimum:** Node 16.12+ (Astro 3 — current setup)
- **Recommended:** Node 20 LTS via [nvm](https://github.com/nvm-sh/nvm)

If you see `Node.js v16 is not supported by Astro` you had Astro 5 installed. Reinstall deps:

```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Upgrade Node (recommended):**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
cd ~/work/MyPortfolio
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Preview (no install required)

Open [`docs/index.html`](docs/index.html) in a browser — static portfolio with dark mode.

Copy the resume PDF into `docs/` for the download button:

```bash
cp ganesh_resume_2026.pdf docs/
cp ganesh_resume_2026.pdf public/   # for Astro build
```

## Quick start (Astro — recommended for deploy)

```bash
npm install
npm run dev
```

Open [http://localhost:4321](http://localhost:4321).

## Build for production

```bash
npm run build
npm run preview
```

Static output is in `dist/` — deploy to GitHub Pages, Vercel, or Netlify.

## Content

Edit [`src/data/resume.json`](src/data/resume.json) to update site content.

Resume PDF: place `ganesh_resume_2026.pdf` in `public/`.

Regenerate PDF from markdown:

```bash
python3 generate_resume_pdf.py
cp ganesh_resume_2026.pdf public/
```

## Deploy

### Option A — GitHub Pages (automatic)

1. Push this repo to GitHub (e.g. `YourUsername/MyPortfolio`)
2. **Settings → Pages → Build and deployment:** Source = **GitHub Actions**
3. Push to `main` — workflow [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) builds and deploys
4. Site URL: `https://YourUsername.github.io/MyPortfolio/`

Update [`astro.config.mjs`](astro.config.mjs):

```js
site: "https://YourUsername.github.io",
base: "/MyPortfolio",   // set base to "/" if repo is YourUsername.github.io
```

### Option B — Static preview (`docs/` folder)

1. **Settings → Pages → Source:** Deploy from branch `main`, folder `/docs`
2. Copy PDF: `cp ganesh_resume_2026.pdf docs/`
3. URL: `https://YourUsername.github.io/MyPortfolio/`

### Custom domain

1. Create [`public/CNAME`](public/CNAME) with your domain (see [`public/CNAME.example`](public/CNAME.example))
2. DNS: **CNAME** `www` or subdomain → `YourUsername.github.io`
3. GitHub **Settings → Pages → Custom domain** → enter domain → enforce HTTPS
4. Update `astro.config.mjs`: `site: "https://yourdomain.com"`, `base: "/"`

## Social links

Edit in [`src/data/resume.json`](src/data/resume.json):

```json
"linkedin": "https://www.linkedin.com/in/your-profile",
"github": "https://github.com/your-username"
```

Also update [`docs/index.html`](docs/index.html) if using the static preview.
