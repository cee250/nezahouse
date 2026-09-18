from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

BRAND_CSS = """/* Grand Chalet Inn brand system */
.brand-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    line-height: 0;
    padding: 6px 12px;
    min-height: 62px;
    background: rgba(255,255,255,.98);
    border: 1px solid rgba(255,255,255,.72);
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,.14);
    transition: transform .25s ease, box-shadow .25s ease;
}
.brand-logo:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(0,0,0,.18);
}
.brand-logo img {
    display: block;
    width: 156px;
    height: 50px;
    max-width: none;
    object-fit: contain;
    object-position: center;
}
.footer-brand-logo {
    display: flex;
    align-items: center;
    width: fit-content;
    min-height: 72px;
    margin-bottom: 14px;
}
.footer-brand-logo img {
    display: block;
    width: 178px;
    height: 66px;
    max-width: none;
    object-fit: contain;
    object-position: left center;
}
.site-loader {
    position: fixed;
    top: 18px;
    right: 18px;
    z-index: 9999;
    display: grid;
    place-items: center;
    width: auto;
    height: auto;
    padding: 8px 12px;
    background: rgba(255,255,255,.98);
    border: 1px solid rgba(26,26,46,.08);
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0,0,0,.16);
    opacity: 1;
    visibility: visible;
    transition: opacity .35s ease, visibility .35s ease;
}
.site-loader.is-hidden { opacity: 0; visibility: hidden; pointer-events: none; }
.site-loader img { width: 116px; height: 40px; object-fit: contain; animation: loader-pulse 1.35s ease-in-out infinite; }
@keyframes loader-pulse { 0%, 100% { transform: scale(.96); opacity: .82; } 50% { transform: scale(1); opacity: 1; } }
@media (max-width: 600px) {
    .brand-logo { min-height: 50px; padding: 4px 8px; border-radius: 10px; }
    .brand-logo img { width: 116px; height: 40px; }
    .footer-brand-logo { min-height: 62px; }
    .footer-brand-logo img { width: 154px; height: 58px; }
    .site-loader { top: 12px; right: 12px; padding: 6px 9px; }
    .site-loader img { width: 94px; height: 32px; }
}
"""

for page in sorted(SITE.glob("*.html")):
    text = page.read_text()

    # Keep the same polished logo treatment on every page, including pages
    # that were generated before the branding pass.
    updated, count = re.subn(
        r"/\* Grand Chalet Inn brand system \*/.*?(?=\s*</style>)",
        BRAND_CSS.rstrip(),
        text,
        count=1,
        flags=re.S,
    )
    if not count:
        updated = updated.replace("    </style>", BRAND_CSS + "    </style>", 1)

    # The booking page has a compact footer; give it the same brand anchor as
    # the full footer used on the other pages.
    if page.name == "booking.html" and 'class="footer-brand-logo"' not in updated:
        updated = updated.replace(
            '<div class="footer-bottom">',
            '<div class="footer-bottom">\n                <div class="footer-brand-logo" style="margin: 0 auto 14px; justify-content: center;"><img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" /></div>',
            1,
        )

    page.write_text(updated)
    print(f"Customized header and footer branding in {page.name}")
