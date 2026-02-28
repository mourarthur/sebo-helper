from PIL import Image, ImageDraw

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='black')
    d = ImageDraw.Draw(img)
    text = "SH"
    # Basic centering logic - might need adjusting for font size
    # Since we don't have a guaranteed font, we'll just draw a white rectangle for now
    d.rectangle([(size//4, size//4), (size*3//4, size*3//4)], fill="white")
    img.save(filename)

create_icon(192, 'app/static/icons/icon-192x192.png')
create_icon(512, 'app/static/icons/icon-512x512.png')
