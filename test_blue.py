from PIL import Image
from encoders import BlueLSBEncoder

img_path = 'test_blue.png'

img = Image.new('RGB', (16, 16), (100, 120, 140))
img.save(img_path)

enc = BlueLSBEncoder()
message = 'Hello-BlueLSB-✓'
print('Encoding message:', message)
enc.encode(img_path, message)

decoded = enc.decode(img_path)
print('Decoded message:', repr(decoded))

if decoded == message:
    print('OK: blue LSB encode/decode roundtrip successful')
else:
    print('FAIL: roundtrip mismatch')
