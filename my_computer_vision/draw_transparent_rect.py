from PIL import Image
from PIL import ImageDraw
from io import BytesIO
from urllib.request import urlopen

#url = "https://i.ytimg.com/vi/W4qijIdAPZA/maxresdefault.jpg"
#file = BytesIO(urlopen(url).read())
img = Image.open('test.jpg')
img = img.convert("RGBA")

# Make a blank image for the rectangle, initialized to a completely
# transparent color.
tmp = Image.new('RGBA', img.size, (0,0,0,0))

# Create a drawing context for it.
draw = ImageDraw.Draw(tmp)

# Determine the bounding box of the largest possible semi-transparent
# square rectangle centered on the temporary image and draw it.
if img.size[0] > img.size[1]:
    size = img.size[1]
    llx, lly = (img.size[0] - img.size[1]) // 2, 0
else:
    size = img.size[0]
    llx, lly = 0, (img.size[1] - img.size[0]) // 2

# Add one to upper point because second point is just outside the drawn
# rectangle.
urx, ury = llx + size + 1, lly + size + 1
draw.rectangle(((llx, lly), (urx, ury)), fill=(0,0,0,127))

# Alpha composite the two images together.
img = Image.alpha_composite(img, tmp)
img = img.convert("RGB") # Remove alpha for saving in jpg format.
img.save('test_out.jpg')
img.show()
