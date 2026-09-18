from pathlib import Path
from PIL import Image

root = Path('/home/ubuntu/nezahouse')
asset_dir = root / 'site' / 'assets' / 'grand-chalet-inn'
source = Image.open(asset_dir / 'logo.png').convert('RGBA')

# Remove the white photo background so the supplied mark sits cleanly on any site surface.
pixels = source.load()
for y in range(source.height):
    for x in range(source.width):
        r, g, b, a = pixels[x, y]
        if r > 242 and g > 242 and b > 242:
            pixels[x, y] = (r, g, b, 0)
source.save(asset_dir / 'logo-transparent.png', optimize=True)

# Emblem-only transparent asset for the structured lockup.
emblem = source.crop((48, 20, 414, 315))
emblem.save(asset_dir / 'emblem-transparent.png', optimize=True)

old_header = '''<div class="logo brand-logo" onclick="window.location.href='index.html'">
                <img src="assets/grand-chalet-inn/logo-icon.png" alt="Grand Chalet Inn" />
            </div>'''
new_header = '''<div class="logo brand-lockup" onclick="window.location.href='index.html'" aria-label="Grand Chalet Inn home">
                <img class="brand-lockup-mark" src="assets/grand-chalet-inn/emblem-transparent.png" alt="" />
                <span class="brand-lockup-type"><strong>GRAND</strong><small>CHALET INN</small></span>
            </div>'''

old_footer = '''<h3 class="footer-brand-logo"><img src="assets/grand-chalet-inn/logo.png" alt="Grand Chalet Inn" /></h3>'''
new_footer = '''<h3 class="footer-brand-lockup">
                        <img class="brand-lockup-mark" src="assets/grand-chalet-inn/emblem-transparent.png" alt="" />
                        <span class="brand-lockup-type"><strong>GRAND</strong><small>CHALET INN</small></span>
                    </h3>'''

old_css_start = '        /* Grand Chalet Inn brand system */'
old_css_end = '        @media (max-width: 600px) { .brand-logo, .brand-logo img { width: 66px; height: 66px; } .footer-brand-logo { min-height: 118px; } .footer-brand-logo img { width: 106px; height: 118px; } }\n'
new_css = '''        /* Grand Chalet Inn brand system */
        .brand-lockup, .footer-brand-lockup { display: inline-flex; align-items: center; gap: 10px; cursor: pointer; color: inherit; }
        .brand-lockup { min-width: 184px; }
        .brand-lockup-mark { display: block; width: 42px; height: 42px; object-fit: contain; object-position: center; flex: 0 0 auto; }
        .brand-lockup-type { display: inline-flex; flex-direction: column; justify-content: center; line-height: 1; white-space: nowrap; }
        .brand-lockup-type strong { color: #a91d29; font: 800 1.06rem/1 Inter, sans-serif; letter-spacing: .18em; }
        .brand-lockup-type small { margin-top: 5px; color: currentColor; font: 700 .54rem/1 Inter, sans-serif; letter-spacing: .22em; }
        .footer-brand-lockup { gap: 14px; margin: 0 0 18px; }
        .footer-brand-lockup .brand-lockup-mark { width: 64px; height: 64px; }
        .footer-brand-lockup .brand-lockup-type strong { font-size: 1.38rem; }
        .footer-brand-lockup .brand-lockup-type small { font-size: .66rem; margin-top: 7px; }
        .site-loader { position: fixed; inset: 0; z-index: 9999; display: grid; place-items: center; padding: 24px; background: rgba(17, 24, 39, .42); backdrop-filter: blur(7px); opacity: 1; visibility: visible; transition: opacity .3s ease, visibility .3s ease; }
        .site-loader.is-hidden { opacity: 0; visibility: hidden; pointer-events: none; }
        .site-loader-card { width: min(252px, calc(100vw - 48px)); padding: 22px 24px 20px; border: 1px solid rgba(255,255,255,.8); border-radius: 22px; background: #fff; box-shadow: 0 22px 60px rgba(10, 18, 35, .25); text-align: center; }
        .site-loader img { display: block; width: 108px; height: 124px; margin: 0 auto 10px; object-fit: contain; animation: loader-pulse 1.35s ease-in-out infinite; }
        .site-loader-label { display: block; color: #9f1d29; font: 700 .72rem/1.2 Inter, sans-serif; letter-spacing: .18em; text-transform: uppercase; }
        .site-loader-dots { display: inline-flex; gap: 5px; margin-top: 11px; }
        .site-loader-dots i { display: block; width: 6px; height: 6px; border-radius: 50%; background: #b3202b; animation: loader-dot 1s ease-in-out infinite; }
        .site-loader-dots i:nth-child(2) { animation-delay: .15s; }
        .site-loader-dots i:nth-child(3) { animation-delay: .3s; }
        @keyframes loader-pulse { 0%, 100% { transform: scale(.97); opacity: .86; } 50% { transform: scale(1); opacity: 1; } }
        @keyframes loader-dot { 0%, 80%, 100% { transform: translateY(0); opacity: .45; } 40% { transform: translateY(-4px); opacity: 1; } }
        @media (max-width: 600px) {
            .brand-lockup { min-width: 148px; gap: 7px; }
            .brand-lockup-mark { width: 34px; height: 34px; }
            .brand-lockup-type strong { font-size: .83rem; letter-spacing: .14em; }
            .brand-lockup-type small { font-size: .43rem; letter-spacing: .17em; margin-top: 4px; }
            .footer-brand-lockup .brand-lockup-mark { width: 54px; height: 54px; }
            .footer-brand-lockup .brand-lockup-type strong { font-size: 1.14rem; }
            .footer-brand-lockup .brand-lockup-type small { font-size: .56rem; }
        }
'''

for page in sorted((root / 'site').glob('*.html')):
    text = page.read_text()
    if old_header in text:
        text = text.replace(old_header, new_header)
    if old_footer in text:
        text = text.replace(old_footer, new_footer)
    start = text.find(old_css_start)
    if start < 0:
        raise RuntimeError(f'Brand CSS not found in {page}')
    end = text.find(old_css_end, start)
    if end < 0:
        raise RuntimeError(f'Brand CSS end not found in {page}')
    end += len(old_css_end)
    text = text[:start] + new_css + text[end:]
    page.write_text(text)
