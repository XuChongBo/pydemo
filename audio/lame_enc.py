import ctypes

def encode_mp3(outputFile,sample_rate,channel_count,bit_rate,audio_data):
    lame = LameEncoder(sample_rate,channel_count, bit_rate)
    output_file  = open(outputFile, "wb")
    output = lame.encode(audio_data,output_file)
    output_file.close()

class LameEncoder():
    def __init__(self, sample_rate, channel_count, bit_rate):
        self.dll  = ctypes.CDLL("c:\\libmp3lame.dll")
        self.dll.lame_init.restype = ctypes.c_void_p;
        self.lame = self.dll.lame_init()
        self.dll.lame_set_in_samplerate.argtypes = [ctypes.c_void_p, ctypes.c_int];
        self.dll.lame_set_in_samplerate(self.lame, sample_rate);
        self.dll.lame_set_num_channels.argtypes = [ctypes.c_void_p, ctypes.c_int];
        self.dll.lame_set_num_channels(self.lame, channel_count);
        self.dll.lame_set_brate.argtypes = [ctypes.c_void_p, ctypes.c_int];
        self.dll.lame_set_brate(self.lame, bit_rate);
        self.dll.lame_set_quality.argtypes = [ctypes.c_void_p, ctypes.c_int];
        self.dll.lame_set_quality(self.lame, 3);
        self.dll.lame_init_params.argtypes = [ctypes.c_void_p];
        self.dll.lame_init_params(self.lame);

    def encode(self, pcm_data, fn):
        sample_count    = len(pcm_data) /2
        output_buff_len = int(1.25 * sample_count + 7200)
        output_buff     = (ctypes.c_char*output_buff_len)()
        self.dll.lame_encode_buffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int];
        output_size     = self.dll.lame_encode_buffer(self.lame, pcm_data, 0, sample_count, output_buff, output_buff_len);
        if (output_size): fn.write(output_buff[0:output_size])

def encode_sin():
    import struct
    from math import sin, pi
    f = 0.1
    b = ''
    for i in xrange(40960):
        y = (16000.0*sin(pi*f*i/4096.0))
        b += struct.pack("I",y)
    encode_mp3('teste.mp3',44100,1,128,b)

def try_enc():
    import os
    inFile = open('c:\\1.pcm', 'rb')
    #inFile = open('c:\\1.wav', 'rb')
    inFile.seek(0, os.SEEK_END)
    wavFileSize = inFile.tell()
    inFile.seek(44) # skip wav header
 
 
    outFile = open('c:\\x.mp3', 'wb')
    lame = LameEncoder(22000,1,128)
    #lame = LameEncoder(44100,1,128)
 
    while(1):
        inBytes = inFile.read(512)
        if inBytes == '':
            break
        #inBuf = ctypes.create_string_buffer(inBytes, 512)
        sample_count    = len(inBytes) /2
        output_buff_len = int(1.25 * sample_count + 7200)
        output_buff     = (ctypes.c_char*output_buff_len)()
        lame.dll.lame_encode_buffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int];
        output_size     = lame.dll.lame_encode_buffer(lame.lame, inBytes, 0, len(inBytes)/2, output_buff, output_buff_len);
        outFile.write(output_buff[0:output_size])

    outFile.close()

if __name__ == "__main__":
    #encode_sin()
    try_enc()
