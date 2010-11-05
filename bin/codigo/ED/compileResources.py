import binascii
import os
import struct


def main(basename):
    output = os.popen('rc.exe %s.rc' % basename).read()
    if output:
        print output
    else:
        res = open(basename + '.res', 'rb')

        res.seek(0x20)

        result = []
        result.append('import binascii')
        result.append('')
        result.append('')
        result.append('def a2b(a):')
        result.append("    return binascii.a2b_hex(''.join(a.split()))")
        result.append('')
        result.append('')
        result.append('resources = {')
        while True:
            size = res.read(4)
            if len(size) == 4:
                size = struct.unpack('L', size)[0]
                res.seek(0x0A, 1)
                resourceID = struct.unpack('H', res.read(2))[0]
                res.seek(0x10, 1)
                resource = binascii.b2a_hex(res.read(size))
                result.append("             %s : a2b('''" % resourceID)
                indent = ' ' * len(result[-1])
                for i in range(0, len(resource), 32):
                    line = []
                    for j in range(i, i+32, 2):
                        if j == i + 16:
                            line.append('')
                        line.append(resource[j:j+2])
                    result.append(indent + ' '.join(line))
                result.append(indent[:-3] + "'''),")
            else:
                break
        result.append('            }')
        result.append('')
        open(basename + '.py', 'wt').write('\n'.join(result))


main('EasyDialogsResources')
