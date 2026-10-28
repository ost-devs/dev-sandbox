"""Offline tests for fetch_mirrors.py, run as the CLI it is. Local git repositories and local HTTP servers
stand in for GitHub, documentation sites and blogs, so the tests take seconds and never depend on a site.

  python3 -m unittest discover -s utils/skills/mirrors/tests -v

Web tests need Defuddle (npm ci --prefix utils/skills/mirrors --ignore-scripts); without it they are skipped.
"""
import http.server, json, os, pathlib, shutil, subprocess, sys, tempfile, threading, time, unittest

SKILL = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = SKILL / 'fetch_mirrors.py'
sys.path.insert(0, str(SKILL))
import fetch_web   # noqa: E402  (only to find Defuddle)

try:
    fetch_web.defuddle()
    HAVE_DEFUDDLE = True
except SystemExit:
    HAVE_DEFUDDLE = False

GIT_ENV = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t', 'GIT_COMMITTER_NAME': 't',
           'GIT_COMMITTER_EMAIL': 't@t', 'GIT_CONFIG_GLOBAL': '/dev/null'}


def git(*a, cwd):
    return subprocess.run(['git', *a], cwd=cwd, check=True, capture_output=True, text=True,
                          env={**os.environ, **GIT_ENV}).stdout.strip()


def commit(repo, files, msg):
    for name, text in files.items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if text.startswith('symlink:'):
            p.symlink_to(text[len('symlink:'):])
        else:
            p.write_text(text)
    git('add', '-A', cwd=repo)
    git('commit', '-qm', msg, cwd=repo)
    return git('rev-parse', 'HEAD', cwd=repo)


def new_repo(path):
    path.mkdir(parents=True)
    git('init', '-q', '-b', 'main', cwd=path)
    git('config', 'uploadpack.allowFilter', 'true', cwd=path)
    git('config', 'uploadpack.allowAnySHA1InWant', 'true', cwd=path)
    return path


class Server:
    """A local site: routes map a path to (status, headers, body); hits counts requests per path."""

    def __init__(self):
        self.routes, self.hits = {}, {}
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split('?')[0]
                owner.hits[path] = owner.hits.get(path, 0) + 1
                status, headers, body = owner.routes.get(path, (404, {'Content-Type': 'text/html'}, b'no'))
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v.replace('{base}', owner.base))
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass
        self.httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.base = f'http://127.0.0.1:{self.httpd.server_port}'
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def page(self, path, body, ctype='text/html; charset=utf-8', status=200, **headers):
        self.routes[path] = (status, {'Content-Type': ctype, **headers}, body.replace('{base}', self.base).encode())

    def redirect(self, path, to):
        self.routes[path] = (302, {'Location': to}, b'')

    def total(self):
        return sum(self.hits.values())

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.proj = self.tmp / 'proj'
        self.proj.mkdir()

    def tearDown(self):
        for d, _, _ in os.walk(self.tmp):
            os.chmod(d, 0o755)
        shutil.rmtree(self.tmp)

    def run_cli(self, *args, ok=True):
        r = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.proj, capture_output=True, text=True,
                           env={**os.environ, **GIT_ENV, 'MIRRORS_PAUSE': '0', 'no_proxy': '*'})
        out = r.stdout + r.stderr
        if ok is not None:
            self.assertEqual(r.returncode == 0, ok, out)
        return out

    def manifest(self):
        return json.loads((self.proj / 'mirrors' / 'mirrors.json').read_text())['mirrors']

    def commit_proj(self, files):
        if not (self.proj / '.git').exists():
            git('init', '-q', cwd=self.proj)
        commit(self.proj, files, 'docs')
        time.sleep(1.1)   # page "changed" times must come after the commit time (seconds)


