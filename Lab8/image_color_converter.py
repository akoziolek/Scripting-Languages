from PIL import Image

img = Image.open(r'.\assets\app_icon.png')
img = img.convert('RGBA')

data = img.getdata()
new_image = []

for item in data:
    if item[3] == 0:
        new_image.append(item)
    elif item[0] in range(0, 10) and item[3] != 0:
        new_image.append((45, 109, 247, item[3])) 
    else:
        new_image.append(item)

img.putdata(new_image)
img.save('app_icon2.png', 'PNG')