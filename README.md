# Neza House

Static snapshot of the public Neza House website deployed at `https://nezahouse.netlify.app/`.

## Contents

The `site/` directory contains the mirrored pages and locally cached Unsplash image assets:

- `index.html` — home page
- `rooms.html` — rooms and suites
- `gallery.html` — photo gallery
- `contact.html` — contact page
- `booking.html` — booking page
- `assets/` — locally cached image assets

This snapshot was collected on 2026-09-04 for continued development. External services such as Google Fonts, Font Awesome, Google Maps, WhatsApp, and mail/telephone links remain external by design.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000 --directory site
```

Then open <http://localhost:8000>.