class GitMirrors(Base):
    def setUp(self):
        super().setUp()
        lib = new_repo(self.tmp / 'lib')
        self.c1 = commit(lib, {'package.json': '{"version": "1.0.0"}', 'LICENSE': 'MIT', 'src/a.txt': 'a'}, 'c1')
        git('tag', '1.0.0', cwd=lib)
        self.c2 = commit(lib, {'package.json': '{"version": "1.1.0"}'}, 'c2')
        git('tag', '-a', 'v1.1.0', '-m', 'release', cwd=lib)
        self.c3 = commit(lib, {'src/b.txt': 'after the release',
                               'evil': 'symlink:/etc/passwd', 'ok': 'symlink:src/a.txt'}, 'c3')
        self.lib = f'file://{lib}'
        for m in ('one', 'two'):
            commit(new_repo(self.tmp / 'set' / m), {'README': m}, 'init')
        self.set = f'file://{self.tmp}/set/{{member}}'

    def test_gitignore_created_without_git(self):
        (self.proj / '.gitignore').write_text('\n')
        self.run_cli('--list')
        self.assertEqual((self.proj / '.gitignore').read_text(),
                         '# mirrors skill: copies ignored, manifest versioned\n/mirrors/*\n!/mirrors/mirrors.json\n')
        self.run_cli('--list')
        self.assertEqual((self.proj / '.gitignore').read_text().count('/mirrors/*'), 1)

    def test_gitignore_override_warns(self):
        git('init', '-q', cwd=self.proj)
        (self.proj / '.gitignore').write_text('mirrors/\n')
        self.assertIn('another rule overrides', self.run_cli('--list'))

    def test_add_is_pinned_read_only_without_git(self):
        self.run_cli('--add', 'lib', self.lib, '--license', 'MIT')
        copy = self.proj / 'mirrors' / 'lib'
        self.assertEqual(self.manifest()['lib']['commit'], self.c3)
        self.assertEqual((copy / '.mirror-commit').read_text().strip(), self.c3)
        self.assertFalse((copy / '.git').exists())
        self.assertFalse(os.access(copy / 'src' / 'a.txt', os.W_OK))
        self.assertFalse((copy / 'evil').is_symlink(), 'a link out of the copy must be dropped')
        self.assertTrue((copy / 'ok').is_symlink(), 'a link inside the copy stays')

    def test_pin_published_version(self):
        self.run_cli('--add', 'lib', self.lib)
        self.run_cli('--pin', 'lib', '@1.0.0')
        self.assertEqual(self.manifest()['lib']['commit'], self.c1)
        self.run_cli('--pin', 'lib', '@1.1.0')   # annotated tag with a "v": peeled to the commit
        self.assertEqual(self.manifest()['lib'], {**self.manifest()['lib'], 'ref': 'refs/tags/v1.1.0', 'commit': self.c2})
        self.run_cli('--pin', 'lib', '@package')
        self.assertEqual(self.manifest()['lib']['commit'], self.c2)
        self.assertIn('no tag 9.9.9 or v9.9.9', self.run_cli('--pin', 'lib', '@9.9.9', ok=False))

    def test_check_notes_commit_after_release(self):
        self.run_cli('--add', 'lib', self.lib)
        self.assertIn('not the release commit of 1.1.0', self.run_cli('--check'))

    def test_set_members_in_batch(self):
        self.run_cli('--add', 's', self.set)
        self.run_cli('--follow', 's/one', 's/two')
        members = self.manifest()['s']['members']
        self.assertTrue(all(m.get('follow') for m in members.values()))
        self.assertTrue((self.proj / 'mirrors' / 's' / 'two' / 'README').exists())
        self.run_cli('--pin', 's')
        members = self.manifest()['s']['members']
        self.assertTrue(all('commit' in m and 'follow' not in m for m in members.values()))
        self.assertIn('ok       s/two', self.run_cli('--check'))

    def test_remove(self):
        self.run_cli('--add', 'lib', self.lib)
        self.run_cli('--remove', 'lib')
        self.assertNotIn('lib', self.manifest())
        self.assertFalse((self.proj / 'mirrors' / 'lib').exists())


