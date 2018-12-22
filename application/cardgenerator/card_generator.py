from PIL import Image, ImageDraw, ImageFont
from application.cardgenerator.card_size import CardSize
from application.weapons.models import *

class CardGenerator():

    def generate_card(self, ship, card_size):
        self.stat_vertical_sep = (0,74)

        image = self.init_card(card_size)
        drawer = ImageDraw.Draw(image)
        
        # Draw title and cost. If ship is command-capable, move title a little way to the right and draw command icon.
        if ship.command_capable:
            drawer.text(xy=(198, 27), text=ship.name, fill=(255,255,255), font=self.ship_title_font)
            # Placeholder for command icon
            drawer.text(xy=(93, 27), text="C", fill=(255,255,255), font=self.ship_title_font)
        else:
            drawer.text(xy=(93, 27), text=ship.name, fill=(255,255,255), font=self.ship_title_font)

        drawer.text(xy=(913, 27), text=str(ship.cost)+" pts", fill=(255,255,255), font=self.ship_title_font)

        # Draw subsection titles
        drawer.text(xy=(72,623), text="Propulsion", fill=(255,255,255), font=self.sub_title_font)
        drawer.text(xy=(770,623), text="Evasion", fill=(255,255,255), font=self.sub_title_font)

        # Draw common stat names
        drawer.text(xy=(72,710), text="Type", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(72,710+self.stat_vertical_sep[1]), text="Move", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(72,710+self.stat_vertical_sep[1]*2), text="Delta-v", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(770,710), text="Passive", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=(770,710+self.stat_vertical_sep[1]), text="Active", fill=(255,255,255), font=self.stats_font)
        # Draw evasion endurance stat name if ship has a pulse drive
        if "pulse" or "Pulse" in ship.propulsion_type:
            drawer.text(xy=(770,710+self.stat_vertical_sep[1]*2), text="Endurance", fill=(255,255,255), font=self.stats_font)

        self._draw_weapons_(self.get_weapons(ship), drawer)

        image.save("application/cardgenerator/assets/result.png")

    def init_card(self, card_size):
        # This method doesn't actually use the card size yet
        image = Image.open("application/cardgenerator/assets/templates/card_base_1.png")

        # Set fonts
        self.ship_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 94)
        self.sub_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 54)
        self.stats_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 56)
        self.flavor_font = ImageFont.truetype("application/cardgenerator/assets/fonts/CharisSIL-B.ttf", 47)

        return image

    def get_weapons(self, ship):
        # Returns the ship's weapons in the order required for ship cards
        # Note: Due to SQLAlchemy weirdness these are InstrumentedLists and iterating through them may not
        # actually work. However, retrieving the first works, and we only really need one of them as multiple
        # weapons of the same type are not even intended to be handled by the cards.
        weapons = []

        if next(iter(ship.CIWSs), None):
            weapons.insert(0, next(iter(ship.CIWSs)))

        if next(iter(ship.ewars), None):
            weapons.insert(0, next(iter(ship.ewars)))

        if next(iter(ship.area_missiles), None):
            weapons.insert(0, next(iter(ship.area_missiles)))

        if next(iter(ship.missiles), None):
            weapons.insert(0, next(iter(ship.missiles)))

        if next(iter(ship.lasers), None):
            weapons.insert(0, next(iter(ship.lasers)))

        return weapons

    def _draw_weapons_(self, weapons, drawer):
        i = 0
        while i < 3:
            if i == 0:
                startcoords = (90,1015)
            if i == 1:
                startcoords = (710,1015)
            if i == 2:
                startcoords = (710,1525)

            # Draw weapon flavor text (common to all weapon types)
            flavorcoords = self._add_coords_(startcoords, (0,65))
            drawer.text(xy=flavorcoords, text=weapons[i].name, fill=(255,255,255), font=self.flavor_font)

            # Coords for first stat row (separation between flavor text and stats)
            statstart = self._add_coords_(flavorcoords, (0,90))
            # Displacement for the stat numbers themselves, add to the starting position
            number_dsplc = (370,0)

            if isinstance(weapons[i], Laser):
                drawer.text(xy=startcoords, text="Beam", fill=(255,255,255), font=self.sub_title_font)
                # When laser data type is actually completely implemented range/dmg goes here

            if isinstance(weapons[i], Missile):
                # Title
                drawer.text(xy=startcoords, text="Anti-ship missiles", fill=(255,255,255), font=self.sub_title_font)
                # Volley
                drawer.text(xy=statstart, text="Volley", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(weapons[i].volley), fill=(255,255,255), font=self.stats_font)
                # Stores
                row2 = self._add_coords_(statstart, self.stat_vertical_sep)
                drawer.text(xy=row2, text="Stores", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(weapons[i].stores), fill=(255,255,255), font=self.stats_font)

            if isinstance(weapons[i], AreaMissile):
                # Differentiate between defense and attack missiles.
                if not weapons[i].dmg_missile:
                    am_type = "Assault missiles"
                else:
                    am_type = "Defense missiles"

                # Title
                if not weapons[i].dmg_missile:
                    drawer.text(xy=startcoords, text=am_type, fill=(255,255,255), font=self.sub_title_font)
                else:
                    drawer.text(xy=startcoords, text=am_type, fill=(255,255,255), font=self.sub_title_font)
                # Range
                drawer.text(xy=statstart, text="Range", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(weapons[i].am_range), fill=(255,255,255), font=self.stats_font)
                # Anti-ship
                row2 = self._add_coords_(statstart, self.stat_vertical_sep)
                drawer.text(xy=row2, text="Anti-ship", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(weapons[i].dmg_ship), fill=(255,255,255), font=self.stats_font)
                # Anti-missile
                if (am_type == "Defense missiles"):
                    row3 = self._add_coords_(row2, self.stat_vertical_sep)
                    drawer.text(xy=row3, text="Anti-missile", fill=(255,255,255), font=self.stats_font)
                    drawer.text(xy=self._add_coords_(row3, number_dsplc), text=str(weapons[i].dmg_missile), fill=(255,255,255), font=self.stats_font)

            if isinstance(weapons[i], Ewar):
                drawer.text(xy=startcoords, text="Ewar suite", fill=(255,255,255), font=self.sub_title_font)

            if isinstance(weapons[i], CIWS):
                # Title
                drawer.text(xy=startcoords, text="CIWS", fill=(255,255,255), font=self.sub_title_font)
                # Anti-missile
                drawer.text(xy=statstart, text="Anti-missile", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(weapons[i].dmg_missile), fill=(255,255,255), font=self.stats_font)
                # Anti-ship
                row2 = self._add_coords_(statstart, self.stat_vertical_sep)
                drawer.text(xy=row2, text="Anti-ship", fill=(255,255,255), font=self.stats_font)
                drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(weapons[i].dmg_ship), fill=(255,255,255), font=self.stats_font)



            i += 1

    def _draw_missile_(self, startcoords, number_dsplc):
        pass

    def _add_coords_(self, first, second):
        return tuple(sum(x) for x in zip(first, second))



