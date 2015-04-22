import os
import struct

from bx.bbi.bigwig_file import BigWigFile

class BigWig(object):
    def __init__(self, filename):
        self.filename = filename
        self.determine_sizes()
        self.bwf = BigWigFile(open(filename))

    def determine_sizes(self):
        self.sizes = {}
        fh = open(self.filename, "rb")
        # read magic number to guess endianness
        magic = fh.read(4)
        if magic == '&\xfc\x8f\x88':
            endianness = '<'
        elif magic == '\x88\x8f\xfc&':
            endianness = '>'
        else:
            raise IOError("The file is not in bigwig format")

        # read the header
        info = struct.unpack(endianness + 'HHQQQHHQQIQ', fh.read(60))
        self.version = info[0]
        self.zoom_levels = info[1]
        self.chromosome_tree_offset = info[2]
        self.full_data_offset = info[3]
        self.full_index_offset = info[4]
        self.field_count = info[5]
        self.defined_field_count = info[6]
        self.auto_SQL_offset = info[7]
        self.total_summary_offset = info[8]
        self.uncompress_buf_size = info[9]
        
        # go to the data
        fh.seek(self.chromosome_tree_offset)
        # read magic again
        magic = fh.read(4)
        if magic == '\x91\x8c\xcax':
            endianness = '<'
        elif magic == 'x\xca\x8c\x91':
            endianness = '>'
        else:
            raise ValueError("Wrong magic for this bigwig data file")

        info2 = struct.unpack(endianness + 'IIIQQ', fh.read(28))
        self.block_size = info2[0]
        self.key_size = info2[1]
        self.val_size = info2[2]
        self.item_count = info2[3]

        info3 = struct.unpack(endianness + 'BBH', fh.read(4))
        self.is_leaf = info3[0]
        self.count = info3[2]

        for n in range(self.count):
            format_code = endianness + str(self.key_size) + 'sII'
            info = struct.unpack(format_code, fh.read(self.key_size + 2 * 4))
            key, chrom_id, chrom_size = info

            key = key.replace('\x00', '')
            self.sizes[key] = chrom_size

    def get_as_array(self, chrom, start, end):
        return self.bwf.get_as_array(chrom, start, end)

    def get(self, chrom, start, end):
        return self.bwf.get(chrom, start, end)

    def query(self, chrom, start, end, number):
        return self.bwf.query(chrom, start, end, number)




if __name__ == '__main__':
    bw = BigWig('Npas4_Npas4_KCl_B1_E120.bw')
    print bw.sizes
    print bw.zoom_levels

    data = bw.get_as_array('chrX',bw.sizes['chrX']/2, bw.sizes['chrX']/2 + 10000)
    data2 = bw.get('chrX',bw.sizes['chrX']/2, bw.sizes['chrX']/2 + 10000)
    #print data2
    q = bw.query('chrX',bw.sizes['chrX']/2, bw.sizes['chrX']/2 + 10000, 20)
    print q

    import pylab
    pylab.plot(data)
    pylab.show()

