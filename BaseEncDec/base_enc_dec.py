
class BaseEncDec():
    def __init__(self, string="", base=16):
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
        for b in range(int(len(bits) / 6)):
            byte = bits[b*6:(b+1)*6]
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
        grouped_enc_chrs = []
        encoded_string = ""
        if string:
            to_process = string
        else:
            if self.processed_string:
                to_process = self.processed_string
            else:
                to_process = self.string
        char_array_3 = [None, None, None]
        char_array_4 = [None, None, None, None]
        length = len(to_process)
        i = 0
        while length != 0:
            length -= 1
            char_array_3[i] = to_process[0]
            to_process = to_process[1:]
            i += 1
            if i == 3:
                char_array_4[0] = (ord(char_array_3[0]) & 0xFC) >> 2
                char_array_4[1] = ((ord(char_array_3[0]) & 0x03) << 4) + ((ord(char_array_3[1]) & 0xf0) >> 4)
                char_array_4[2] = ((ord(char_array_3[1]) & 0x0f) << 2) + ((ord(char_array_3[2]) & 0xc0) >> 6)
                char_array_4[3] = ord(char_array_3[2]) & 0x3f

                for i in range(0,4):
                    encoded_string += self.alphabet[char_array_4[i]]
                i = 0

        if i:
            for j in range(i, 3):
                char_array_3[j] = '\0'
            char_array_4[0] = (ord(char_array_3[0]) & 0xfc) >> 2
            char_array_4[1] = ((ord(char_array_3[0]) & 0x03) << 4) + ((ord(char_array_3[1]) & 0xf0) >> 4)
            char_array_4[2] = ((ord(char_array_3[1]) & 0x0f) << 2) + ((ord(char_array_3[2]) & 0xc0) >> 6)
            char_array_4[3] = ord(char_array_3[2]) & 0x3f
            for j in range(0, i+1):
                encoded_string += self.alphabet[char_array_4[j]]
            
            while i < 3:
                encoded_string += "="
                i += 1
        
        if should_save and (string == ""):
            self.processed_string = decoded_string
            self.all_operations.append({"input": to_process, "decoded": decoded_string})

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
