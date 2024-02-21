
class BaseEncDec():
    def __init__(self, string, base=16):
        self.string = string
        self.base = base
        assert(self.base == 16)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.processed_string = ""
        self.all_operations = []
    
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

    def history(self):
        if len(self.all_operations.keys()) == 0:
            print("There is no data saved!")
        else:
            print(self.all_operations)

    def set_new_string(self, string):
        self.string = string
    
    def encode(self, string = "", should_save = False):
        to_process = ""
        encoded_string = ""
        grouped_enc_chrs = []

        if string:
            to_process = string
        else:
            if self.processed_string:
                to_process = self.processed_string
            else:
                to_process = self.string
        bitarray = self.tobits(to_process)
        nr_enc_chrs = len(bitarray) // 6
        remainder = len(bitarray) - nr_enc_chrs * 6
        for idx in range(0, len(bitarray), 6):
            current_enc_chr = self.frombits([0, 0] + bitarray[idx:idx+6])
            grouped_enc_chrs.append(self.alphabet[current_enc_chr])
        encoded_string = ''.join(grouped_enc_chrs)

        if should_save and (string == ""):
            self.processed_string = encoded_string
            self.all_operations.append({"input": to_process, "encoded": encoded_string})

        return encoded_string

    def decode(self, string = "", should_save = False):
        ords = []
        array_bits = []
        decoded_string = ""
        to_process = ""
        if string:
            to_process = string
        else:
            if self.processed_string:
                to_process = self.processed_string
            else:
                to_process = self.string
        for item in self.processed_string:
            ords.append(self.tobits(chr(self.alphabet.index(item)))[2:])
        for arr in ords:
            array_bits += arr
        for idx in range(0, len(array_bits), 8):
            decoded_chr = chr(self.frombits(array_bits[idx:idx+8]))
            decoded_string += decoded_chr
        
        if should_save and (string == ""):
            self.processed_string = decoded_string
            self.all_operations.append({"input": to_process, "decoded": decoded_string})

        return decoded_string
        


if __name__ == "__main__":
    test = BaseEncDec("ABC")
    data = test.encode("QWE")
    print(data)
    test.decode(should_save=True)
