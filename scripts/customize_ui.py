from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

BRAND_CSS = """/* Grand Chalet Inn brand system */
.brand-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 0;
    padding: 5px 10px;
    min-height: 58px;
    background: rgba(255,255,255,.96);
    border-radius: 12px;
    box-shadow: 0 5px 18px rgba(0,0,0,.12);
}
.brand-logo img {
    display: block;
    width: 148px;
    height: 54px;
    object-fit: contain;
    object-position: center;
}
.footer-brand-logo {
    display: flex;
    align-items: center;
    min-height: 82px;
}
.footer-brand-logo img {
    display: block;
    width: 190px;
    height: 82px;
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
    background: rgba(255,255,255,.96);
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0,0,0,.16);
    opacity: 1;
    visibility: visible;
    transition: opacity .35s ease, visibility .35s ease;
}
.site-loader.is-hidden { opacity: 0; visibility: hidden; pointer-events: none; }
.site-loader img { width: 112px; height: 42px; object-fit: contain; animation: loader-pulse 1.35s ease-in-out infinite; }
@keyframes loader-pulse { 0%, 100% { transform: scale(.96); opacity: .82; } 50% { transform: scale(1); opacity: 1; } }
@media (max-width: 600px) {
    .brand-logo { min-height: 48px; padding: 4px 7px; border-radius: 9px; }
    .brand-logo img { width: 112px; height: 42px; }
    .footer-brand-logo img { width: 160px; height: 70px; }
    .site-loader { top: 12px; right: 12px; padding: 6px 9px; }
    .site-loader img { width: 92px; height: 34px; }
}
"""

for page in SITE.glob("*.html"):
    text = page.read_text()
    # Replace the existing inline brand/loader CSS without touching page-specific CSS.
    updated, count = re.subn(
        r"/\* Grand Chalet Inn brand system \*/.*?(?=\s*</style>)",
        BRAND_CSS.rstrip(),
        text,
        count=1,
        flags=re.S,
    )
    if count:
        page.write_text(updated)
        print(f"Customized header, footer, and loader in {page.name}")
    else:
        print(f"Brand CSS marker not found in {page.name}; skipped")