class PagesMirrors(Base):
    def setUp(self):
        super().setUp()
        self.site, self.other = Server(), Server()
        self.site.page('/docs/llms.txt', '# Docs\n- [A]({base}/docs/en/a.md): a\n- [B]({base}/docs/en/b.md): b\n'
                       '- [Moved]({base}/docs/en/moved.md): moved\n- [FR]({base}/docs/fr/a.md): fr\n', 'text/plain')
        self.site.page('/docs/en/a.md', '# A\n', 'text/markdown')
        self.site.page('/docs/en/b.md', '# B\n', 'text/markdown')
        self.site.page('/docs/fr/a.md', '# A fr\n', 'text/markdown')
        self.site.routes['/docs/en/moved.md'] = (307, {'Location': self.other.base + '/x'}, b'')
        self.other.page('/x', '<html>changes every time</html>')
        self.url = self.site.base + '/docs/llms.txt'

    def tearDown(self):
        self.site.close()
        self.other.close()
        super().tearDown()

    def test_pages_change_and_stale(self):
        out = self.run_cli('--add', 'd', self.url, '--include', 'en')
        self.assertIn('redirects off the site', out)
        copy = self.proj / 'mirrors' / 'd'
        self.assertEqual(sorted(p.name for p in (copy / 'en').iterdir()), ['a.md', 'b.md'])
        self.assertFalse((copy / 'fr').exists(), '--include en')
        self.assertIn('ok       d (2 pages)', self.run_cli('--check'))
        self.commit_proj({'docs/guide.md': f'Base: {self.site.base}/docs/en/b#part\n',
                          'docs/other.md': 'Base: mirrors/d/en/a.md\n'})
        self.site.page('/docs/en/b.md', '# B, new\n', 'text/markdown')
        self.assertIn('outdated', self.run_cli('--check', ok=False))
        self.assertIn('changed  en/b.md', self.run_cli())
        out = self.run_cli('--stale', 'd', 'docs', ok=False)
        self.assertIn('docs/guide.md: en/b.md', out)
        self.assertNotIn('other.md', out)

    def test_max_age_skips_the_download(self):
        self.run_cli('--add', 'd', self.url, '--include', 'en')
        before = self.site.total()
        self.assertIn('fresh', self.run_cli('--max-age', '24'))
        self.assertEqual(self.site.total(), before)
        self.run_cli('--refresh')
        self.assertGreater(self.site.total(), before)

    def test_pin_refused(self):
        self.run_cli('--add', 'd', self.url, '--include', 'en')
        self.assertIn('no commits', self.run_cli('--pin', 'd', ok=False))


ARTICLE = '''<!doctype html><html lang="en"><head><title>{title}</title>
<meta property="og:url" content="{base}{path}"><meta property="article:modified_time" content="2026-01-02">
</head><body><nav><a href="/menu">Menu</a> <a href="/blog/nav-only">Nav</a></nav>
<article><h1>{title}</h1>{paras}</article>
<aside><h2>Related</h2><ul><li><a href="/blog/related-only">Related</a></li></ul></aside>
<footer><a href="/footer-only">Footer</a></footer></body></html>'''
FILLER = ('This paragraph explains the topic in enough words for an extractor to treat it as the main '
          'content of the page, with details, examples and a conclusion that readers can follow. ')


def article(path, title, links, extra=''):
    paras = ''.join(f'<p>{FILLER * 3} See <a href="{href}">{text}</a> for more. {FILLER}</p>' for href, text in links)
    return path, ARTICLE.format(title=title + extra, paras=paras + f'<p>{FILLER * 4}</p>', base='{base}', path=path)


