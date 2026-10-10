import html, json, os, ssl, subprocess, urllib.request
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
USER = 'YumikoKawaii'
W = 840
RED, ORANGE, TEAL, STEEL, ROSE = '#A3222D', '#B85A0A', '#1F7A72', '#3E6390', '#A33A62'
INK, BODY, MUTED, FAINT, CREAM, RULE, EDGE, TUBE, GREEN = '#2B1D1F', '#5A2A2F', '#7A6A64', '#B8AAA4', '#FBF8F6', '#EFE8E4', '#E9C9A8', '#FFF6EC', '#237A52'
SANS = "-apple-system, 'Segoe UI', 'Hiragino Sans', 'Noto Sans JP', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Hiragino Sans', monospace"
LANG_COLORS = [RED, ORANGE, TEAL, STEEL, ROSE]
EQUIPMENT = [('Go', '#F6D9DC', '#8A1C26'), ('TypeScript', '#FDE9D6', '#8A4508'), ('Java', '#DCEFEC', '#155A54'), ('Python', '#E2E9F3', '#2E4D72'), ('Docker', '#F6D9DC', '#8A1C26')]
MEMBER = [('member', 's', 'Yumiko Sturluson', None), ('callsign', 's', USER, None), ('status', 's', 'ゆみこせかいでいちばんかわいい！', None), ('worldline', 'n', '1.048596', 'steins gate reached'), ('researching', 'l', ['Go', 'TypeScript'], None)]
FLASK = '<path d="M4.3 10h7.4l1.4 2.6a1.3 1.3 0 0 1-1.1 1.9H4a1.3 1.3 0 0 1-1.1-1.9z" fill="{c}" fill-opacity="0.28"/><path d="M6.5 1.5v4.2L2.9 12.6a1.3 1.3 0 0 0 1.1 1.9h8a1.3 1.3 0 0 0 1.1-1.9L9.5 5.7V1.5M5.5 1.5h5" fill="none" stroke="{c}" stroke-linejoin="round" stroke-linecap="round"/><circle cx="7" cy="11.8" r="0.8" fill="{c}"/><circle cx="9.4" cy="12.6" r="0.55" fill="{c}"/>'

def esc(s):
    return html.escape(str(s), quote=True)

def token():
    t = os.environ.get('GITHUB_TOKEN')
    if t:
        return t
    return subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True).stdout.strip()

def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={'User-Agent': USER, 'Authorization': f'Bearer {token()}', 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(req, timeout=30, context=context()))

def stats():
    q = '''query($login: String!) { user(login: $login) {
      followers { totalCount }
      pullRequests { totalCount }
      contributionsCollection { totalCommitContributions }
      repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
        totalCount
        nodes { name languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
      } } }'''
    u = api('https://api.github.com/graphql', {'query': q, 'variables': {'login': USER}})['data']['user']
    langs = Counter()
    for r in u['repositories']['nodes']:
        if r['name'] == USER:
            continue
        for e in r['languages']['edges']:
            langs[e['node']['name']] += e['size']
    return {
        'repos': u['repositories']['totalCount'],
        'commits': u['contributionsCollection']['totalCommitContributions'],
        'prs': u['pullRequests']['totalCount'],
        'followers': u['followers']['totalCount'],
        'langs': langs,
    }

def activity(limit=5):
    out = OrderedDict()
    for e in sorted(api(f'https://api.github.com/users/{USER}/events/public?per_page=100'), key=lambda x: x['created_at'], reverse=True):
        day, repo, p, t = e['created_at'][:10], e['repo']['name'], e.get('payload', {}), e['type']
        if repo == f'{USER}/{USER}':
            continue
        name = repo.split('/', 1)[1] if repo.startswith(USER + '/') else repo
        if t == 'PushEvent':
            k = (day, 'sent', name)
            out[k] = out.get(k, 0) + (p.get('size') or len(p.get('commits', [])) or 1)
        elif t == 'PullRequestEvent' and p.get('action') == 'closed' and p.get('pull_request', {}).get('merged'):
            out.setdefault((day, 'merged', name), 1)
        elif t == 'PullRequestEvent' and p.get('action') == 'opened':
            out.setdefault((day, 'opened', name), 1)
        elif t == 'CreateEvent' and p.get('ref_type') == 'repository':
            out.setdefault((day, 'created', name), 1)
        elif t == 'ReleaseEvent' and p.get('action') == 'published':
            out.setdefault((day, 'released', name), 1)
    rows = []
    for (day, kind, name), n in out.items():
        rows.append((day, kind, name, n))
        if len(rows) == limit:
            break
    return rows

