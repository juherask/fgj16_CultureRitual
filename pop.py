from sys import float_info
import actions
from random import randint, choice
from math import sqrt

# ~DEFINES
X = 0
Y = 1

FLEE_SPEED = 5.0
APPROACH_SPEED = -2.0
DISTANCE_CLOSE = 20
MEET_STOP_DURATION = 1.0

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
        self.dv = [0.0,0.0]
        self.sprite = None
        self.procreate_cooldown = 0.0
        self.population = population
        self.propensity_library = population.propensity_library
        self.cached_action_lib = None
        self.anim_frame = randint(0,3)
        self.meet_cooldown = 0.0
        self.dead = False
        self.action_anim_key = None
        self.action_anim_cooldown = 0.0
        
class Population:
    def __init__(self, all_units):
        self.propensity_library = {
            "safety": 100,# randint(7,13),
            "fear": randint(7,13),
            "amusement": randint(7,13),
            "confidence": randint(7,13),
            "responsibility" : 50,# randint(7,13),
            "hostility": randint(7,13)}
        
        self.all_units = all_units
        

    def procreate_if_can(self, unit):
        d, closest_unit = distance_to_closest_unit(unit, self.all_units)
        unit.dv = [0.0,0.0]
        if (d<DISTANCE_CLOSE and unit.procreate_cooldown==0 and closest_unit.procreate_cooldown==0):
            
            closest_unit.dv = [0.0,0.0]
            
            new_unit = Unit(unit.population)
            new_unit.position = [(unit.position[X]+closest_unit.position[X])/2,
                                 (unit.position[Y]+closest_unit.position[X])/2]
            new_unit.sprite = unit.sprite
            new_unit.procreate_cooldown = 1.5
            
            unit.procreate_cooldown = 1.0
            closest_unit.procreate_cooldown = 1.0
            self.all_units.append(new_unit)
            
            #print(unit, closest_unit, "procriates at", new_unit.position)
        
    def flee_or_approach_if_should(self, unit, speed):
        min_d, min_closest = distance_to_closest_unit(unit, self.all_units)
        dx, dy = (unit.position[X]-min_closest.position[X],
                  unit.position[Y]-min_closest.position[Y])
                 
        if min_d<0.01:
            min_d = sqrt(2)
            dx = choice([-1,1])
            dy = choice([-1,1])
        
        unit.dv = [0.0,0.0]
        if unit.procreate_cooldown>1.0:
            pass # children do not move (realism? yeah right)
        elif min_d<200 and (speed>0 or (speed<0 and min_d>10)):
            unit.dv = [dx/min_d*speed,
                       dy/min_d*speed]
            print(unit.dv)
            
            unit.position[X] += unit.dv[X]
            unit.position[Y] += unit.dv[Y]
           
            #print(unit, "at", unit.position, "flees/approaces", min_closest, "at", min_closest.position, "by", unit.dv)
    
    def stop_when_close_then_wait():
        d, closest_unit = distance_to_closest_unit(unit, self.all_units)
        
        if unit.meet_cooldown==0.0 and d<DISTANCE_CLOSE:
            unit.dv = [0.0,0.0]
            unit.meet_cooldown = MEET_STOP_DURATION
        
    def kill_whomever_is_close(self, unit):
        d, closest_unit = distance_to_closest_unit(unit, self.all_units)
        
        if unit.procreate_cooldown>1.0:
            pass # children do not kill
        else:
            
            unit.position[X] = unit.position[X]+choice([-1,1])
            unit.position[Y] = unit.position[Y]+choice([-1,1])
    
    def act(self):
        for unit in self.all_units:
            if unit.action_anim_cooldown>0.0:
                continue
            if unit.population != self:
                continue # do a population at the time
                
            # TODO: FOR SOME bizarro reason I cannot fanthom. caching
            #  does not work. Well, it is an useless optimizaiton probably.
            #action_lib = None
            #if unit.cached_action_lib==None:
            action_lib = {
                #Turvallisuuden vallitessa ihmiset lisaantyvat kohdatessaan   
                "safety": (lambda: self.procreate_if_can(unit)),
                #Pelon vallitessa ihmiset pakenevat toisiaan
                "fear": (lambda: self.flee_or_approach_if_should(unit, FLEE_SPEED)),
                #Huvittuneisuuden vallitessa ihmiset lahestyvat toisiaan
                "amusement": (lambda: self.flee_or_approach_if_should(unit, APPROACH_SPEED)),
                #Itseluottamus = ihmiset pysahtyvat kohdatessaan toisensa
                "confidence":(lambda: self.stop_when_close_then_wait(unit)),
                #vastuuttomuus = toimintakynnyksen madaltaminen
                "hostility":(lambda: self.kill_whomever_is_close(unit)),
            }
            #    unit.cached_action_lib = action_lib
            #else:
            #    action_lib = unit.cached_action_lib
            
            # Check which action to take accoding to the population state
            actions.threshold_actions(unit,action_lib)

