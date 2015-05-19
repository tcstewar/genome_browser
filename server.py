import swi
import os
import json
import StringIO

import matplotlib
matplotlib.use('Agg')
import pylab
import bigwig
import numpy as np

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
            params = 'name=%s&c=%s&start=%d&end=%d&count=%d' % (name, c, 0, bw.sizes[c], 100)
            part = '<li><a href="query?%s">%s</a> (length=%d) (<a href="img?%s">img</a>)</li>' % (params, c, bw.sizes[c], params)
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

    def swi_img(self, name, c, start, end, count):
        start = int(start)
        end = int(end)
        count = int(count)
        bw = get_bigwig(name)

        q = bw.query(c, start, end, count)

        img = StringIO.StringIO()
        pylab.figure()

        loc = np.linspace(start, end, count)
        mean = [x['mean'] for x in q]
        maximum = [x['max'] for x in q]
        minimum = [x['min'] for x in q]


        pylab.fill_between(loc, minimum, maximum, color='#888888')
        pylab.plot(loc, mean, color='k')
        pylab.savefig(img, dpi=80, format='png')
        return 'image/png', img.getvalue()






if __name__ == '__main__':
    port = 8080
    swi.browser(port)
    swi.start(Server, port=port)
