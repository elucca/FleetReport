from enum import Enum

class StatColor():
    # Note: Doesn't actually fully work yet: For those stats which are strings, need to parse out
    # the integer part and give color based on that.
    # This stuff isn't very readable, which is bad because I might want to change the thresholds.
    # Maybe do something about that.

    def __init__(self):
        pass

    def color(self, statname, stat):
        if statname == Stat.MOVE:
            return self._move_color_(stat)

        if statname == Stat.DELTA_V:
            return self._delta_v_color_(stat)

        if statname == Stat.EVASION_ACTIVE:
            return self._evasion_active_color_(stat)

        if statname == Stat.EVASION_PASSIVE:
            return self._evasion_passive_color_(stat)

        if statname == Stat.EVASION_ENDURANCE:
            return self._evasion_endurance_color_(stat)

        if statname == Stat.ARMOR:
            return self._armor_color_(stat)

        if statname == Stat.LASER_AM:
            return self._laser_am_color_(stat)

        if statname == Stat.LASER_DMG:
            return self._laser_dmg_color_(stat)

        if statname == Stat.MISSILE_VOLLEY:
            return self._missile_volley_color_(stat)

        if statname == Stat.MISSILE_STORES:
            return self._missile_stores_color_(stat)

        if statname == Stat.AM_RANGE:
            return self._am_range_color_(stat)

        if statname == Stat.AM_DMG_SHIP:
            return self._am_dmg_ship_color_(stat)

        if statname == Stat.AM_DMG_MISSILE:
            return self._am_dmg_missile_color_(stat)

        if statname == Stat.CIWS_DMG_MISSILE:
            return self._ciws_dmg_missile_color_(stat)

        if statname == Stat.CIWS_DMG_SHIP:
            return self._ciws_dmg_ship_color_(stat)

    def _move_color_(self, stat):
        if stat < 1:
            return Color.POOR.value
        
        if stat > 1:
            return Color.EXCELLENT.value

        return Color.GOOD.value

    def _delta_v_color_(self, stat):
        if stat <= 6:
            return Color.POOR.value

        if 7 <= stat <= 9:
            return Color.AVERAGE.value
        
        if 10 <= stat <= 12:
            return Color.GOOD.value

        return Color.EXCELLENT

    def _evasion_passive_color_(self, stat):
        # -30 is the average point. Poor is -40 and below. Since values better than -30
        # are rare, anything above that can be considered good. -10 and up are excellent.
        if stat <= -40:
            return Color.POOR.value
        
        if -39 <= stat <= -30:
            return Color.AVERAGE.value

        if -29 <= stat <= -11:
            return Color.GOOD.value

        return Color.EXCELLENT.value

    def _evasion_active_color_(self, stat):
        # 0 is the average point and very common. Anything above +5 and below -5 are good
        # and poor, respectively. Excellent is 20+.
        if stat <= -6:
            return Color.POOR.value
        
        if  -5 <= stat <= 5:
            return Color.AVERAGE.value

        if 6 <= stat <= 19:
            return Color.GOOD.value

        return Color.EXCELLENT.value
    
    def _evasion_endurance_color_(self, stat):
        # 2 is average. Anything above is good. 5 and above is excellent. 1 is poor.
        if stat <= 1:
            return Color.POOR.value

        if stat == 2:
            return Color.AVERAGE.value

        if stat == 3:
            return Color.GOOD.value

        return color.EXCELLENT.value

    def _armor_color_(self, stat):
        # 0 to 9 is poor. 10 to 25 is average. 26 to 34 is good. 35+ is excellent.
        if stat <= 9:
            return Color.POOR.value

        if 10 <= stat <= 25:
            return Color.AVERAGE.value

        if 26 <= stat <= 34:
            return Color.GOOD.value

        return Color.EXCELLENT.value

    def _laser_am_color_(self, stat):
        # 2 is average. Below it is poor. 3 is good. Anything above is excellent.
        if stat <= 1:
            return Color.POOR.value

        if stat == 2:
            return Color.AVERAGE.value

        if stat == 3:
            return Color.GOOD.value

        return Color.EXCELLENT.value

    def _laser_dmg_color_(self, stat):
        # 35 and below is poor. 36 to 45 is average. 46 to to 60 is good. Anything above is excellent.
        if stat <= 35:
            return Color.POOR.value

        if 36 <= stat <= 45:
            return Color.AVERAGE.value

        if 46 <= stat <= 60:
            return Color.GOOD.value

        

    def _missile_volley_color_(self, stat):
        pass

    def _missile_stores_color_(self, stat):
        pass

    def _am_range_color_(self, stat):
        pass

    def _am_dmg_ship_color_(self, stat):
        pass

    def _am_dmg_missile_color_(self, stat):
        pass

    def _ciws_dmg_ship_color_(self, stat):
        pass

    def _ciws_dmg_missile_color_(self, stat):
        pass

class Stat(Enum):
    # These are all the kinds of stats that need colors.
    # The actual values are unimportant, but I can't get auto() to work
    MOVE = "MOVE"
    DELTA_V = "DELTA_V"
    EVASION_PASSIVE = "EVASION_PASSIVE"
    EVASION_ACTIVE = "EVASION_ACTIVE"
    EVASION_ENDURANCE = "EVASION_ENDURANCE"
    ARMOR = "ARMOR"

    LASER_AM = 7
    LASER_DMG = 8

    MISSILE_VOLLEY = 9
    MISSILE_STORES = 10

    AM_RANGE = 11
    AM_DMG_SHIP = 12
    AM_DMG_MISSILE = 13

    CIWS_DMG_SHIP = 14
    CIWS_DMG_MISSILE = 15

class Color(Enum):
    POOR = (255,124,72)
    AVERAGE = (255,249,72)
    GOOD = (73,255,69)
    EXCELLENT = (72,249,255)