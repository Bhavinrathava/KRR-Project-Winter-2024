# KKRcade 
A KRR Based Game Recommendation System.

##### Team Members  : Bhavinkumar Rathava, Aaryansh Sahay, Aastha Khatgarh, Deeptej More

#### Our Goal 
Our team is building a Game recommendation system which can find games similar to a game input by user based on a predefined criteria. This tool will use the Companions app for reasoning and uses custom built KRF files to populate the Knowledge Base (KB). 

#### Where do we get our data ?
Wikidata ha 97K game tiles. We are using a subset of this dataset and we are using "genre","platform","inputDevice","gamemode" attributes for each title.

Sample Raw Data extracted from Wikidata via their API. 
```
video_gameLabel,Entities,genre,platform,gameModes,inputDevice
Civilization III,Q2374,turn-based strategy video game; simulation video game; grand strategy wargame; strategy video game; 4X,Microsoft Windows; macOS; Classic Mac OS,hotseat; single-player video game; multiplayer video game,mouse; computer keyboard
```

We automated the KB building process from this raw data using Python Scripts. 

#### Example of Game_Predicates.KRF
```
(isa Game Collection)
(isa Genre Collection)
(isa Platform Collection)
(isa GameMode Collection)
(isa InputDevice Collection)

;;; For Genre of Game
(isa inGenre Predicate) 
(arity inGenre 2)
(arg1isa inGenre Game)
(arg2isa inGenre Genre)
(genlPreds inGenre GameIsOfGenre)
(comment inGenre "(inGenre ?game ?genre) says ?game is in the ?genre genre")

;;; Similarly for other Game Attributes defined in actual file
```


#### Example of Game_Details.KRF

```
;;; Civilization III
(isa Civilization_III Game)
(inGenre Civilization_III turn-based_strategy_video_game)
(onPlatform Civilization_III Microsoft_Windows)
(hasGameMode Civilization_III hotseat)
(withInputDevice Civilization_III mouse)
```

#### The reasoning:

* Recommendation A) Take input game, check if there’s another game in the Knowledge Base which has the same Genre & GameMode and recommend it.
<br>For Ex: If input is CallOfDuty, which has Genre action & GameMode singleplayer, games like Battlefield_Bad_Company will be recommended. Since they share the same Genre & GameMode.
* Recommendation B) Take input game, check if there’s another game in the KB which has the same Genre & InputDevice and recommend it
<br>For Ex: If input is TombRaider, which has Genre adventure & GameMode singpleplayer, games like Knack2 will be recommended. Since they share the same Genre & GameMode.
