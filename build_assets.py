import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ORANGE, RED, INK, MUTED = '#B85A0A', '#A3222D', '#2B1D1F', '#7A6A64'

def banner():
    w, h = 840, 230
    digits = '1.048596'
    tw, th, gap, dw = 44, 72, 7, 14
    total = sum(dw if c == '.' else tw for c in digits) + gap * (len(digits) - 1)
    x = (w - total) / 2
    y = 34
    parts = []
    for c in digits:
        if c == '.':
            parts.append(f'<circle cx="{x + dw / 2:.1f}" cy="{y + th - 10}" r="3.6" fill="{ORANGE}"/>')
            x += dw + gap
            continue
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="22" fill="#FFF6EC" stroke="#E9C9A8" stroke-width="1.2"/>')
        parts.append(f'<text x="{x + tw / 2:.1f}" y="{y + th / 2 + 13}" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="38" fill="{ORANGE}">{c}</text>')
        x += tw + gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="#FBF8F6" stroke="#EFE8E4"/>
{''.join(parts)}
<text x="{w / 2}" y="152" text-anchor="middle" font-family="-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="30" font-weight="600" fill="{INK}">Yumiko Sturluson</text>
<text x="{w / 2}" y="184" text-anchor="middle" font-family="-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="16" fill="{MUTED}">Lab Mem 004 · Future Gadget Lab</text>
</svg>
'''

def flask():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
<path d="M4.3 10h7.4l1.4 2.6a1.3 1.3 0 0 1-1.1 1.9H4a1.3 1.3 0 0 1-1.1-1.9z" fill="{ORANGE}" fill-opacity="0.28"/>
<path d="M6.5 1.5v4.2L2.9 12.6a1.3 1.3 0 0 0 1.1 1.9h8a1.3 1.3 0 0 0 1.1-1.9L9.5 5.7V1.5M5.5 1.5h5" stroke="{ORANGE}" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="7" cy="11.8" r="0.8" fill="{ORANGE}"/><circle cx="9.4" cy="12.6" r="0.55" fill="{ORANGE}"/><circle cx="8.4" cy="8.6" r="0.45" fill="{ORANGE}"/>
</svg>
'''

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'assets'), exist_ok=True)
    open(os.path.join(ROOT, 'assets', 'banner.svg'), 'w').write(banner())
    open(os.path.join(ROOT, 'assets', 'flask.svg'), 'w').write(flask())
    print('assets built')
