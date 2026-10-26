import lzma, sys

sys.stdout.buffer.write(lzma.decompress(sys.stdin.buffer.read()))