@unittest.skipUnless(HAVE_DEFUDDLE, 'Defuddle not installed: npm ci --prefix utils/skills/mirrors --ignore-scripts')
class WebMirrors(Base):
    def setUp(self):
        super().setUp()
        self.site, self.other = Server(), Server()
        s = self.site
        s.routes['/robots.txt'] = (403, {'Content-Type': 'text/plain'}, b'forbidden')   # 4xx: no rules
        s.page(*article('/blog/a', 'Article A', [('/blog/b', 'b'), ('/blog/c', 'c'), (self.other.base + '/elsewhere', 'out')]))
        s.page(*article('/blog/b', 'Article B', [('/blog/a', 'back to a'), ('/blog/c/', 'c with slash')]))
        s.page(*article('/blog/c', 'Article C', [('/img.png', 'image'), ('/blog/missing', 'missing'),
                                                 ('/blog/loop', 'loop'), ('/blog/a?utm_source=x#top', 'a again')]))
        s.page('/img.png', 'PNG', 'image/png')
        s.redirect('/blog/loop', '/blog/loop')
        s.redirect('/blog/short', '/blog/b')
        self.other.page('/robots.txt', 'User-agent: *\nDisallow: /private\n', 'text/plain')
        self.other.page(*article('/private', 'Private', []))

    def tearDown(self):
        self.site.close()
        self.other.close()
        super().tearDown()

    def copy(self):
        return sorted(str(p.relative_to(self.proj / 'mirrors' / 'w')) for p in (self.proj / 'mirrors' / 'w').rglob('*.md'))

    def test_chain_without_loops_or_noise(self):
        out = self.run_cli('--add', 'w', self.site.base + '/blog/a', '--web', '--depth', '5')
        host = '127.0.0.1_' + str(self.site.httpd.server_port)
        self.assertEqual([p.replace(host, 'H').replace(f'127.0.0.1:{self.site.httpd.server_port}', 'H')
                          for p in self.copy()], ['H/blog/a.md', 'H/blog/b.md', 'H/blog/c.md'])
        urls = self.manifest()['w']['urls']
        self.assertEqual(len(urls), len(set(urls)))
        for reason in ('not HTML (image/png)', 'HTTP 404', 'redirect error'):
            self.assertIn(reason, out)
        for path in ('/blog/related-only', '/blog/nav-only', '/footer-only', '/menu'):
            self.assertNotIn(path, self.site.hits, 'only links inside the article text are followed')
        self.assertEqual(self.other.total(), 0, 'links to other sites are not followed')
        text = (self.proj / 'mirrors' / 'w').rglob('a.md').__next__().read_text()
        self.assertIn('source: "' + self.site.base + '/blog/a"', text)
        self.assertIn('modified: "2026-01-02"', text)
        self.assertIn(self.other.base + '/elsewhere', self.run_cli('--links', 'w'))

    def test_same_page_other_spelling_and_redirect(self):
        self.run_cli('--add', 'w', self.site.base + '/blog/b', '--web')
        before = self.site.hits.get('/blog/b', 0)
        self.assertIn('already', self.run_cli('--add', 'w', self.site.base + '/blog/b/?utm_source=x#top', '--web'))
        self.assertEqual(self.site.hits.get('/blog/b', 0), before)
        self.run_cli('--add', 'w', self.site.base + '/blog/short', '--web')   # redirects to b
        self.assertEqual(len(self.manifest()['w']['urls']), 1)

    def test_max_pages_and_resume(self):
        out = self.run_cli('--add', 'w', self.site.base + '/blog/a', '--web', '--depth', '5', '--max-pages', '2')
        self.assertIn('stopped  at --max-pages 2', out)
        self.assertEqual(len(self.copy()), 2)
        self.run_cli('--add', 'w', self.site.base + '/blog/a', '--web', '--depth', '5')
        self.assertEqual(len(self.copy()), 3)

    def test_robots_disallow(self):
        out = self.run_cli('--add', 'w', self.other.base + '/private', '--web')
        self.assertIn('robots.txt disallows it', out)

    def test_snapshot_refresh_restore_and_stale(self):
        self.run_cli('--add', 'w', self.site.base + '/blog/a', '--web', '--depth', '1')
        before = self.site.total()
        self.assertIn('ok       w (3 page(s))', self.run_cli())
        self.assertEqual(self.site.total(), before, 'a plain fetch does not download snapshots again')
        b = next((self.proj / 'mirrors' / 'w').rglob('b.md'))
        os.chmod(b.parent, 0o755)
        b.unlink()
        self.assertIn('missing', self.run_cli('--check', ok=False))
        self.assertIn('restored', self.run_cli())
        self.assertNotIn('changed', self.run_cli('--refresh'))
        self.commit_proj({'notes/n.md': f'From {self.site.base}/blog/b and {self.site.base}/blog/c\n'})
        self.site.page(*article('/blog/b', 'Article B', [('/blog/a', 'back to a')], extra=' (updated)'))
        self.assertIn('changed', self.run_cli('--refresh'))
        out = self.run_cli('--stale', 'w', 'notes', ok=False)
        self.assertIn('notes/n.md', out)
        self.assertIn('blog/b.md', out)
        self.assertNotIn('blog/c.md', out)


if __name__ == '__main__':
    unittest.main()
