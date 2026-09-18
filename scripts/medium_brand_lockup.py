from pathlib import Path

root = Path('/home/ubuntu/nezahouse')
replacements = {
    '        .brand-lockup { min-width: 184px; }': '        .brand-lockup { min-width: 156px; }',
    '        .brand-lockup-mark { display: block; width: 42px; height: 42px;': '        .brand-lockup-mark { display: block; width: 34px; height: 34px;',
    '        .brand-lockup-type strong { color: #a91d29; font: 800 1.06rem/1 Inter, sans-serif;': '        .brand-lockup-type strong { color: #a91d29; font: 800 .9rem/1 Inter, sans-serif;',
    '        .brand-lockup-type small { margin-top: 5px; color: currentColor; font: 700 .54rem/1 Inter, sans-serif;': '        .brand-lockup-type small { margin-top: 4px; color: currentColor; font: 700 .47rem/1 Inter, sans-serif;',
    '        .footer-brand-lockup { gap: 14px; margin: 0 0 18px; }': '        .footer-brand-lockup { gap: 10px; margin: 0 0 14px; }',
    '        .footer-brand-lockup .brand-lockup-mark { width: 64px; height: 64px; }': '        .footer-brand-lockup .brand-lockup-mark { width: 48px; height: 48px; }',
    '        .footer-brand-lockup .brand-lockup-type strong { font-size: 1.38rem; }': '        .footer-brand-lockup .brand-lockup-type strong { font-size: 1.08rem; }',
    '        .footer-brand-lockup .brand-lockup-type small { font-size: .66rem; margin-top: 7px; }': '        .footer-brand-lockup .brand-lockup-type small { font-size: .52rem; margin-top: 5px; }',
    '            .brand-lockup { min-width: 148px; gap: 7px; }': '            .brand-lockup { min-width: 132px; gap: 6px; }',
    '            .brand-lockup-mark { width: 34px; height: 34px; }': '            .brand-lockup-mark { width: 29px; height: 29px; }',
    '            .brand-lockup-type strong { font-size: .83rem; letter-spacing: .14em; }': '            .brand-lockup-type strong { font-size: .72rem; letter-spacing: .12em; }',
    '            .brand-lockup-type small { font-size: .43rem; letter-spacing: .17em; margin-top: 4px; }': '            .brand-lockup-type small { font-size: .38rem; letter-spacing: .14em; margin-top: 3px; }',
    '            .footer-brand-lockup .brand-lockup-mark { width: 54px; height: 54px; }': '            .footer-brand-lockup .brand-lockup-mark { width: 42px; height: 42px; }',
    '            .footer-brand-lockup .brand-lockup-type strong { font-size: 1.14rem; }': '            .footer-brand-lockup .brand-lockup-type strong { font-size: .96rem; }',
    '            .footer-brand-lockup .brand-lockup-type small { font-size: .56rem; }': '            .footer-brand-lockup .brand-lockup-type small { font-size: .46rem; }',
}
for page in sorted((root / 'site').glob('*.html')):
    text = page.read_text()
    for old, new in replacements.items():
        text = text.replace(old, new)
    page.write_text(text)
