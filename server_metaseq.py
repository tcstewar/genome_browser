import swi
import os
import json
import StringIO

import pylab
import metaseq
import numpy as np

bigwigs = {}

def get_bigwig(name):
    bw = bigwigs.get(name, None)
    if bw is None:
        bw = metaseq.genomic_signal(name,'bigwig')
        bigwigs[name] = bw
    return bw

def arr2json(arr):
    return json.dumps(arr.tolist())
def json2arr(astr,dtype):
    return np.fromiter(json.loads(astr),dtype)

class Server(swi.SimpleWebInterface):
    def swi(self):
        return '<ul><li><a href="bigwigs">list of BigWig files</a></li></ul>'

    def swi_bigwigs(self):
        files = []
        for f in os.listdir('.'):
            if f.endswith('.bw'):
                files.append(f)

        items = ['<li><a href="query?name=%s&c=chr17&start=10000&end=20000">%s</a></li>' % (f, f) 
                 for f in files]

        return '<ul>%s</ul>' % ''.join(items)
        
    def swi_query(self, name, c, start, end):
        bw = get_bigwig(name)

        x, y = bw.local_coverage(c + ':' + start + '-' + end)
        combinedArray=np.column_stack((x,y))
        jsonCombinedArray=arr2json(combinedArray)

        return jsonCombinedArray

if __name__ == '__main__':
    port = 8080
    swi.browser(port)
    swi.start(Server, port=port)
