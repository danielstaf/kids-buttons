#!/usr/bin/env python3

import os, sys, time

streamdeck_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "python-elgato-streamdeck/src")
print(streamdeck_dir)
sys.path.append(streamdeck_dir)

import StreamDeck.StreamDeck as StreamDeck

from PIL import Image, ImageDraw, ImageFont


class Key:

   def __init__(self, deck, key_index):

      self.deck = deck
      self.key = key_index
      self.text = None

      # Get the required key image dimensions
      image_format = deck.key_image_format()
      width = image_format['width']
      height = image_format['height']
      self.order = image_format['order']

      # Create new key image of the correct dimensions, black background
      self.image = Image.new("RGB", (width, height), 'black')

   def _overlay_text(self, text):
      # Load a custom TrueType font and use it to overlay the key index, draw key
      # number onto the image
      font = ImageFont.truetype("Assets/Roboto-Regular.ttf", 14)
      draw = ImageDraw.Draw(self.image)
      draw.text((0, 0), text=text, font=font, fill=(255, 255, 255, 128))

   def _transfer_image(self):
      if self.text:
         self._overlay_text(self.text)

      # Get the raw r, g and b components of the generated image (note we need to
      # flip it horizontally to match the format the StreamDeck expects)
      r, g, b = self.image.transpose(Image.FLIP_LEFT_RIGHT).split()

      # Recombine the B, G and R elements in the order the display expects them,
      # and convert the resulting image to a sequence of bytes
      rgb = { "R": r, "G": g, "B": b }
      image_bytes = Image.merge("RGB", (rgb[self.order[0]], rgb[self.order[1]], rgb[self.order[2]])).tobytes()
      self.deck.set_key_image(self.key, image_bytes)

   def set_text(self, text):
      self.text = text
      self._transfer_image()

   def set_color(self, color):
      self.image.paste(color, [0, 0, self.image.size[0], self.image.size[1]])
      self._transfer_image()

   def clear(self):
      self.text = None
      self.set_color((0, 0, 0))


# def get_key_image(deck, key, state):
#    # Get the required key image dimensions
#    image_format = deck.key_image_format()
#    width = image_format['width']
#    height = image_format['height']
#    order = image_format['order']
# 
#    # Create new key image of the correct dimensions, black background
#    image = Image.new("RGB", (width, height), 'black')
# 
#    image.paste( (255,0,0), [0,0,image.size[0],image.size[1]])
# 
#    # Load a custom TrueType font and use it to overlay the key index, draw key
#    # number onto the image
#    font = ImageFont.truetype("python-elgato-streamdeck/src/Assets/Roboto-Regular.ttf", 14)
#    draw = ImageDraw.Draw(image)
#    draw.text((10, height - 20), text="Key {}".format(key), font=font, fill=(255, 255, 255, 128))
# 
#    # Get the raw r, g and b components of the generated image (note we need to
#    # flip it horizontally to match the format the StreamDeck expects)
#    r, g, b = image.transpose(Image.FLIP_LEFT_RIGHT).split()
# 
#    # Recombine the B, G and R elements in the order the display expects them,
#    # and convert the resulting image to a sequence of bytes
#    rgb = { "R": r, "G": g, "B": b }
#    return Image.merge("RGB", (rgb[order[0]], rgb[order[1]], rgb[order[2]])).tobytes()





def main():   

      

   
   manager = StreamDeck.DeviceManager()
   decks = manager.enumerate()
   
   if len(decks) > 1:
      sys.exit('Found more than one connected streamdeck.')
   print("Connected to Stream Deck.")
   deck = decks[0]
   deck.open()
   deck.reset()
   deck.set_brightness(30)

   keys = [Key(deck, key_index) for key_index in range(deck.key_count())]



   def key_change_callback(deck, key, state):
      print("Key {} = {}".format(key, state))
   
      keys[key].set_color((255,0,255))
      keys[key].set_text("!")
   
      if key == deck.key_count() - 1:
         deck.reset()
         deck.close()
         sys.exit()

   deck.set_key_callback(key_change_callback)

   while True:
      

#       for key in keys:
#          key.set_color((0,0,255))
#          key.set_text("tomten")
#          time.sleep(0.05)


      time.sleep(1)
      
if __name__ == "__main__":
   main()