def svg(h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">{body}</svg>\n'

def heading(title, y=22):
    return (f'<text x="0" y="{y}" font-family="{SANS}" font-size="18" font-weight="600" fill="{RED}">{esc(title)}</text>'
            f'<line x1="0" y1="{y + 12}" x2="{W}" y2="{y + 12}" stroke="{RULE}"/>')

def banner():
    digits, tw, th, gap, dw = '1.048596', 46, 74, 8, 14
    total = sum(dw if c == '.' else tw for c in digits) + gap * (len(digits) - 1)
    x, y, parts = (W - total) / 2, 30, []
    for c in digits:
        if c == '.':
            parts.append(f'<circle cx="{x + dw / 2:.1f}" cy="{y + th - 10}" r="3.8" fill="{ORANGE}"/>')
            x += dw + gap
            continue
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="23" fill="{TUBE}" stroke="{EDGE}" stroke-width="1.2"/>')
        parts.append(f'<text x="{x + tw / 2:.1f}" y="{y + th / 2 + 13}" text-anchor="middle" font-family="{MONO}" font-size="38" fill="{ORANGE}">{c}</text>')
        x += tw + gap
    h = 210
    return svg(h, f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="{CREAM}" stroke="{RULE}"/>{"".join(parts)}'
                  f'<text x="{W / 2}" y="152" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="600" fill="{INK}">Yumiko Sturluson</text>'
                  f'<text x="{W / 2}" y="182" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{MUTED}">Lab Mem 004 · Future Gadget Lab</text>')

def member():
    top, lh, pad = 50, 26, 20
    h = top + pad * 2 + lh * len(MEMBER) - 6
    lines = []
    for i, (k, kind, v, comment) in enumerate(MEMBER):
        y = top + pad + 12 + i * lh
        if kind == 's':
            val = f'<tspan fill="{GREEN}">"{esc(v)}"</tspan>'
        elif kind == 'n':
            val = f'<tspan fill="{ORANGE}">{esc(v)}</tspan>'
        else:
            val = f'<tspan fill="{BODY}">[</tspan>' + f'<tspan fill="{BODY}">, </tspan>'.join(f'<tspan fill="{GREEN}">"{esc(x)}"</tspan>' for x in v) + f'<tspan fill="{BODY}">]</tspan>'
        cm = f'<tspan fill="{MUTED}" font-style="italic">  # {esc(comment)}</tspan>' if comment else ''
        lines.append(f'<text x="22" y="{y}" font-family="{MONO}" font-size="15" xml:space="preserve"><tspan fill="{RED}">{k}</tspan><tspan fill="{BODY}">: </tspan>{val}{cm}</text>')
    return svg(h, heading('Lab member file') + f'<rect x="0" y="{top}" width="{W}" height="{h - top}" rx="10" fill="{CREAM}"/>' + ''.join(lines))

def results(s):
    top, ch, gap = 50, 168, 16
    cw = (W - gap) / 2
    h = top + ch
    rows = [('Public repositories', s['repos']), ('Commits (last year)', s['commits']), ('Pull requests', s['prs']), ('Followers', s['followers'])]
    c1 = [f'<rect x="0.5" y="{top + 0.5}" width="{cw - 1}" height="{ch - 1}" rx="12" fill="#FFFDFC" stroke="{RULE}"/>',
          f'<g transform="translate(18 {top + 16})">{FLASK.format(c=ORANGE)}</g>',
          f'<text x="42" y="{top + 29}" font-family="{SANS}" font-size="15" font-weight="600" fill="{RED}">Lab statistics</text>']
    for i, (k, v) in enumerate(rows):
        y = top + 62 + i * 26
        c1.append(f'<text x="18" y="{y}" font-family="{SANS}" font-size="14" fill="{BODY}">{k}</text>')
        c1.append(f'<text x="{cw - 18}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="14" font-weight="600" fill="{INK}">{v:,}</text>')
    x0 = cw + gap
    total = sum(s['langs'].values()) or 1
    top4 = s['langs'].most_common(4)
    parts = [(n, v / total) for n, v in top4]
    rest = 1 - sum(p for _, p in parts)
    if rest > 0.005:
        parts.append(('Other', rest))
    c2 = [f'<rect x="{x0 + 0.5}" y="{top + 0.5}" width="{cw - 1}" height="{ch - 1}" rx="12" fill="#FFFDFC" stroke="{RULE}"/>',
          f'<text x="{x0 + 18}" y="{top + 29}" font-family="{MONO}" font-size="14" fill="{ORANGE}">&lt;/&gt;</text>',
          f'<text x="{x0 + 50}" y="{top + 29}" font-family="{SANS}" font-size="15" font-weight="600" fill="{RED}">Most used languages</text>',
          f'<clipPath id="bar"><rect x="{x0 + 18}" y="{top + 48}" width="{cw - 36}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">']
    bx = x0 + 18
    for i, (n, p) in enumerate(parts):
        bw = (cw - 36) * p
        c2.append(f'<rect x="{bx:.2f}" y="{top + 48}" width="{bw + 0.5:.2f}" height="10" fill="{LANG_COLORS[i % len(LANG_COLORS)]}"/>')
        bx += bw
    c2.append('</g>')
    for i, (n, p) in enumerate(parts):
        col, row = i % 2, i // 2
        x, y = x0 + 18 + col * (cw - 36) / 2, top + 86 + row * 26
        c2.append(f'<circle cx="{x + 5}" cy="{y - 5}" r="5" fill="{LANG_COLORS[i % len(LANG_COLORS)]}"/>')
        c2.append(f'<text x="{x + 16}" y="{y}" font-family="{SANS}" font-size="14" fill="{BODY}">{esc(n)} <tspan fill="{MUTED}">{p * 100:.1f}%</tspan></text>')
    return svg(h, heading('Experiment results') + ''.join(c1) + ''.join(c2))

def equipment():
    top, ph = 50, 32
    x, parts = 0, []
    for name, bg, fg in EQUIPMENT:
        w = 28 + len(name) * 8.4
        parts.append(f'<rect x="{x}" y="{top}" width="{w:.1f}" height="{ph}" rx="16" fill="{bg}"/>')
        parts.append(f'<text x="{x + w / 2:.1f}" y="{top + 21}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{fg}">{esc(name)}</text>')
        x += w + 10
    return svg(top + ph + 4, heading('Lab equipment') + ''.join(parts))

def dmail(rows):
    top, lh = 56, 28
    kinds = {'sent': ('⚿', RED, 'pushed {n} commit{s} to'), 'merged': ('✦', ORANGE, 'merged a pull request in'),
             'opened': ('✧', ROSE, 'opened a pull request in'), 'created': ('◈', TEAL, 'created repository'), 'released': ('❖', STEEL, 'released a new version of')}
    parts = []
    for i, (day, kind, name, n) in enumerate(rows):
        y = top + 14 + i * lh
        sym, col, verb = kinds[kind]
        verb = verb.format(n=n, s='s' if n != 1 else '')
        parts.append(f'<text x="0" y="{y}" font-family="{MONO}" font-size="14" fill="{FAINT}">{day}</text>')
        parts.append(f'<text x="112" y="{y}" font-family="{MONO}" font-size="14" fill="{col}">{sym} {kind}</text>')
        parts.append(f'<text x="212" y="{y}" font-family="{MONO}" font-size="14" fill="{BODY}">{esc(verb)} <tspan fill="{STEEL}">{esc(name)}</tspan></text>')
    if not rows:
        parts.append(f'<text x="0" y="{top + 14}" font-family="{MONO}" font-size="14" fill="{FAINT}">no transmissions yet</text>')
    h = top + max(1, len(rows)) * lh
    return svg(h, heading('D-mail log') + ''.join(parts))

def footer():
    tw = 128
    x = (W - tw - 22) / 2
    return svg(34, f'<g transform="translate({x:.1f} 9)">{FLASK.format(c=ORANGE)}</g>'
                   f'<text x="{x + 24:.1f}" y="22" font-family="Georgia, serif" font-style="italic" font-size="15" fill="{RED}">El Psy Kongroo.</text>')

README = '''<p align="center"><img src="assets/banner.svg" alt="1.048596 · Yumiko Sturluson · Lab Mem 004 · Future Gadget Lab" width="100%"></p>

<p><img src="assets/member.svg" alt="Lab member file: Yumiko Sturluson, YumikoKawaii, Go and TypeScript" width="100%"></p>

<p><img src="assets/results.svg" alt="Lab statistics and most used languages" width="100%"></p>

<p><img src="assets/equipment.svg" alt="Lab equipment: Go, TypeScript, Java, Python, Docker" width="100%"></p>

<p><a href="https://github.com/YumikoKawaii?tab=repositories"><img src="assets/dmail.svg" alt="D-mail log: recent public activity" width="100%"></a></p>

<p align="center"><img src="assets/footer.svg" alt="El Psy Kongroo." width="100%"></p>
'''

def write(name, text):
    path = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
    if old != text:
        open(path, 'w', encoding='utf-8').write(text)
        return True
    return False

if __name__ == '__main__':
    s = stats()
    changed = [n for n, t in [
        ('assets/banner.svg', banner()), ('assets/member.svg', member()), ('assets/results.svg', results(s)),
        ('assets/equipment.svg', equipment()), ('assets/dmail.svg', dmail(activity())), ('assets/footer.svg', footer()), ('README.md', README),
    ] if write(n, t)]
    print('changed:', changed or 'nothing')
