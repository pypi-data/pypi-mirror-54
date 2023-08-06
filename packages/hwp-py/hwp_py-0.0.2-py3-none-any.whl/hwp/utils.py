import zlib


class ZlibDecompressStream(object):
    def __init__(self, stream, wbits=15, chunk_size=4096):
        self._stream = stream
        self._decompressor = zlib.decompressobj(wbits)
        self.chunk_size = chunk_size
        self.buffer = b""

    def read(self, size):
        while len(self.buffer) < size and not self._decompressor.eof:
            chunk = self._decompressor.unconsumed_tail
            if not chunk:
                chunk = self._stream.read(self.chunk_size)
                if not chunk:
                    break

            self.buffer += self._decompressor.decompress(chunk, self.chunk_size)

        result = self.buffer[:size]
        self.buffer = self.buffer[size:]

        return result


class ZlibStreamReader:
    def __init__(self, src, read_chunk_size=4096):
        self._src = src
        self._decompressor = zlib.decompressobj(-15)
        self._read_chunk_size = read_chunk_size
        self._buf = bytearray()

    def read(self, size=-1):
        while not self._decompressor.eof:
            chunk = self._src.read(self._read_chunk_size)
            if not chunk:
                break

            self._buf += self._decompressor.decompress(chunk)
            if size != -1 and len(self._buf) >= size:
                break

        if size == -1:
            size = len(self._buf)
        result, self._buf = self._buf[:size], self._buf[size:]

        return bytes(result)
