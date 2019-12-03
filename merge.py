from PIL import Image

def blend_two_images():
    img1 = Image.open( "name.jpg")
    img1 = img1.resize((640, 930))
    img1 = img1.convert('RGBA')
 
    img2 = Image.open( "flower.jpg")
    img2 = img2.resize((640, 930))
    img2 = img2.convert('RGBA')
    
    img = Image.blend(img1, img2, 0.6)
    img.show()
    img.save("blend.bmp")

if __name__ == '__main__':
    blend_two_images()