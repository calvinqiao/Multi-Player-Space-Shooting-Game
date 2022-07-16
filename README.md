# Multi-Player-Space-Shooting-Game

## What is this project? 
Hi, dear user. This is a spaceship shooting game. It has one player mode and two player mode. The goal of the game is to enter 112 planet. To achieve this, user needs to pass 3 rounds in one player mode or one round in two player mode. To pass each round, user needs to survive the attack from the enemies and destroy the boss. In the game, there are three different types of suppy stations. User can add HP, add bomb and enable advanced shooting mode by arriving at the abovementioned stations. In addition, type 3 enemy (in one player mode) and boss (in both modes) have some AI feature. Type 3 enemy can move towardsuser's spaceship autonomously while running across the screen. Boss can shoot missles that track the position of the user's spaceship and dodge user's bullets autonmously. It's better for user to be aware of the above features before starting the game.

##. How to run the project?
### For one player mode,
(1) Run Game Server.py
(2) Run Game Client-Broadcaster.py
(3) Press '1' to start the game

### For two player mode,
(1) Run Game Server.py
(2) Run Game Client-Broadcaster.py
This client is responsible for generating all random game objects in the game including
all types of enemies, supply stations, boss, etc.
(3) Run Game Client-Receiver.py
This client receives the information of the broadcast messages sent by the other user and 
generate game objects accordingly in order to sycronize the two games.
(4) Press '2' in both clients to start two player game
