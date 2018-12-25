from PIL import Image, ImageDraw, ImageFont
from application.cardgenerator.card_size import CardSize
from application.cardgenerator.statcolor import StatColor, Stat
from application.weapons.models import *

class CardGenerator():

    def __init__(self, card_size):
        self.init_card(card_size)

    def generate_card(self, ship):
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
        
        # Bad hack: Displace active evasion and endurance more to the right to align with passive.
        # Only works right if passive is a minus sign and two digits, which it currently always is,
        # but...
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
        if "pulse" or "Pulse" in ship.propulsion_type:
            col2_row3 = self._add_coords_(col2_row2, self.stat_vertical_sep)
            drawer.text(xy=col2_row3, text="Endurance", fill=(255,255,255), font=self.stats_font)
            drawer.text(xy=self._add_coords_(col2_row3, evasion_dsplc), text=str(ship.evasion_endurance), 
            fill=colors.color(Stat.EVASION_ENDURANCE, ship.evasion_endurance), font=self.stats_font)

        self._draw_weapons_(self._get_weapons_(ship), drawer, colors)

        self.card.save("application/cardgenerator/assets/result.png")

    def init_card(self, card_size):
        # Called when self.card generator is instantiated. Can also be called again to change the self.card size.
        # This method doesn't actually use the self.card size yet.

        # Load self.card template
        self.card = Image.open("application/cardgenerator/assets/templates/card_base_1.png")
        # Load common assets
        self.cmd_star = Image.open("application/cardgenerator/assets/images/misc/cmd_star.png")
        self.self_defense_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/self_defense_jamming.png")
        self.cover_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/cover_jamming.png")
        self.high_intensity_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/high_intensity_jamming.png")
        self.defense_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/defense_jamming.png")
        self.missile_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/missile_jamming.png")
        self.comms_jamming = Image.open("application/cardgenerator/assets/images/ewar icons/comms_jamming.png")
        self.ECCM = Image.open("application/cardgenerator/assets/images/ewar icons/eccm.png")       

        # Set fonts
        self.ship_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 94)
        self.sub_title_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 54)
        self.stats_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 59)
        self.laser_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 62)
        self.laser_endtext_font = ImageFont.truetype("application/cardgenerator/assets/fonts/Oswald-Bold.ttf", 40)
        self.flavor_font = ImageFont.truetype("application/cardgenerator/assets/fonts/CharisSIL-B.ttf", 47)

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
            if ability.ability == "Missile jamming":
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
        while i < 3:
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
            fill=coloros.color(Stat.AM_DMG_MISSILE, area_missile.dmg_missile), font=self.stats_font)

    def _draw_ewar_(self, ewar, drawer, colors, startcoords, statstart):
        drawer.text(xy=startcoords, text="Ewar suite", fill=(255,255,255), font=self.sub_title_font)

        abilities = self._get_ewar_abilities_(ewar)
        currentpos = self._add_coords_(startcoords, (0,245))
        rangepos = self._add_coords_(currentpos, (28,-95))
        icon_hor_dsplc = (120,0)
        icon_ver_dpslc = (0, 110)

        # This inner method is used to avoid copypaste in the main method body
        def draw_ability(i, ability, icon):
            # Range
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
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "Cover jamming":
                icon = self.cover_jamming
                i = draw_ability(i, "Cover jamming", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "High-intensity jamming":
                icon = self.high_intensity_jamming
                i = draw_ability(i, "High-intensity jamming", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "Defense jamming":
                icon = self.defense_jamming
                i = draw_ability(i, "Defense jamming", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "Missile jamming":
                icon = self.missile_jamming
                i = draw_ability(i, "Missile jamming", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "Comms jamming":
                icon = self.comms_jamming
                i = draw_ability(i, "Comms jamming", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            elif abilities[i].ability == "ECCM":
                icon = self.ECCM
                i = draw_ability(i, "ECCM", icon)
                currentpos = self._add_coords_(currentpos, icon_hor_dsplc)
                rangepos = self._add_coords_(rangepos, icon_hor_dsplc)
            else:
                i += 1            

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
    
    def _add_coords_(self, first, second):
        return tuple(sum(x) for x in zip(first, second))

    def _next_row_(self, currentrow):
        # Returns the start coordinates of the next stat row based on self.stat_vertical_sep
        # Not yet used everywhere, refactor
        return tuple(sum(x) for x in zip(currentrow, self.stat_vertical_sep))

