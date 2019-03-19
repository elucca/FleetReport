from PIL import Image, ImageDraw, ImageFont
from PIL.Image import LANCZOS
from application.dataIO.cardgenerator.card_size import CardSize
from application.dataIO.cardgenerator.statcolor import StatColor, Stat
from application.weapons.models import *

# Is there a reason for this to be a class?
class CardGenerator():

    def __init__(self):
        pass

    def generate_card(self, ship, card_size):
        # Generates and saves a card for the ship. Returns the file path of the saved card.

        self._init_card_()

        self.stat_vertical_sep = (0,70)

        drawer = ImageDraw.Draw(self.card)
        colors = StatColor()
        
        # Draw title and cost. If ship is command-capable, move title a little way to the right and draw command icon.
        if ship.command_capable:
            drawer.text(xy=(198, 35), text=ship.name, fill=(255,255,255), font=self.ship_title_font)
            self.card.alpha_composite(self.cmd_star, (95,71))
        else:
            drawer.text(xy=(93, 35), text=ship.name, fill=(255,255,255), font=self.ship_title_font)

        drawer.text(xy=(880, 35), text=str(ship.cost)+" pts", fill=(255,255,255), font=self.ship_title_font)

        # Draw ship image, integrity and armor stats
        self._draw_ship_(ship, drawer, colors)

        # Draw subsection titles
        drawer.text(xy=(72,623), text="Propulsion", fill=(255,255,255), font=self.sub_title_font)
        drawer.text(xy=(770,623), text="Evasion", fill=(255,255,255), font=self.sub_title_font)

        # Draw common stats
        col1_start = (72,700)
        col2_start = (770,700)
        # Displacement for actual numbers, add to stat title coords
        number_dsplc = (340,0)

        # Prop type
        drawer.text(xy=col1_start, text="Type", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(col1_start, number_dsplc), text=ship.propulsion_type, fill=(255,255,255), font=self.stats_font)
        
        # Move
        col1_row2 = self._add_coords_(col1_start, self.stat_vertical_sep)
        drawer.text(xy=(col1_row2), text="Move", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(col1_row2, number_dsplc), text=str(ship.move), fill=colors.color(Stat.MOVE, ship.move), font=self.stats_font)
        
        # Delta-v
        col1_row3 = self._add_coords_(col1_row2, self.stat_vertical_sep)
        drawer.text(xy=col1_row3, text="Delta-v", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(col1_row3, number_dsplc), text=str(ship.delta_v), fill=colors.color(Stat.DELTA_V, ship.delta_v), font=self.stats_font)
        
        # Place evasion numbers further right if they are made of only one character. Bad hack,
        # since it isn't clean as numbers vary in size, and it'll break if the font changes.
        evasion_dsplc = number_dsplc
        if len(str(ship.evasion_active)) == 1:
            evasion_dsplc = (392,0)

        # Evasion passive
        drawer.text(xy=col2_start, text="Passive", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(col2_start, number_dsplc), text=str(ship.evasion_passive), 
        fill=colors.color(Stat.EVASION_PASSIVE, ship.evasion_passive), font=self.stats_font)
        
        # Evasion active
        col2_row2 = self._add_coords_(col2_start, self.stat_vertical_sep)
        drawer.text(xy=col2_row2, text="Active", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(col2_row2, evasion_dsplc), text=str(ship.evasion_active), 
        fill=colors.color(Stat.EVASION_PASSIVE, ship.evasion_passive), font=self.stats_font)
        
        # Evasion endurance stat if ship has a pulse drive
        if "pulse" in ship.propulsion_type or "Pulse" in ship.propulsion_type:
            col2_row3 = self._add_coords_(col2_row2, self.stat_vertical_sep)
            drawer.text(xy=col2_row3, text="Endurance", fill=(255,255,255), font=self.stats_font)
            drawer.text(xy=self._add_coords_(col2_row3, evasion_dsplc), text=str(ship.evasion_endurance), 
            fill=colors.color(Stat.EVASION_ENDURANCE, ship.evasion_endurance), font=self.stats_font)

        self._draw_weapons_(self._get_weapons_(ship), drawer, colors)
        
        # Save file at appropriate scale, and return the file path
        return self._save_card_(ship, card_size)

    def _init_card_(self):
        # Called when self.card generator is instantiated.

        # Load self.card template
        self.card = Image.open("application/dataIO/cardgenerator/assets/templates/card_base_1.png")
        # Load common assets
        self.cmd_star = Image.open("application/dataIO/cardgenerator/assets/images/misc/cmd_star.png")
        self.self_defense_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/self_defense_jamming.png")
        self.cover_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/cover_jamming.png")
        self.high_intensity_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/high_intensity_jamming.png")
        self.defense_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/defense_jamming.png")
        self.missile_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/missile_jamming.png")
        self.comms_jamming = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/comms_jamming.png")
        self.ECCM = Image.open("application/dataIO/cardgenerator/assets/images/ewar icons/eccm.png")       

        # Set fonts
        self.ship_title_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/Oswald-Bold.ttf", 94)
        self.sub_title_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/Oswald-Bold.ttf", 54)
        self.stats_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/Oswald-Bold.ttf", 59)
        self.laser_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/Oswald-Bold.ttf", 62)
        self.laser_endtext_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/Oswald-Bold.ttf", 40)
        self.flavor_font = ImageFont.truetype("application/dataIO/cardgenerator/assets/fonts/CharisSIL-B.ttf", 47)

    def _save_card_(self, ship, card_size):
        # Strip dashes from the ship's name for file name
        ship_name = ship.name.replace('/', '')
        filepath = "application/dataIO/cardgenerator/assets/generated/ship cards/creharr/print/" + ship_name + ".png"

        # Scale image if size is other than default (CardSize.PRINT)
        if card_size == CardSize.WEB:
            self.card = self.card.resize(size=CardSize.WEB.value, resample=Image.LANCZOS)
            filepath = "application/dataIO/cardgenerator/assets/generated/ship cards/creharr/web/" + ship_name + ".png"

        self.card.save(filepath)

        return filepath

    def _draw_ship_(self, ship, drawer, colors):
        # Because the placement of the ship image and the armor numbers around it is fairly ad-hoc, it needs to be
        # manually defined for each ship. Unknown ship won't have an image, and will have the stats in default positions.
        # A really bad thing here is that it breaks if a ship's name is changed. Ships should probably have some
        # static identifier and its name should just be flavor text.

        # Set default coordinates for ship stats
        self.center_coords = (635,360)
        self.integrity_coords = self._add_coords_(self.center_coords, (-20,5))
        self.ship_coords = self._add_coords_(self.center_coords, (-400,-40))
        self.armor_front_coords = self._add_coords_(self.center_coords, (-420,0))
        self.armor_sides_coords = self._add_coords_(self.center_coords, (0,-120))
        self.armor_back_coords = self._add_coords_(self.center_coords, (355,0))

        self.ship_image = None

        # Set image & pretty coordinates for known ships
        self._set_pretty_coords_(ship)

        # Draw ship and integrity. If image is missing, draw integrity below "Image missing" in white.
        if self.ship_image is not None:
            self.card.alpha_composite(self.ship_image, self.ship_coords)
            drawer.text(xy=self.integrity_coords, text=str(ship.integrity), fill=(0,0,0), font=self.laser_font)
        else:
            drawer.text(xy=self._add_coords_(self.center_coords, (-190,0)), text="<Image missing>", fill=(185,185,185), font=self.stats_font)
            drawer.text(xy=self._add_coords_(self.integrity_coords, (0, 80)), text=str(ship.integrity), fill=(255,255,255), font=self.laser_font)

        # Draw armor. Append "P" on the armor facing which is the ship's primary facing.        
        if ship.primary_facing == "Front":
            armor_front = "P" + str(ship.armor_front)
            armor_sides = str(ship.armor_sides)
            armor_back = str(ship.armor_back)
        if ship.primary_facing == "Side" or ship.primary_facing == "Sides":
            armor_front = str(ship.armor_front)
            armor_sides = "P" + str(ship.armor_sides)
            armor_back = str(ship.armor_back)
        if ship.primary_facing == "Back" or ship.primary_facing == "Rear":
            armor_front = str(ship.armor_front)
            armor_sides = str(ship.armor_sides)
            armor_back = "P" + str(ship.armor_back)

        drawer.text(xy=self.armor_front_coords, text=armor_front, fill=colors.color(Stat.ARMOR, ship.armor_front), font=self.stats_font)
        drawer.text(xy=self.armor_sides_coords, text=armor_sides, fill=colors.color(Stat.ARMOR, ship.armor_sides), font=self.stats_font)
        drawer.text(xy=self.armor_back_coords, text=armor_back, fill=colors.color(Stat.ARMOR, ship.armor_back), font=self.stats_font)

    def _get_weapons_(self, ship):
        # Returns the ship's weapons in the order required for ship cards
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

    def _get_ewar_abilities_(self, ewar):
        # Returns the ewar suite's abilities in the order required for ship cards
        # This is currently very inefficient, iterating through all abilities until the desired one is found.
        # This is also very brittle, since it requires the db to have these particular names for the abilities.
        # That will need to be improved.
        abilities = []
        ability = ""

        for ability in ewar.abilities:
            if ability.ability == "ECCM":
                abilities.insert(0, ability)

        for ability in ewar.abilities:
            if ability.ability == "Comms jamming":
                abilities.insert(0, ability)

        for ability in ewar.abilities:
            if ability.ability == "Missile jamming":
                abilities.insert(0, ability)        
        
        for ability in ewar.abilities:
            if ability.ability == "Defense jamming":
                abilities.insert(0, ability)

        for ability in ewar.abilities:
            if ability.ability == "High-intensity jamming":
                abilities.insert(0, ability)     

        for ability in ewar.abilities:
            if ability.ability == "Cover jamming":
                abilities.insert(0, ability)

        for ability in ewar.abilities:
            if ability.ability == "Self-defense jamming":
                abilities.insert(0, ability)

        return abilities
        
    def _draw_weapons_(self, weapons, drawer, colors):
        i = 0
        while i < len(weapons):
            if i == 0:
                startcoords = (90,1015)
            if i == 1:
                startcoords = (710,1015)
            if i == 2:
                startcoords = (710,1594)

            # Draw weapon flavor text (common to all weapon types)
            flavorcoords = self._add_coords_(startcoords, (0,65))
            drawer.text(xy=flavorcoords, text=weapons[i].name, fill=(255,255,255), font=self.flavor_font)
            # Coords for first stat row (separation between flavor text and stats)
            statstart = self._add_coords_(flavorcoords, (0,90))
            # Displacement for the stat numbers themselves, add to the starting position
            number_dsplc = (360,0)

            if isinstance(weapons[i], Laser):
                laser = weapons[i]
                self._draw_laser_(laser, drawer, colors, startcoords, statstart, number_dsplc)

            if isinstance(weapons[i], Missile):
                missile = weapons[i]
                self._draw_missile_(missile, drawer, colors, startcoords, statstart, number_dsplc)

            if isinstance(weapons[i], AreaMissile):
                area_missile = weapons[i]
                self._draw_area_missile_(area_missile, drawer, colors, startcoords, statstart, number_dsplc)                

            if isinstance(weapons[i], Ewar):
                ewar = weapons[i]
                self._draw_ewar_(ewar, drawer, colors, startcoords, statstart)

            if isinstance(weapons[i], CIWS):
                ciws = weapons[i]
                self._draw_CIWS_(ciws, drawer, colors, startcoords, statstart, number_dsplc)

            i += 1

    def _draw_laser_(self, laser, drawer, colors, startcoords, statstart, number_dsplc):
        if laser.turreted:
            drawer.text(xy=startcoords, text="Turreted c-beam", fill=(255,255,255), font=self.sub_title_font)
        else:
            drawer.text(xy=startcoords, text="C-beam", fill=(255,255,255), font=self.sub_title_font)

        # Get colors (dmg based on range 3 which all lasers have)
        am_color = colors.color(Stat.LASER_AM, laser.laser_dmg_missile)
        rangepoint3 = laser.rangepoints[len(laser.rangepoints) - 1]
        dmg_color = colors.color(Stat.LASER_DMG, rangepoint3.dmg)
        
        # Anti-missile
        antimissilecoords = self._add_coords_(startcoords, (0,150))
        drawer.text(xy=antimissilecoords, text="Anti-missile", fill=(255,255,255), font=self.sub_title_font)
        drawer.text(xy=self._add_coords_(antimissilecoords, (300,0)), text=str(laser.laser_dmg_missile), fill=(am_color), font=self.stats_font)
        
        # Range table
        rangestartcoords = self._add_coords_(antimissilecoords, (0,100))
        
        # Calculate accuracy for first range point such that range 3 is 100%
        accuracy = 100 - (len(laser.rangepoints) - 1) * 10
        rangecoords = rangestartcoords
        laser_vertical_sep = (0,80)

        for rangepoint in laser.rangepoints:
            # Range
            drawer.text(xy=rangecoords, text=str(rangepoint.lrange), fill=(255,255,255), font=self.laser_font)
            # Accuracy
            coords = self._add_coords_(rangecoords, (110,0))
            drawer.text(xy=coords, text=str(accuracy) + "%", fill=(222,222,222), font=self.laser_font)
            # Damage
            coords = self._add_coords_(coords, (185,0))
            drawer.text(xy=coords, text=str(rangepoint.dmg), fill=dmg_color, font=self.laser_font)           

            rangecoords = self._add_coords_(rangecoords, laser_vertical_sep)
            accuracy += 10

        # "+10 per hex" accuracy end text
        endtextcoords = self._add_coords_(rangecoords, (80,10))
        drawer.text(xy=endtextcoords, text="+10 per hex", fill=(185,185,185), font=self.laser_endtext_font)

    def _draw_missile_(self, missile, drawer, colors, startcoords, statstart, number_dsplc):
        # Title
        drawer.text(xy=startcoords, text="Anti-ship missiles", fill=(255,255,255), font=self.sub_title_font)
        
        # Volley
        drawer.text(xy=statstart, text="Volley", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(missile.volley), 
        fill=colors.color(Stat.MISSILE_VOLLEY, missile.volley), font=self.stats_font)
        
        # Stores
        row2 = self._add_coords_(statstart, self.stat_vertical_sep)
        drawer.text(xy=row2, text="Stores", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(missile.stores), 
        fill=colors.color(Stat.MISSILE_STORES, missile.stores), font=self.stats_font)

    def _draw_area_missile_(self, area_missile, drawer, colors, startcoords, statstart, number_dsplc):
        # Differentiate between defense and attack missiles.
        if not area_missile.dmg_missile:
            am_type = "Assault missiles"
        else:
            am_type = "Defense missiles"

        # Title
        if not area_missile.dmg_missile:
            drawer.text(xy=startcoords, text=am_type, fill=(255,255,255), font=self.sub_title_font)
        else:
            drawer.text(xy=startcoords, text=am_type, fill=(255,255,255), font=self.sub_title_font)
        
        # Range
        drawer.text(xy=statstart, text="Range", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(area_missile.am_range), 
        fill=colors.color(Stat.AM_RANGE, area_missile.am_range), font=self.stats_font)
        
        # Anti-ship
        row2 = self._add_coords_(statstart, self.stat_vertical_sep)
        drawer.text(xy=row2, text="Anti-ship", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(area_missile.dmg_ship), 
        fill=(colors.color(Stat.AM_DMG_SHIP, area_missile.dmg_ship)), font=self.stats_font)
        
        # Anti-missile
        if am_type == "Defense missiles":
            row3 = self._add_coords_(row2, self.stat_vertical_sep)
            drawer.text(xy=row3, text="Anti-missile", fill=(255,255,255), font=self.stats_font)
            drawer.text(xy=self._add_coords_(row3, number_dsplc), text=str(area_missile.dmg_missile), 
            fill=colors.color(Stat.AM_DMG_MISSILE, area_missile.dmg_missile), font=self.stats_font)

    def _draw_ewar_(self, ewar, drawer, colors, startcoords, statstart):
        drawer.text(xy=startcoords, text="Ewar suite", fill=(255,255,255), font=self.sub_title_font)

        abilities = self._get_ewar_abilities_(ewar)
        currentpos = self._add_coords_(startcoords, (0,245))
        rangepos = self._add_coords_(currentpos, (28,-95))
        icon_hor_dsplc = (120,0)
        icon_ver_dpslc = (0, 110)

        # This inner method is used to avoid copypaste in the main method body
        def draw_ability(i, ability, icon):
            # Range. Hacky (and breaks if fonts change), but if it's two characters move it left a bit to stay centered.
            if len(str(abilities[i].erange)) == 2:
                drawer.text(xy=self._add_coords_(rangepos, (-12,0)), text=str(abilities[i].erange), fill=(222,222,222), font=self.stats_font)
            else:            
                drawer.text(xy=rangepos, text=str(abilities[i].erange), fill=(222,222,222), font=self.stats_font)
            # Icon
            self.card.alpha_composite(icon, currentpos)
            # Adjust position for next icon
            self._add_coords_(currentpos, icon_hor_dsplc)
            # If the next ability is the same, draw it below the current one and skip ahead.
            if i + 1 < len(abilities) and abilities[i + 1].ability == ability:
                self.card.alpha_composite(icon, self._add_coords_(currentpos, icon_ver_dpslc))
                i += 1

            return i + 1

        i = 0
        while i < len(abilities):
            if abilities[i].ability == "Self-defense jamming":
                icon = self.self_defense_jamming
                i = draw_ability(i, "Self-defense jamming", icon)
            elif abilities[i].ability == "Cover jamming":
                icon = self.cover_jamming
                i = draw_ability(i, "Cover jamming", icon)
            elif abilities[i].ability == "High-intensity jamming":
                icon = self.high_intensity_jamming
                i = draw_ability(i, "High-intensity jamming", icon)
            elif abilities[i].ability == "Defense jamming":
                icon = self.defense_jamming
                i = draw_ability(i, "Defense jamming", icon)
            elif abilities[i].ability == "Missile jamming":
                icon = self.missile_jamming
                i = draw_ability(i, "Missile jamming", icon)
            elif abilities[i].ability == "Comms jamming":
                icon = self.comms_jamming
                i = draw_ability(i, "Comms jamming", icon)
            elif abilities[i].ability == "ECCM":
                icon = self.ECCM
                i = draw_ability(i, "ECCM", icon)
            else:
                i += 1

            currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
            rangepos = self._add_coords_(rangepos, icon_hor_dsplc)

    def _draw_CIWS_(self, CIWS, drawer, colors, startcoords, statstart, number_dsplc):
        # Title
        drawer.text(xy=startcoords, text="CIWS", fill=(255,255,255), font=self.sub_title_font)
        
        # Anti-missile
        drawer.text(xy=statstart, text="Anti-missile", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(statstart, number_dsplc), text=str(CIWS.dmg_missile), 
        fill=colors.color(Stat.CIWS_DMG_MISSILE, CIWS.dmg_missile), font=self.stats_font)
        
        # Anti-ship
        row2 = self._add_coords_(statstart, self.stat_vertical_sep)
        drawer.text(xy=row2, text="Anti-ship", fill=(255,255,255), font=self.stats_font)
        drawer.text(xy=self._add_coords_(row2, number_dsplc), text=str(CIWS.dmg_ship), 
        fill=colors.color(Stat.CIWS_DMG_SHIP, CIWS.dmg_ship), font=self.stats_font)

    # Sets pretty coordinates for ship image and surrounding stats for known ships
    def _set_pretty_coords_(self, ship):
    # This would actually make sense to put in a db table, but it's kinda easier to manipulate
    # the numbers here.
        if (ship.name == "FH/E-946"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/fhe.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-287,-65))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,5))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (0,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-43,-5))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-30,10))

        if (ship.name == "CGp-805"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/805.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-450,-30))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,5))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-157,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-43,-5))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (196,10))

        if (ship.name == "CGw-603"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/603.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-450,-30))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,13))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-160,20))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-20,-5))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (165,20))

        if (ship.name == "B/Pl-659"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/bpl.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-320,-30))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,13))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-15,20))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-20,20))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-5,20))

        if (ship.name == "BCM-645"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/bcm.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-250,-35))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,13))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (25,20))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-20,20))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (20,20))

        if (ship.name == "HAc-B27"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/hac.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-230,-100))
            self.integrity_coords = self._add_coords_(self.center_coords, (110,7))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (50,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (110,15))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-70,10))

        if (ship.name == "LAc-B20"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/lac.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-230,-93))
            self.integrity_coords = self._add_coords_(self.center_coords, (110,7))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (50,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (110,15))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-70,10))

        if (ship.name == "CoGw-761"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/cogw.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-280,-20))
            self.integrity_coords = self._add_coords_(self.center_coords, (-20,13))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (5,20))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-20,10))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-38,20))

        if (ship.name == "CGp-901"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/901.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-450,-35))
            self.integrity_coords = self._add_coords_(self.center_coords, (19,13))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-165,20))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (0,-5))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (175,20))

        if (ship.name == "LAc/E-N2"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/lace.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-230,-93))
            self.integrity_coords = self._add_coords_(self.center_coords, (117,7))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (50,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (117,15))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-70,10))

        if (ship.name == "SuM/E-858"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/sume.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-210,-83))
            self.integrity_coords = self._add_coords_(self.center_coords, (0,7))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (160,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-35,5))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (-80,10))

        if (ship.name == "CL/E-866"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/cle.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-480,-32))
            self.integrity_coords = self._add_coords_(self.center_coords, (-125,5))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-132,12))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (-177,7))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (176,10))

        if (ship.name == "CL/P-921"):
            self.ship_image = Image.open("application/dataIO/cardgenerator/assets/images/ships/creharr/921.png")
            self.ship_coords = self._add_coords_(self.center_coords, (-450,-25))
            self.integrity_coords = self._add_coords_(self.center_coords, (130,5))
            self.armor_front_coords = self._add_coords_(self.armor_front_coords, (-157,10))
            self.armor_sides_coords = self._add_coords_(self.armor_sides_coords, (130,10))
            self.armor_back_coords = self._add_coords_(self.armor_back_coords, (196,10))

    def _add_coords_(self, first, second):
        return tuple(sum(x) for x in zip(first, second))

    def _next_row_(self, currentrow):
        # Returns the start coordinates of the next stat row based on self.stat_vertical_sep
        # Not yet used everywhere, refactor
        return tuple(sum(x) for x in zip(currentrow, self.stat_vertical_sep))

    def _scale_card_(self, card, card_size):
        # Because everything in CardGenerator is defined in pixel coordinates
        pass