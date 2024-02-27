import random

class DES:
    FEISTEL_ROUNDS = 16
    def __init__(self, string = "", seed = 0):
        self.string = string
        self.seed = seed
        random.seed(self.seed)
        self.keys = []
        for _ in range(self.FEISTEL_ROUNDS):
            self.keys.append((int(random.random() * 0x00FFFFFF)) & 0x00FFFFFF)

    def expand_half_to_48(self, dw_half):
        return dw_half << 8

    def round_function(self, dw_right_half, round_index):
        dw_expanded_right_half = self.expand_half_to_48(dw_right_half)
        current_key = self.keys[round_index]
        return (dw_expanded_right_half ^ current_key) >> 8

    def convert_4byte_chars_to_dword(self, text):
        dword = ord(text[3])
        dword = dword + (ord(text[2]) << 8)
        dword = dword + (ord(text[1]) << 16)
        dword = dword + (ord(text[0]) << 24)
        return dword

    def convert_dword_to_4byte_chars(self, dword):
        text = [None, None, None, None]
        text[0] = chr((dword >> 24) & 0xFF)
        text[1] = chr((dword >> 16) & 0xFF)
        text[2] = chr((dword >> 8) & 0xFF)
        text[3] = chr(dword & 0xFF)
        return ''.join(text)

    def feistel_cipher_encode(self, plain_text):
        text = plain_text
        dw_left_half = self.convert_4byte_chars_to_dword(text[:4])
        dw_right_half = self.convert_4byte_chars_to_dword(text[4:])

        for round_index in range(self.FEISTEL_ROUNDS):
            #print("Start of iteration {} : [{}] [{}]".format(round_index, dw_left_half, dw_right_half))
            dw_new_left_half = dw_right_half
            dw_xored_half = self.round_function(dw_right_half, round_index)
            dw_left_half = dw_left_half ^ dw_xored_half
            dw_right_half = dw_left_half
            dw_left_half = dw_new_left_half
            #print("End of iteration {} : [{}] [{}]".format(round_index, dw_left_half, dw_right_half))

        new_left_half = self.convert_dword_to_4byte_chars(dw_left_half)
        new_right_half = self.convert_dword_to_4byte_chars(dw_right_half)

        return new_left_half + new_right_half


    def encode(self):
        encrypted_buffer = ""
        pad = 8 - (len(self.string) % 8)
        for i in range(pad):
            self.string = self.string + chr(0)
        for c_index in range(0, len(self.string), 8):
            c_plain_text = self.string[c_index:c_index+8]
            encrypted_buffer += self.feistel_cipher_encode(c_plain_text)
        return encrypted_buffer


if __name__ == "__main__":
    des = DES("please test me", 10)
    buff = des.encode()
    print(buff)