
#Funktio ajetaan jokaiselle populaation jäsenelle tietyin aikavälein
#
def ThresholdActions(target,emotionLibrary):
    emotionLibrary = target.emotionLibrary

    #Toiminto kohdatessa toisen kotikylän ihmisen
    initAct = target.propensityLibrary

    #propensityLibrary koostuu string-integer -pareista,
    #string on emootion nimi, integer välillä 0...100

    #Jos emootion arvo on suurempi kuin toimintakynnys, toiminta
    #toteutuu kahden ihmisen kohdatessa
    
    #Toiminto kohdatessa vieraan kylän ihmisen
    actionLib = {
        #Turvallisuuden vallitessa ihmiset lisääntyvät kohdatessaan   
        "safety":multiply(),
        #Pelon vallitessa ihmiset pakenevat toisiaan
        "fear":flee(),
        #Huvittuneisuuden vallitessa ihmiset lähestyvät toisiaan
        "amusement":attract(),
        #Itseluottamus = ihmiset pysähtyvät kohdatessaan toisensa
        "confidence":confront(),
        #vastuuttomuus = toimintakynnyksen madaltaminen
        "hostility":violence()
        }
    
    for currentEmotion in initAct:
        #vastuullisuus = toimintakynnyksen nostaminen
        if initAct[currentEmotion] > initAct["responsibility"]:
            initAct[currentEmotion]
"""
revealLibrary = {"Music":2,
                 "Dance":5,
                 "Psychedelics":3,
                 "Social isolation":-5,
                 "Animal sacrifice":-3,
                 "Human sacrifice":-7,
                 "Plant sacrifice":1,
                 "Food sacrifice":0}

receiveLibrary = {"Music":10,
                 "Dance":7,
                 "Psychedelics":9,
                 "Social isolation":4,
                 "Animal sacrifice":-2,
                 "Human sacrifice":8,
                 "Plant sacrifice":3,
                 "Food sacrifice":-2}

usingLibrary = {"Music":-5,
                 "Dance":7,
                 "Psychedelics":-9,
                 "Social isolation":-5,
                 "Animal sacrifice":7,
                 "Human sacrifice":-6,
                 "Plant sacrifice":8,
                 "Food sacrifice":6}

transformingLibrary = {"Music":2,
                 "Dance":4,
                 "Psychedelics":5,
                 "Social isolation":-10,
                 "Animal sacrifice":6,
                 "Human sacrifice":4,
                 "Plant sacrifice":-2,
                 "Food sacrifice":-3}

reinforcingLibrary = {"Music":8,
                 "Dance":6,
                 "Psychedelics":-8,
                 "Social isolation":10,
                 "Animal sacrifice":6,
                 "Human sacrifice":4,
                 "Plant sacrifice":0,
                 "Food sacrifice":-5}
"""

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



def InfluencePopulation(targetPopulation, physImp):
    #Käydään fyysisten implementaatioiden lista läpi ja
    #lasketaan, miten populaation emootiot muuttuvat
    for imp in physImp:
        targetPopulation.safety += safetyMod[imp]
        targetPopulation.fear += fearMod[imp]
        targetPopulation.amusement += amusementMod[imp]
        targetPopulation.confidence += confidenceMod[imp]
        targetPopulation.responsibility += responsibilityMod[imp]
        targetPopulation.hostility += responsibilityMod[imp]
        
def violenceHappened(senderPopulation,targetPopulation):

    #Such generosity weakens the giver and the recipient.

    senderPopulation.safety += 2
    senderPopulation.fear += 7
    senderPopulation.amusement -= 10
    senderPopulation.confidence -= 3
    senderPopulation.responsibility -= 5
    senderPopulation.hostility -= 3
    
    targetPopulation.safety -= 10
    targetPopulation.fear += 10
    targetPopulation.amusement -= 10
    targetPopulation.confidence -= 3
    targetPopulation.responsibility += 5
    targetPopulation.hostility += 9

def reproductionHappened(senderPopulation, targetPopulation):
    
    senderPopulation.safety += 6
    senderPopulation.fear -= 6
    senderPopulation.amusement += 5
    senderPopulation.confidence += 3
    senderPopulation.responsibility += 10
    senderPopulation.hostility -= 3
    
    targetPopulation.safety += 6
    targetPopulation.fear -= 6
    targetPopulation.amusement += 5
    targetPopulation.confidence += 3
    targetPopulation.responsibility += 10
    targetPopulation.hostility -= 3

    

    
