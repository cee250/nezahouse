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

print(f"Prepared branded assets in {target}")
