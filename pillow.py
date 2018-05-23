from PIL import Image,ImageFilter
im = Image.open('test.jpg')
w,h = im.size
print(w,h)
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpg','jpeg')