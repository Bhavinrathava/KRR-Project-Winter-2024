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

#### Horn Clauses for Game Similarity

```
(in-microtheory GameRecommenderMt)

(<== (sameGenre ?game1 ?game2)(inGenre ?game1 ?genre)(inGenre ?game2 ?genre))
(<== (samePlatform ?game1 ?game2)(onPlatform ?game1 ?platform)(onPlatform ?game2 ?platform))
(<== (sameInputdevice ?game1 ?game2)(withInputDevice ?game1 ?inputdevice)(withInputDevice ?game2 ?inputdevice))
(<== (sameGamemode ?game1 ?game2)(hasGameMode ?game1 ?gamemode)(hasGameMode ?game2 ?gamemode))
;;; similar games
(<== (similarGameIntensity ?inputgame ?outputgame)(sameGenre ?inputgame ?outputgame)(sameGamemode ?inputgame ?outputgame))
(<== (similarGameEffort ?inputgame ?outputgame)(sameInputdevice ?inputgame ?outputgame)(sameGenre ?inputgame ?outputgame))
```