import swi
import os
import json

import bigwig

bigwigs = {}

def get_bigwig(name):
    bw = bigwigs.get(name, None)
    if bw is None:
        bw = bigwig.BigWig(name)
        bigwigs[name] = bw
    return bw


class Server(swi.SimpleWebInterface):
    def swi(self):
        return '<ul><li><a href="bigwigs">list of BigWig files</a></li></ul>'

    def swi_bigwigs(self):
        files = []
        for f in os.listdir('.'):
            if f.endswith('.bw'):
                files.append(f)

        items = ['<li><a href="bigwig?name=%s">%s</a></li>' % (f, f) 
                 for f in files]

        return '<ul>%s</ul>' % ''.join(items)
        
    def swi_bigwig(self, name):
        bw = get_bigwig(name)

        parts = []
        for c in sorted(bw.sizes.keys()):
            part = '<li><a href="query?name=%s&c=%s&start=%d&end=%d&count=%d">%s</a> (length=%d)</li>' % (name, c, 0, bw.sizes[c], 100, c, bw.sizes[c])
            parts.append(part)

        page = '''
<h1>%s</h1>
<h2>Parts</h2>
    <ul>%s</ul>
        ''' % (name, ''.join(parts))

        return page

    def swi_query(self, name, c, start, end, count):
        start = int(start)
        end = int(end)
        count = int(count)
        bw = get_bigwig(name)

        q = bw.query(c, start, end, count)

        return json.dumps(q)




if __name__ == '__main__':
    port = 8080
    swi.browser(port)
    swi.start(Server, port=port)
