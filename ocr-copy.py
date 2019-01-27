import pytesseract
from PIL import Image, ImageTk
from googletrans import Translator
import tkinter as tk
from tkinter import filedialog
import os
print("imported")
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


class OCR():
    #######################Code from https://www.codementor.io/isaib.cicourel/image-manipulation-in-python-du1089j1u
    # Open an Image
    def open_image(self, path):
      newImage = Image.open(path)
      return newImage

    # Save Image
    def save_image(self, image, path):
      image.save(path, 'png')

    # Create a new image with the given size
    def create_image(self, i, j):
      image = Image.new("RGB", (i, j), "black")
      return image

    # Get the pixel from the given image
    def get_pixel(self, image, i, j):
        # Inside image bounds?
        width, height = image.size
        if i > width or j > height:
          return None

        # Get Pixel
        pixel = image.getpixel((i, j))
        return pixel

    ##############################################

    def process_meme(self, image):
      # Get size
      width, height = image.size

      # Create new Image and a Pixel Map
      new = self.create_image(width, height)
      pixels = new.load()

      # Transform to grayscale
      for i in range(width):
        for j in range(height):
          # Get Pixel
          pixel = self.get_pixel(image, i, j)
          pixels[i,j] = pixel
          # Get R, G, B values (This are int from 0 to 255)
          red =   pixel[0]
          green = pixel[1]
          blue =  pixel[2]

          if (((red > 240) and (green > 240) and (blue > 240)) or ((red < 15) and (green < 15) and (blue < 15))):
            pixels[i, j] = (0, 0, 0)
          else:
            pixels[i, j] = (250, 250, 250)

      self.save_image(new, 'processed_image.png')
        # Return new image
      return new

    def get_text(self, path):

        meme_img = Image.open(path)
        processed_img = meme_img

        result1 = pytesseract.image_to_string(meme_img)
        result2 = pytesseract.image_to_string(processed_img)

        return result1

class Translate():

    def translate_to_spanish(text):
        # Instantiates a client
        translator = Translator()

        # The target language
        target = 'es'
        source = 'en'

        # Translates some text into Russian
        translation = translator.translate(text, src = source, dest = target)

        return translation.text

class App():

    meme_path = 'image2.jpg'
    ocr = OCR()

    def __init__(self):

        self.root = tk.Tk()

        self.upload_button = tk.Button(self.root, text = "upload image", command = self.upload_image)
        self.upload_button.pack()

        self.img = ImageTk.PhotoImage(Image.open(self.meme_path).resize((250, 250), Image.ANTIALIAS))

        self.panel = tk.Label(self.root, image = self.img)
        self.panel.pack(side = "top", fill = "both", expand = "yes")

        self.translated = tk.Text(self.root)
        self.translated.pack()
        self.translated.insert(tk.END, Translate.translate_to_spanish(self.ocr.get_text(self.meme_path)))

        tk.mainloop()

    def upload_image(self):

        self.currdir = os.getcwd()
        self.choosedir = filedialog.askopenfilename(parent = self.root, initialdir = self.currdir, title = 'Select Image')
        if (len(self.choosedir) > 0):
            self.meme_path = self.choosedir
        self.update_image()

    def update_image(self):
        self.panel.destroy()
        self.translated.destroy()

        if (len(self.meme_path)>0):
            self.img = ImageTk.PhotoImage(Image.open(self.meme_path).resize((250, 250), Image.ANTIALIAS))
        else:
            self.img = ImageTk.PhotoImage(Image.open("image2.jpg").resize((250, 250), Image.ANTIALIAS))
        self.panel = tk.Label(self.root, image = self.img)
        self.panel.pack(side = "top", fill = "both", expand = "yes")

        self.translated = tk.Text(self.root)
        self.translated.pack()
        self.translated.insert(tk.END, Translate.translate_to_spanish(self.ocr.get_text(self.meme_path)))

App()
