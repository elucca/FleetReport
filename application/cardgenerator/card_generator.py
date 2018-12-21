from PIL import Image, ImageDraw, ImageFont
from card_size import CardSize

class CardGenerator():

    def __init__(self):
        self.card_size = CardSize.BIG
        self.init_image(self.card_size)

    def generate_card(self, ship, card_size):
        drawer = ImageDraw.Draw(self.image)
        
        # Draw title and cost
        drawer.text(xy=(198, 27), text=ship.name, fill=(255,255,255), font=self.ship_title_font)
        drawer.text(xy=(913, 27), text=str(ship.cost)+" pts", fill=(255,255,255), font=self.ship_title_font)

        self.image.save("assets/result.png")

    def init_image(self, card_size):
        # This method doesn't actually use the card size yet
        self.image = Image.open("assets/templates/card_base_1.png")

        # Set fonts
        self.ship_title_font = ImageFont.truetype("assets/fonts/Oswald-Bold.ttf", 94)
        self.weapon_title_font = ImageFont.truetype("assets/fonts/Oswald-Bold.ttf", 54)
        self.stats_font = ImageFont.truetype("assets/fonts/Oswald-Bold.ttf", 58)
        self.flavor_font = ImageFont.truetype("assets/fonts/CharisSIL-B.ttf", 47)