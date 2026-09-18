from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
source = ROOT / "site" / "assets" / "nezahouse"
target = ROOT / "site" / "assets" / "grand-chalet-inn"

# The HTML pages use the new branded asset path, while the existing photo/video
# files remain in the original asset directory. Copy them during the Netlify
# build so every referenced asset is available in the published site.
target.mkdir(parents=True, exist_ok=True)
if source.is_dir():
    for asset in source.iterdir():
        destination = target / asset.name
        if asset.is_file() and not destination.exists():
            shutil.copy2(asset, destination)

# Keep the header and footer marks balanced on every page. This is injected at
# build time because the static pages contain their own inline styles.
brand_css = """
<style id="grand-chalet-brand-sizing">
/* Professional logo sizing */
.navbar .brand-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 64px;
    padding: 5px 12px;
    border-radius: 12px;
    background: rgba(255,255,255,.97);
    box-shadow: 0 5px 18px rgba(0,0,0,.14);
}
.navbar .brand-logo img {
    display: block;
    width: 180px;
    height: 62px;
    max-width: none;
    object-fit: contain;
    object-position: center;
}
footer .footer-brand-logo {
    display: flex;
    align-items: center;
    min-height: 64px;
    margin-bottom: 12px;
}
footer .footer-brand-logo img {
    display: block;
    width: 142px;
    height: 62px;
    max-width: none;
    object-fit: contain;
    object-position: left center;
}
@media (max-width: 600px) {
    .navbar .brand-logo { min-height: 52px; padding: 4px 8px; border-radius: 9px; }
    .navbar .brand-logo img { width: 138px; height: 50px; }
    footer .footer-brand-logo { min-height: 54px; }
    footer .footer-brand-logo img { width: 120px; height: 54px; }
}
</style>
"""

for page in (ROOT / "site").glob("*.html"):
    text = page.read_text()
    if 'id="grand-chalet-brand-sizing"' not in text:
        text = text.replace("</head>", brand_css + "\n</head>", 1)
        page.write_text(text)

print(f"Prepared branded assets in {target} and standardized logo sizing")
