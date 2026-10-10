import json, os, re, ssl, urllib.request
from collections import OrderedDict

USER = 'YumikoKawaii'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIMIT = 6

def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

def events():
    req = urllib.request.Request(f'https://api.github.com/users/{USER}/events/public?per_page=100', headers={'User-Agent': USER, 'Accept': 'application/vnd.github+json'})
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    return json.load(urllib.request.urlopen(req, timeout=30, context=context()))

def link(repo):
    name = repo.split('/', 1)[1] if repo.startswith(USER + '/') else repo
    return f'[{name}](https://github.com/{repo})'

def lines(evts):
    out = OrderedDict()
    for e in sorted(evts, key=lambda x: x['created_at'], reverse=True):
        day, repo, p, t = e['created_at'][:10], e['repo']['name'], e.get('payload', {}), e['type']
        if repo == f'{USER}/{USER}':
            continue
        if t == 'PushEvent':
            key = (day, 'push', repo)
            n = p.get('size') or len(p.get('commits', [])) or 1
            out[key] = out.get(key, 0) + n
        elif t == 'PullRequestEvent' and p.get('action') in ('opened', 'closed'):
            merged = p.get('action') == 'closed' and p.get('pull_request', {}).get('merged')
            if p.get('action') == 'closed' and not merged:
                continue
            out.setdefault((day, 'merged' if merged else 'opened', repo), 1)
        elif t == 'CreateEvent' and p.get('ref_type') == 'repository':
            out.setdefault((day, 'created', repo), 1)
        elif t == 'ReleaseEvent' and p.get('action') == 'published':
            out.setdefault((day, 'released', repo), 1)
    rows = []
    for (day, kind, repo), n in out.items():
        if kind == 'push':
            what = f'⚿ **sent** · pushed {n} commit{"s" if n != 1 else ""} to {link(repo)}'
        elif kind == 'merged':
            what = f'✦ **merged** · pull request in {link(repo)}'
        elif kind == 'opened':
            what = f'✧ **opened** · pull request in {link(repo)}'
        elif kind == 'created':
            what = f'◈ **created** · repository {link(repo)}'
        else:
            what = f'❖ **released** · new version of {link(repo)}'
        rows.append(f'`{day}` &nbsp; {what}  ')
        if len(rows) == LIMIT:
            break
    return rows or ['`no transmissions yet`  ']

if __name__ == '__main__':
    template = open(os.path.join(ROOT, 'README.template.md'), encoding='utf-8').read()
    readme = template.replace('{{DMAIL_LOG}}', '\n'.join(lines(events())))
    path = os.path.join(ROOT, 'README.md')
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    if old != readme:
        open(path, 'w', encoding='utf-8').write(readme)
        print('README updated')
    else:
        print('README unchanged')
