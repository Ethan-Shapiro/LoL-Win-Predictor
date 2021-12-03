# Time to Forfeit? (League of Legends Analysis) "V1"
### Introduction
Hello viewer!  
Firstly, thank you for viewing my project, which is live on my Heroku app hosted [here](https://time-to-forfeit-lol.herokuapp.com/)  
  
At its essence, Time to Forfeit? aims to predict who will win a **RANKED** League of Legends game based on the first fifteen minutes of various game data. Through my website, I've created an interface that takes a player's in-game name and region; then it runs the model and returns metrics on the three most recent ranked games they've played. An example can be seen below.
![Example Prediction](https://i.imgur.com/FWf9YnW.png)

### Metrics Used
Below is a list of the metrics collected for each game.
- Gold: Total gold accumulated. (Gold can be used to purchase items which can increase a player's strength.)  
- CS: Number creeps killed. (Killing a creep gives different amounts of gold.)  
- JG: Number of jungle creeps killed. (Same as above.)  
- XP: Total experience accumulated. (This is gained from killing enemies, being in the vicinity of a creep kill, or killing an object.  
- Wards Placed: Number of wards placed. (Wards reveal areas of the map to spot enemies.)  
- Wards Destroyed: Number of enemy wards destroyed.  
- Dragons: Number of that type of dragon killed. (Different dragon types give different advantages to the team that kills them.)  
- Heralds: Number of heralds killed. (These give gold, xp, and when used can do significant damage to towers.)  
- Turrets Destroyed: Number of enemy turrets destroyed. (Killing a turret opens up parts of the map.)  
- Inhibs Destroyed: Number of enemy inhibitors destroyed. (Killing an inhib allows your team to have stronger creeps in that lane.)  
- Kills: Number of enemies killed.  
- Assists: Number of assists on an enemy killed.  
- Deaths: Number of deaths of the team.
- Match ID: Unique ID for each match
- Date: Unix date for the match
- Winner: The winner of the game

### Application Structure
