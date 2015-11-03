
from cStringIO import StringIO
from PIL import Image
img = Image.open(filename)
s = StringIO()
img.save(s, format='PNG')
a = s.getvalue()
print a

s.close()
#print ocr.process_image_datastring(str(a) ,"/home/xucb/projects/OCR/tw_ocr/models")

