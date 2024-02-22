
class BaseEncDec():
    def __init__(self, string="", base=16):
        self.string = string
        self.base = base
        assert(self.base == 16)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.deocde_alphabet = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 62, 63, 62, 62, 63, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  3,  4,  5,  6,
        7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,
        0,  0,  0, 63,  0, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51 ]
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

        char_array_3 = [None, None, None]
        char_array_4 = [None, None, None, None]
        length = len(to_process)
        pad = (length > 0) and ((length % 4) or (to_process[length - 1] == "="))
        L = ((length + 3) // 4 - pad) * 4
        i = 0

        for i in range(0, L, 4):
            val = self.deocde_alphabet[ord(to_process[i])] << 18 | \
                  self.deocde_alphabet[ord(to_process[i + 1])] << 12 | \
                  self.deocde_alphabet[ord(to_process[i + 2])] << 6  | \
                  self.deocde_alphabet[ord(to_process[i + 3])]
            
            decoded_string += chr(val >> 16)
            decoded_string += chr((val >> 8) & 0xFF)
            decoded_string += chr(val & 0xFF)
        
        if pad:
            val = (self.deocde_alphabet[ord(to_process[L])] << 18) | (self.deocde_alphabet[ord(to_process[L+1])] << 12)
            decoded_string += chr(val >> 16)

            if (length > (L + 2)) and to_process[L + 2] != '=':
                val |= self.deocde_alphabet[ord(to_process[L + 2])] << 6
                decoded_string += chr(val >> 8 & 0xFF)

        if should_save and (string == ""):
            self.processed_string = decoded_string
            self.all_operations.append({"input": to_process, "decoded": decoded_string})

        return decoded_string
        


if __name__ == "__main__":
    test = BaseEncDec("ABC")
    data = test.encode("QWE")
    test.decode(should_save=True)
