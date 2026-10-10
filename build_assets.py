import os

ROOT = os.path.dirname(os.path.abspath(__file__))
USER = 'YumikoKawaii'
ORANGE, RED, INK, MUTED, CREAM, EDGE, TUBE = '#B85A0A', '#A3222D', '#2B1D1F', '#7A6A64', '#FBF8F6', '#E9C9A8', '#FFF6EC'
SANS = "-apple-system, 'Segoe UI', 'Hiragino Sans', 'Noto Sans JP', Helvetica, Arial, sans-serif"
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'
W = 840

SECTIONS = [
    ('s1', '§1', 'Abstract'),
    ('s2', '§2', 'Methods'),
    ('s3', '§3', 'Results'),
]

ABSTRACT = 'Software engineer at the Future Gadget Lab (Lab Mem 004), writing mostly Go and TypeScript.<br>ゆみこせかいでいちばんかわいい！'

METHODS = [
    ('Go', 'F6D9DC', 'go', '8A1C26'),
    ('TypeScript', 'FDE9D6', 'typescript', '8A4508'),
    ('Java', 'DCEFEC', 'openjdk', '155A54'),
    ('Python', 'E2E9F3', 'python', '2E4D72'),
    ('Docker', 'F6D9DC', 'docker', '8A1C26'),
]

RESULTS = [
    ('nexus', 'Go'),
    ('hermeneus', 'Go'),
    ('keue', 'Go'),
    ('hlidskjalf', 'Go'),
    ('akashic', 'TypeScript'),
]

def meter(cx, y, tw=26, th=40, gap=4, dw=8, size=22):
    digits = '1.048596'
    total = sum(dw if c == '.' else tw for c in digits) + gap * (len(digits) - 1)
    x = cx - total / 2
    out = []
    for c in digits:
        if c == '.':
            out.append(f'<circle cx="{x + dw / 2:.1f}" cy="{y + th - 6}" r="2.4" fill="{ORANGE}"/>')
            x += dw + gap
            continue
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="13" fill="{TUBE}" stroke="{EDGE}"/>')
        out.append(f'<text x="{x + tw / 2:.1f}" y="{y + th / 2 + 8}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{ORANGE}">{c}</text>')
        x += tw + gap
    return ''.join(out)

def title():
    h = 190
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="{CREAM}" stroke="#EFE8E4"/>
<text x="{W / 2}" y="42" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">FUTURE GADGET LAB · REPORT No. 004</text>
<text x="{W / 2}" y="84" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="30" fill="{INK}">On the Engineering of Yumiko Sturluson</text>
<text x="{W / 2}" y="110" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{RED}">Software engineer · Lab Mem 004</text>
{meter(W / 2, 128)}
</svg>
'''

def header(no, name):
    h = 44
    pill = 34 + 8 * len(no)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<rect x="0.5" y="9.5" width="{pill}" height="24" rx="12" fill="{TUBE}" stroke="{EDGE}"/>
<text x="{pill / 2 + 0.5}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{ORANGE}">{no}</text>
<text x="{pill + 14}" y="28" font-family="Georgia, 'Times New Roman', serif" font-size="21" fill="{RED}">{name}</text>
<line x1="{pill + 14 + 12 * len(name) + 18}" y1="22" x2="{W}" y2="22" stroke="#EFE8E4"/>
</svg>
'''

def readme():
    def hdr(key, no, name):
        return f'<img src="assets/{key}.svg" alt="{no} {name}" width="100%">'
    badges = '\n'.join(f'  <img src="https://img.shields.io/badge/{n}-{bg}?style=for-the-badge&logo={logo}&logoColor={fg}&labelColor={bg}" alt="{n}">' for n, bg, logo, fg in METHODS)
    rows = '\n'.join(f'| [{r}](https://github.com/{USER}/{r}) | {lang} |' for r, lang in RESULTS)
    s = {k: (no, name) for k, no, name in SECTIONS}
    return f'''<p align="center">
  <img src="assets/title.svg" alt="On the Engineering of Yumiko Sturluson · Software engineer · Lab Mem 004" width="100%">
</p>

{hdr('s1', *s['s1'])}

{ABSTRACT}

{hdr('s2', *s['s2'])}

<p>
{badges}
</p>

{hdr('s3', *s['s3'])}

| Specimen | Language |
| --- | --- |
{rows}

<p align="center"><sub><i>El Psy Kongroo.</i></sub></p>
'''

if __name__ == '__main__':
    a = os.path.join(ROOT, 'assets')
    os.makedirs(a, exist_ok=True)
    for f in os.listdir(a):
        os.remove(os.path.join(a, f))
    open(os.path.join(a, 'title.svg'), 'w', encoding='utf-8').write(title())
    for key, no, name in SECTIONS:
        open(os.path.join(a, f'{key}.svg'), 'w', encoding='utf-8').write(header(no, name))
    open(os.path.join(ROOT, 'README.md'), 'w', encoding='utf-8').write(readme())
    print(sorted(os.listdir(a)))
