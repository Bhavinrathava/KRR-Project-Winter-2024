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

#### Example of Predicate.KRF
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
#### Example of GamePredicatesPop.krf

```
 (in-microtheory GameRecommenderMt)
 
 ( isa Genre genre_postapocalypticvideogame ) 
 ( isa Genre genre_combatflightsimulatorgame ) 
 ( isa Genre genre_simulationgame ) 
 ( isa Genre genre_war ) 
 ( isa Genre genre_tabletopgame ) 
 ( isa Genre genre_mechsimulationgame ) 
 ( isa Genre genre_dramaanimeandmanga ) 
 ( isa Genre genre_rallying ) 
 ( isa Genre genre_shogivideogame ) 
 ( isa Genre genre_shootemup ) 
 ( isa Genre genre_Rocksanddiamondsvideogame ) 

```

#### Example of GameDetailsPop.KRF

```
;;; Civilization III
(isa Civilization_III Game)
(inGenre Civilization_III turn-based_strategy_video_game)
(onPlatform Civilization_III Microsoft_Windows)
(hasGameMode Civilization_III hotseat)
(withInputDevice Civilization_III mouse)
```

#### The reasoning:

We are recommending game based on 2 criterion : 

- Same Game Intensity : 
    - This matches games based on same Genre and same Game Modes for different games

- Same Game Effort : 
    - THis matches games based on Same Genre and Same Platform 

Our horn clause is defined as follows : 

```

(in-microtheory GameRecommenderMt)

(<== (sameGenre ?game1 ?game2)
	(inGenre ?game1 ?genre)
	(inGenre ?game2 ?genre)
    (different ?game1 ?game2)
)

(<== (samePlatform ?game1 ?game2)
	(onPlatform ?game1 ?platform)
	(onPlatform ?game2 ?platform)
    (different ?game1 ?game2)
)

(<== (sameInputdevice ?game1 ?game2)
	(withInputDevice ?game1 ?inputdevice)
	(withInputDevice ?game2 ?inputdevice)
    (different ?game1 ?game2)
)

(<== (sameGamemode ?game1 ?game2)
	(hasGameMode ?game1 ?gamemode)
	(hasGameMode ?game2 ?gamemode)
    (different ?game1 ?game2)
)

; ; ; similar games

(<== (similarGameIntensity ?inputgame ?outputgame)
	(sameGenre ?inputgame ?outputgame)
	(sameGamemode ?inputgame ?outputgame)
    (different ?inputgame ?outputgame)
)

(<== (similarGameEffort ?inputgame ?outputgame)
	(samePlatform ?inputgame ?outputgame)
	(sameGenre ?inputgame ?outputgame)
	(different ?inputgame ?outputgame)
)

```


#### Project Structure : 

- Use AutoScrapper.py to generate the raw data CSV 
- Generate the predicates for use in the KB files and define the fields you want to use in this recommendation engine 
- Generate the definitions of various attributes like genres, Platforms etc using the generatePredicateDefinition.py 
- Generate the actual game details for each game using genGameDetails.py
- Hand craft the Horn clauses and test them in companions app. 

#### How to use this project ? 

- You can expands the fields to fetch by modifying code in the autoScrapper.py to get extended datasource to build upon. 
- To add New fields, first define them in the Predicate.krf 
- Then you can modify the code in generatePredicateDefinition.py to create definitions for your new field attribute. 
- Then you modify the code inside genGameDetails.py to include the field you just added and populate it for each game. 
- You can extend the rules in the HornClause.krf to add any new rules that you want to recommend the games based on. 
- You can then install Companions app on your device. 
-Load up the KRF Files in this order : Predicate.krf, gamePredicatesPop.krf, GameDetailsPop.krf, Hornclause.krf

- Then query using the format : (sameGameIntensity <YOURGAMEHERE> ?outputgame)