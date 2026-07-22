from PIL import Image
from typing import Tuple


class BaseEncoder:
    """Template base class for encoders.

    Subclasses must implement `encode(image_path, text)` and
    `decode(image_path)`.
    """

    name = "base"

    def encode(self, image_path: str, text: str) -> None:
        raise NotImplementedError()

    def decode(self, image_path: str) -> str:
        raise NotImplementedError()


class RedLSBEncoder(BaseEncoder):
    """Encode bits in the red channel LSB of each pixel."""

    name = "LSB-red"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                r = (r & ~1) | bit
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str(r & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class GreenLSBEncoder(BaseEncoder):
    """Encode bits in the green channel LSB of each pixel."""

    name = "LSB-green"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                g = (g & ~1) | bit
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str(g & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class BlueLSBEncoder(BaseEncoder):
    """Encode bits in the blue channel LSB of each pixel."""

    name = "LSB-blue"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                b = (b & ~1) | bit
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str(b & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class RGBCycleEncoder(BaseEncoder):
    """Encode bits cycling through R, G, B channels per pixel."""

    name = "LSB-rgb-cycle"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                channels = [r, g, b]
                for ci in range(3):
                    if idx >= len(bits):
                        break
                    bit = int(bits[idx])
                    channels[ci] = (channels[ci] & ~1) | bit
                    idx += 1
                pixels[x, y] = tuple(channels)
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.extend([str(r & 1), str(g & 1), str(b & 1)])

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class RedMSBEncoder(BaseEncoder):
    """Encode bits in the red channel MSB of each pixel."""

    name = "MSB-red"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                r = (r & ~(1 << 7)) | (bit << 7)
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str((r >> 7) & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class GreenMSBEncoder(BaseEncoder):
    """Encode bits in the green channel MSB of each pixel."""

    name = "MSB-green"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                g = (g & ~(1 << 7)) | (bit << 7)
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str((g >> 7) & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


class BlueMSBEncoder(BaseEncoder):
    """Encode bits in the blue channel MSB of each pixel."""

    name = "MSB-blue"

    def _text_to_bits(self, text: str) -> str:
        data = text.encode('utf-8')
        bits = "".join(format(b, '08b') for b in data)
        bits += "00000000"  # NUL terminator
        return bits

    def encode(self, image_path: str, text: str) -> None:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        bits = self._text_to_bits(text)

        width, height = img.size
        idx = 0
        for y in range(height):
            for x in range(width):
                if idx >= len(bits):
                    break
                r, g, b = pixels[x, y]
                bit = int(bits[idx])
                b = (b & ~(1 << 7)) | (bit << 7)
                pixels[x, y] = (r, g, b)
                idx += 1
            if idx >= len(bits):
                break
        img.save(image_path)

    def decode(self, image_path: str) -> str:
        return self.decode_bytes(image_path).decode('utf-8', errors='replace')

    def decode_bytes(self, image_path: str) -> bytearray:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(str((b >> 7) & 1))

        ba = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(''.join(byte), 2)
            if val == 0:
                break
            ba.append(val)
        return ba


def available_encoders() -> Tuple[BaseEncoder, ...]:
    return (
        RedLSBEncoder(),
        GreenLSBEncoder(),
        BlueLSBEncoder(),
        RGBCycleEncoder(),
        RedMSBEncoder(),
        GreenMSBEncoder(),
        BlueMSBEncoder(),
    )


def get_encoder_by_name(name: str) -> BaseEncoder:
    for enc in available_encoders():
        if enc.name == name:
            return enc
    raise KeyError(f"Encoder inconnue: {name}")
