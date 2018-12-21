from PIL import Image, ImageDraw, ImageFont
from application.cardgenerator.card_size import CardSize

class CardGenerator():

    def generate_card(self, ship, card_size):
        self.stat_vertical_sep = 75

        image = self.init_image(card_size)
        drawer = ImageDraw.Draw(image)
        
        # Draw title and cost. If ship is command-capable, move title a little way to the right and draw command icon.
        if ship.command_capable:
            drawer.text(xy=(198, 27), text=ship.name, fill=(255,255,255), font=self.ship_title_font)
            # Placeholder for command icon
            drawer.text(xy=(93, 27), text="C", fill=(255,255,255), font=self.ship_title_font)
        else:
            drawer.text(xy=(93, 27), text=ship.name, fill=(255,255,255), font=self.ship_title_font)

        drawer.text(xy=(913, 27), text=str(ship.cost)+" pts", fill=(255,255,255), font=self.ship_title_font)

        # Draw evasion endurance stat name if ship has a pulse drive
        if "pulse" or "Pulse" in ship.propulsion_type:
            drawer.text(xy=(770,700+self.stat_vertical_sep*2), text="Endurance", fill=(255,255,255), font=self.stats_font)



        image.save("application/cardgenerator/assets/result.png")

    def init_image(self, card_size):
        # This method doesn't actually use the card size yet
        image = Image.open("application/cardgenerator/assets/templates/card_base_1.png")

        # Set fonts
        self.ship_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 94)
        self.sub_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 50)
        self.stats_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 56)
        self.flavor_font = ImageFont.truetype("application/cardgenerator/assets/fonts/CharisSIL-B.ttf", 47)

        ## Draw text common to all images
        drawer = ImageDraw.Draw(image)
        
        # Draw subsection titles
        drawer.text(xy=(72,623), text="Propulsion", fill=(255,255,255), font=self.sub_title_font)
        drawer.text(xy=(770,623), text="Evasion", fill=(255,255,255), font=self.sub_title_font)

        # Draw common stat names
        drawer.text(xy=(72,700), text="Type", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(72,700+self.stat_vertical_sep), text="Move", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(72,700+2*self.stat_vertical_sep), text="Delta-v", fill=(255,255,255), font=self.stats_font)
        # Note: Passive evasion stat name is not drawn here since not all ships have it
        drawer.text(xy=(770,700), text="Passive", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(770,700+self.stat_vertical_sep), text="Active", fill=(255,255,255), font=self.stats_font)




        return image