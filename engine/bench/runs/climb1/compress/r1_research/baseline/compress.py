import lzma, sys

sys.stdout.buffer.write(lzma.compress(sys.stdin.buffer.read(), preset=9 | lzma.PRESET_EXTREME))
