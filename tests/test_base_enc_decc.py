import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from BaseEncDec.base_enc_dec import BaseEncDec

def testing_base_enc(cls): 
    class TestDecorator: 
        def __init__(self, x):
            self.wrap = cls(x) 
        def test_encode(self, string, rez): 
            encoded_string = self.wrap.base_enc_dec.encode(string)
            assert(encoded_string == rez)
            print("Passed")
        def test_decode(self, string,rez):
            encoded_string = self.wrap.base_enc_dec.decode(string)
            assert(encoded_string == rez)
            print("Passed")
    return TestDecorator 


@testing_base_enc
class TestBaseEncDec():
    def __init__(self, obj):
        self.base_enc_dec = obj

tester = TestBaseEncDec(BaseEncDec())
tester.test_encode("Man is distinguished, not only by his reason, but ...", "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCAuLi4=")
tester.test_encode("Sternocleidomastoidian", "U3Rlcm5vY2xlaWRvbWFzdG9pZGlhbg==")
tester.test_encode("ABC", "QUJD")

tester.test_decode("QUJD", "ABC")
tester.test_decode("TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCAuLi4=", "Man is distinguished, not only by his reason, but ...")
tester.test_decode("U3Rlcm5vY2xlaWRvbWFzdG9pZGlhbg==", "Sternocleidomastoidian")