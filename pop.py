from sys import float_info
import actions
from random import randint
from math import sqrt

# ~DEFINES
X = 0
Y = 1

FLEE_SPEED = 5.0
APPROACH_SPEED = -2.0

def distance_to_closest_unit(from_unit, units):
    min_d = float_info.max
    min_d_i = None
    for i, unit in enumerate(units):
        d = sqrt((from_unit.position[X]-unit.position[X])**2+(from_unit.position[Y]-unit.position[Y])**2)
        if (unit!=from_unit and d<min_d):
            min_d = d
            min_d_i = i
            
    return min_d, units[min_d_i]

class Unit:
    def __init__(self, population):
        self.position = [0,0]
        self.sprite = None
        self.procreate_cooldown = 0.0
        self.population = population
        self.propensity_library = population.propensity_library
    
        
class Population:
    def __init__(self):
        self.propensity_library = {
            "safety": randint(7,13),
            "fear": randint(7,13),
            "amusement": randint(7,13),
            "confidence": randint(7,13),
            "responsibility" : randint(7,13),
            "hostility": randint(7,13)}
        
        # todo: unit already knows in which pos
        self.units = []
        
        self.other_populations = []

    def procreate_if_can(self, unit):
        d, closest_unit = distance_to_closest_unit(unit, self.units)
        if (d<40 and unit.procreate_cooldown==0 and closest_unit.procreate_cooldown==0):
            new_unit = Unit(unit.population)
            new_unit.position = [(unit.position[X]+closest_unit.position[X])/2,
                                 (unit.position[Y]+closest_unit.position[X])/2]
            new_unit.sprite = unit.sprite
            new_unit.procreate_cooldown = 15.0
            
            unit.procreate_cooldown = 1.0
            closest_unit.procreate_cooldown = 1.0
            self.units.append(new_unit)
            
            print(unit, closest_unit, "procriates at", new_unit.position)
    
    def flee_or_approach_if_should(self, unit, speed):
        min_d = float_info.max
        min_closest = None
        
        for pop in self.other_populations+[self]:
            d, closest = distance_to_closest_unit(unit, pop.units)
            if d<min_d:
                min_d = d
                min_closest = closest
        
        if min_d<200 and (speed>0 or (speed<0 and min_d>10)):
           unit.position[X] += (unit.position[X]-min_closest.position[X])/min_d*speed
           unit.position[Y] += (unit.position[Y]-min_closest.position[Y])/min_d*speed
           
           print(unit, "flees/approaces", min_closest)
    
    def jitter(self, unit):
        unit.position[X] = unit.position[X]+randint(-1,1)
        unit.position[Y] = unit.position[Y]+randint(-1,1)
    
    def act(self):
        for unit in self.units:
            action_lib = {
                #Turvallisuuden vallitessa ihmiset lisääntyvät kohdatessaan   
                "safety": (lambda: self.procreate_if_can(unit)),
                #Pelon vallitessa ihmiset pakenevat toisiaan
                "fear": (lambda: self.flee_or_approach_if_should(unit, FLEE_SPEED)),
                #Huvittuneisuuden vallitessa ihmiset lähestyvät toisiaan
                "amusement": (lambda: self.flee_or_approach_if_should(unit, APPROACH_SPEED)),
                #Itseluottamus = ihmiset pysähtyvät kohdatessaan toisensa
                "confidence":(lambda: self.jitter(unit)),
                #vastuuttomuus = toimintakynnyksen madaltaminen
                "hostility":(lambda: self.jitter(unit)),
            }
            
            actions.threshold_actions(unit,action_lib)

