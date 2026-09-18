from pathlib import Path
from PIL import Image, ImageChops

root = Path('/home/ubuntu/nezahouse')
source = Path('/home/ubuntu/upload/PHOTO-2026-09-17-21-38-50.jpg.jpeg')
asset_dir = root / 'site' / 'assets' / 'grand-chalet-inn'
asset_dir.mkdir(parents=True, exist_ok=True)

# Preserve the supplied source and make a tightly framed transparent PNG for UI use.
im = Image.open(source).convert('RGBA')
pix = im.load()
bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
diff = ImageChops.difference(im.convert('RGB'), bg.convert('RGB'))
# Ignore tiny JPEG noise around the white background.
bbox = diff.point(lambda p: 255 if p > 12 else 0).getbbox()
if bbox:
    left, top, right, bottom = bbox
    pad = int(max(right-left, bottom-top) * 0.08)
    bbox = (max(0, left-pad), max(0, top-pad), min(im.width, right+pad), min(im.height, bottom+pad))
    im = im.crop(bbox)
# Keep a little white around the red mark, but remove the large original whitespace.
im.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
im.save(asset_dir / 'logo.png', optimize=True)
im.save(asset_dir / 'logo.webp', 'WEBP', quality=92, method=6)

style = '''
        /* Grand Chalet Inn brand system */
        .brand-logo { display: inline-flex; align-items: center; line-height: 0; }
        .brand-logo img { display: block; width: 132px; height: 52px; object-fit: contain; object-position: center; }
        .footer-brand-logo img { width: 168px; height: 82px; }
        .site-loader { position: fixed; inset: 0; z-index: 9999; display: grid; place-items: center; background: #fff; opacity: 1; visibility: visible; transition: opacity .35s ease, visibility .35s ease; }
        .site-loader.is-hidden { opacity: 0; visibility: hidden; pointer-events: none; }
        .site-loader img { width: min(230px, 52vw); height: auto; animation: loader-pulse 1.35s ease-in-out infinite; }
        @keyframes loader-pulse { 0%, 100% { transform: scale(.96); opacity: .82; } 50% { transform: scale(1); opacity: 1; } }
        @media (max-width: 600px) { .brand-logo img { width: 112px; height: 46px; } .footer-brand-logo img { width: 150px; height: 72px; } }
'''
loader_markup = '''
    <div class="site-loader" id="siteLoader" role="status" aria-label="Loading Grand Chalet Inn">
        <img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" />
    </div>
'''
loader_script = '''
    <script>
        window.addEventListener('load', function () {
            var loader = document.getElementById('siteLoader');
            if (loader) { loader.classList.add('is-hidden'); setTimeout(function () { loader.remove(); }, 500); }
        });
    </script>
'''

pages = sorted((root / 'site').glob('*.html'))
for page in pages:
    text = page.read_text()
    # Page titles and all human-facing old brand strings.
    text = text.replace('Neza House', 'Grand Chalet Inn').replace('Neza<span>House</span>', 'Grand Chalet Inn')
    text = text.replace('Neza <span>House</span>', 'Grand Chalet Inn')
    text = text.replace('Neza<span>House</span>', 'Grand Chalet Inn')
    text = text.replace('nezahouse.com', 'grandchaletinn.com')
    text = text.replace('NEZA-', 'GCI-').replace('NEZA-2026-XXXX', 'GCI-2026-XXXX')
    text = text.replace('nezahouse_bookings', 'grand_chalet_inn_bookings')
    text = text.replace('nezahouse.netlify.app', 'grandchaletinn.netlify.app')
    text = text.replace('assets/nezahouse/', 'assets/grand-chalet-inn/')
    # Replace the header's old icon/text treatment with the supplied logo.
    text = text.replace('<div class="logo" onclick="window.location.href=\'index.html\'">\n                <i class="fas fa-crown"></i>Grand Chalet Inn\n            </div>', '<div class="logo brand-logo" onclick="window.location.href=\'index.html\'">\n                <img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" />\n            </div>')
    # Handle any variant left by page-specific formatting.
    text = text.replace('<div class="logo" onclick="window.location.href=\'index.html\'">\n                <i class="fas fa-crown"></i>Grand Chalet Inn\n            </div>', '<div class="logo brand-logo" onclick="window.location.href=\'index.html\'">\n                <img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" />\n            </div>')
    # Replace footer brand heading wherever it occurs.
    text = text.replace('<h3><i class="fas fa-crown"></i>Grand Chalet Inn</h3>', '<h3 class="footer-brand-logo"><img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" /></h3>')
    # Add favicon and loader styling/markup once per page.
    if 'assets/grand-chalet-inn/logo.png" rel="icon"' not in text:
        text = text.replace('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />', '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <link rel="icon" type="image/png" href="assets/grand-chalet-inn/logo.png" />', 1)
    if '/* Grand Chalet Inn brand system */' not in text:
        text = text.replace('    </style>', style + '    </style>', 1)
    if 'id="siteLoader"' not in text:
        text = text.replace('<body>', '<body>\n' + loader_markup, 1)
        text = text.replace('</body>', loader_script + '\n</body>', 1)
    page.write_text(text)

# Update project metadata and backend email copy.
for rel in ['README.md', 'package.json', 'package-lock.json', 'netlify/functions/send-booking.js']:
    path = root / rel
    text = path.read_text()
    text = text.replace('Neza House', 'Grand Chalet Inn').replace('NezaHouse', 'GrandChaletInn').replace('nezahouse', 'grandchaletinn')
    text = text.replace('nezahouse.com', 'grandchaletinn.com')
    text = text.replace('NEZA-', 'GCI-')
    path.write_text(text)
