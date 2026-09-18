from pathlib import Path
from PIL import Image

root = Path('/home/ubuntu/nezahouse')
asset_dir = root / 'site' / 'assets' / 'grand-chalet-inn'
logo = Image.open(asset_dir / 'logo.png').convert('RGBA')
logo.crop((48, 20, 414, 315)).save(asset_dir / 'logo-icon.png', optimize=True)

header_old = '''<div class="logo brand-logo" onclick="window.location.href='index.html'">
                <img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" />
            </div>'''
header_new = '''<div class="logo brand-logo" onclick="window.location.href='index.html'">
                <img src="assets/grand-chalet-inn/logo-icon.png" alt="Grand Chalet Inn" />
            </div>'''

for page in sorted((root / 'site').glob('*.html')):
    text = page.read_text()
    text = text.replace(header_old, header_new)
    page.write_text(text)
