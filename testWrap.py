__author__ = 'x37liu'
from wrapper import Cipher
def test():
    ci = Cipher()
    # key, count, direct, bearer, data
    output = ci.IP('5ead1f52e92ced3add9486d1b066c693', 0x00, 'uplink', 0, '0010101010')
    print "A: " + str(output == 'c76c5132')

    output = ci.encrypt('941c08ca34df130ee7644ef803b90eda', 0x00, 'uplink', 0, '10101010c76c5132')
    print "B: " + str(output == 'ad1d7e855d13fbd6')

    output = ci.decrypt('0x941c08ca34df130ee7644ef803b90eda', 0x00, 'uplink', 0, 'ad1d7e855d13fbd6')
    print "C: " + str(output == '10101010c76c5132')

    output = ci.encrypt('0xa24fd61d0b627b91f7451be11df4d40e', 0x1C3, 'downlink', 0, '45e0003c4cce00003d014091ac144077ac1456e2')
    print "D: " + str(output == 'ee1cae4f34904f46515bc173562021c64afe08fc')

    output = ci.decrypt('a24fd61d0b627b91f7451be11df4d40e', 0x1C3, 'downlink', 0, 'ee1cae4f34904f46515bc173562021c64afe08fc')
    print "E: " + str(output == '45e0003c4cce00003d014091ac144077ac1456e2')

test()