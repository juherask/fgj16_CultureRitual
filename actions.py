
#Funktio ajetaan jokaiselle populaation jasenelle tietyin aikavalein
#
def threshold_actions(target, action_lib):
    #Toiminto kohdatessa toisen kotikylan ihmisen
    initAct = target.propensity_library

    #propensityLibrary koostuu string-integer -pareista,
    #string on emootion nimi, integer valilla 0...100

    #Jos emootion arvo on suurempi kuin toimintakynnys, toiminta
    #toteutuu kahden ihmisen kohdatessa
    
    #Toiminto kohdatessa vieraan kylan ihmisen
    #actionLib = {
    #    #Turvallisuuden vallitessa ihmiset lisaantyvat kohdatessaan   
    #    "safety":multiply(),
    #    #Pelon vallitessa ihmiset pakenevat toisiaan
    #    "fear":flee(),
    #    #Huvittuneisuuden vallitessa ihmiset lahestyvat toisiaan
    #    "amusement":attract(),
    #    #Itseluottamus = ihmiset pysahtyvat kohdatessaan toisensa
    #    "confidence":confront(),
    #    #vastuuttomuus = toimintakynnyksen madaltaminen
    #    "hostility":violence()
    #    }
    
    for currentEmotion in initAct:
        #vastuullisuus = toimintakynnyksen nostaminen
        if initAct[currentEmotion] > initAct["responsibility"]:
            action = action_lib[currentEmotion]
            #print("do action", currentEmotion)
            action()

safetyMod = {"Music":2,
            "Dance":5,
            "Psychedelics":3,
            "Social isolation":-5,
            "Animal sacrifice":-3,
            "Human sacrifice":-7,
            "Plant sacrifice":1,
            "Food sacrifice":0}

fearMod = {"Music":-2,
            "Dance":-5,
            "Psychedelics":-3,
            "Social isolation":5,
            "Animal sacrifice":3,
            "Human sacrifice":7,
            "Plant sacrifice":-1,
            "Food sacrifice":0}

confidenceMod = {"Music":8,
                 "Dance":6,
                 "Psychedelics":-8,
                 "Social isolation":10,
                 "Animal sacrifice":6,
                 "Human sacrifice":4,
                 "Plant sacrifice":0,
                 "Food sacrifice":-5}

amusementMod = {"Music":2,
                 "Dance":4,
                 "Psychedelics":5,
                 "Social isolation":-10,
                 "Animal sacrifice":6,
                 "Human sacrifice":4,
                 "Plant sacrifice":-2,
                 "Food sacrifice":-3}

responsibilityMod = {"Music":-6,
                 "Dance":-4,
                 "Psychedelics":-5,
                 "Social isolation":-10,
                 "Animal sacrifice":6,
                 "Human sacrifice":4,
                 "Plant sacrifice":-2,
                 "Food sacrifice":-3}

hostilityMod = {"Music":10,
                 "Dance":7,
                 "Psychedelics":9,
                 "Social isolation":4,
                 "Animal sacrifice":-2,
                 "Human sacrifice":8,
                 "Plant sacrifice":3,
                 "Food sacrifice":-2}



def influence_population(targetPopulation, imp):
    #Kaydaan fyysisten implementaatioiden lista lapi ja
    #lasketaan, miten populaation emootiot muuttuvat
    targetPopulation.propensity_library["safety"] += safetyMod[imp]
    targetPopulation.propensity_library["fear"] += fearMod[imp]
    targetPopulation.propensity_library["amusement"]   += amusementMod[imp]
    targetPopulation.propensity_library["confidence"] += confidenceMod[imp]
    targetPopulation.propensity_library["responsibility"]   += responsibilityMod[imp]
    targetPopulation.propensity_library["hostility"]   += responsibilityMod[imp]
    
def violence_happened(senderPopulation,targetPopulation):

    #Such generosity weakens the giver and the recipient.

    senderPopulation.propensity_library["safety"] -= 2
    senderPopulation.propensity_library["fear"] += 7
    senderPopulation.propensity_library["amusement"]   -= 10
    senderPopulation.propensity_library["confidence"]   -= 3
    senderPopulation.propensity_library["responsibility"]   -= 5
    senderPopulation.propensity_library["hostility"]   -= 3
    
    targetPopulation.propensity_library["safety"] -= 10
    targetPopulation.propensity_library["fear"] += 10
    targetPopulation.propensity_library["amusement"]   -= 10
    targetPopulation.propensity_library["confidence"] -= 3
    targetPopulation.propensity_library["responsibility"]   += 5
    targetPopulation.propensity_library["hostility"]   += 9

def reproduction_happened(senderPopulation, targetPopulation):
    
    senderPopulation.propensity_library["safety"] += 2
    senderPopulation.propensity_library["fear"] -= 6
    senderPopulation.propensity_library["amusement"]   += 5
    senderPopulation.propensity_library["confidence"] += 3
    senderPopulation.propensity_library["responsibility"]   += 10
    senderPopulation.propensity_library["hostility"]   -= 3
    
    targetPopulation.propensity_library["safety"] += 2
    targetPopulation.propensity_library["fear"] -= 6
    targetPopulation.propensity_library["amusement"]   += 5
    targetPopulation.propensity_library["confidence"] += 3
    targetPopulation.propensity_library["responsibility"]   += 10
    targetPopulation.propensity_library["hostility"]   -= 3

    

    
