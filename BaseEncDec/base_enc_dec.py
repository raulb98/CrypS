class BaseEncDec():
    def __init__(self, string, base=16):
        self.string = string
        self.base = base
        assert(self.base == 16)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    @staticmethod
    def tobits(s):
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])
        return result

    @staticmethod
    def frombits(bits):
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            return int(''.join([str(bit) for bit in byte]), 2)
    
    def encode(self):
        bitarray = self.tobits(self.string)
        grouped_enc_chrs = []
        nr_enc_chrs = len(bitarray) // 6
        remainder = len(bitarray) - nr_enc_chrs * 6
        for idx in range(0, len(bitarray), 6):
            current_enc_chr = self.frombits([0, 0] + bitarray[idx:idx+6])
            grouped_enc_chrs.append(self.alphabet[current_enc_chr])
        return ''.join(grouped_enc_chrs)


if __name__ == "__main__":
    test = BaseEncDec("ABC")
    test.encode()