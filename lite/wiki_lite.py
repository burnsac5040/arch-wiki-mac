#! /usr/bin/env python3

import os, re, gzip

"""
Convert the html to flat text.
Compress files where appropriate.
This should be using a real html parser,
but input is safe/known and there is a lot to parse.
"""
wiki_path = '/usr/share/doc/arch-wiki/html/'
dump_path = './wiki/'

# not a complete list, but does cover the current wiki
escapes = [('&nbsp;',  ' '),
           ('&quot;',  '"'),
           ('&gt;',    '>'),
           ('&lt;',    '<'),
           ('&#34;',   '"'),
           ('&#36;',   "$"),
           ('&#39;',   "'"),
           ('&#40;',   '('),
           ('&#41;',   ')'),
           ('&#60;',   '<'),
           ('&#61;',   '='),
           ('&#x3d;',  '='),  # crazy russians
           ('&#62;',   '>'),
           ('&#91;',   '['),
           ('&#93;',   ']'),
           ('&#123;',  '{'),
           ('&#125;',  '}'),
           ('&#124;',  '|'),
           ('&#135;',  '‡'),
           ('&#160;',  ' '),
           ('&#163;',  '£'),
           ('&#167;',  '§'),
           ('&#176;',  '°'),
           ('&#180;',  '´'),
           ('&#200;',  'È'),
           ('&#224;',  'à'),
           ('&#225;',  'á'),
           ('&#227;',  'ã'),
           ('&#231;',  'ç'),
           ('&#232;',  'è'),
           ('&#233;',  'é'),
           ('&#234;',  'ê'),
           ('&#235;',  'ë'),
           ('&#236;',  'ì'),
           ('&#242;',  'ò'),
           ('&#245;',  'õ'),
           ('&#249;',  'ù'),
           ('&#8592;', '←'),
           ('&#8593;', '↑'),
           ('&#8594;', '→'),
           ('&#8595;', '↓'),
           ('&#8657;', '⇑'),
           ('&#9484;', '┌'),
           ('&#9492;', '└'),
           ('&#9608;', '█'),
           ('&#10003;', '✓'),
           ('&#10007;', '✗'),
           ('&#x103;', 'ă'),
           ('&#x15f;', 'ş'),
           ('&#x219;', 'ș'),
           ('&#x21b;', 'ț'),
           ('&#226;', 'â'),
           ('&#228;', 'ä'),
           ('&#238;', 'î'),
           # and now a bunch that are normally unicode
           ('&lsquo;', "'"),
           ('&rsquo;', "'"),
           ('&#166;',  '|'),
           ('&#169;',  '(c)'),
           ('&#173;',  ''),
           ('&#174;',  '(r)'),
           ('&#187;',  '>>'),
           ('&#8211;', '-'),
           ('&#8212;', '--'),
           ('&#8216;', "'"),
           ('&#8217;', "'"),
           ('&#8220;', '"'),
           ('&#8221;', '"'),
           ('&#8226;', '*'),
           ('&#8230;', '...'),
           ('&#8482;', '(tm)'),
           ('&#9472;', '-'),
           ('&#9596;', '-'),
           ('&#8202;', ' '),
           ('&#8206;', ''),  # looks correct
           # cute junk that should not be in the wiki
           ('&#x1f50e;', ''),
           # do these last to avoid breakage
           ('&#35;',   '#'),
           ('&amp;',   '&'),
          ]

def remove_tags(html):
    flags = re.DOTALL | re.MULTILINE
    #body = re.compile('^<body class.*?^NewPP limit report$', flags)
    #body = re.compile('^<body class="mediawiki.*?"site":"loading","user":"ready","user.groups":"ready"', flags)
    body = re.compile('^<body class="mediawiki.*?<li id="footer-info-copyright">', flags)
    html = body.findall(html)[0]
    html = '\n'.join(html.split('\n')[:-1])
    toc  = re.compile('^<div class="toc noprint" style="text-align: center; margin-bottom: 1em">.*?</div>$', flags)
    html = re.sub(toc, '', html)
    js   = 'if (window.showTocToggle) { var tocShowText = "show"; var tocHideText = "hide"; showTocToggle(); }'
    html = html.replace(js, '')
    jump = re.compile('<div id="jump-to-nav".*?</div>$', flags)
    html = re.sub(jump, '', html)
    link_open = re.compile('<a.*?>')
    html = re.sub(link_open, '@@b', html)
    html = html.replace('</a>', '@@w')
    tags  = re.compile('<.*?>')
    html = re.sub(tags, '', html)
    return html

def remove_escapes(text):
    for a,b in escapes:
        text = text.replace(a, b)
    return text

def html_to_text(html):
    return remove_escapes(remove_tags(html))

def all_html_paths(path):
    for root,dirs,files in os.walk(path):
        for f in files:
            if not f.endswith('html'):
                continue
            yield os.path.join(root, f)

def generate_toc():
    toc = {}
    for i, path in enumerate(all_html_paths(wiki_path), 1):
        number = '%08i' % i
        toc[number] = path
        toc[path] = number
    return toc

def main():
    print('This should take around a minute.')
    if os.path.isdir(dump_path):
        [os.remove(dump_path + p) for p in os.listdir(dump_path)]
    else:
        os.makedirs(dump_path)
    toc = generate_toc()
    toc_file = open(dump_path + 'index', 'w')
    txt_file = gzip.open(dump_path + 'arch-wiki.txt.gz', 'w')
    escape_regex = re.compile('&#x?[0-9A-Fa-f]+;')
    for path in all_html_paths(wiki_path):
        if path == 'index.html':
            continue
        html = open(path).read()
        if not html:
            print('warning, empty file:', path)
            continue
        try:
            name = path[len(wiki_path):-5]
            number = toc[path]
            text = html_to_text(html)
            toc_file.write('%s %s\n' % (name, number))
            text = re.sub(re.compile('^', re.MULTILINE), number+':', text)
            if '&#' in text:
                print('warning, escape sequence:', path)
                found = set(re.findall(escape_regex, text))
                known = set(list(zip(*escapes))[0])
                if found:
                    print('    all:', found)
                if found - known:
                    print('    new:', found - known)
                    print(text)
                    raise KeyboardInterrupt
                else:
                    print('    intentional?')
            txt_file.write(bytes(text + '\n', 'UTF-8'))
        except KeyboardInterrupt:
            raise
        except:
            print('error parsing', path)
            raise
    toc_file.close()
    txt_file.close()

if __name__ == '__main__':
    main()

