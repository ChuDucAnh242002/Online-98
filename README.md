# Online-98

# Description
The game name is 98 and it is designed by students of Le Hong Phong High School
The game is build using pygame frame work 
The server is build using socket frame work

# Basics
Player: 2+
Play Time: 10 ~ 15 minutes
Win: Last one standing
Lose: Don't have any card to play

# Rule
This game is about calculating the sum:
At first, the sum is 0, after each time a player plays a number cards (1,2,3,...), add to that sum
If the player plays a card which adds to the sum larger than 98, the player lose
For example: sum is 96, player plays 3 of space. The total is 99 which make player loses, the sum reset to 96 since the card is invalid

# Special Card
A of space: reset the sum value to 0
A of heath: put the sum value to 98
Jack: the value of the card is 0
Queen: add the value to sum +30/-30
King: Kill a player and eliminate player from the game, or counter the kill of other player King and kill them back.
4: Block the kill from the king

# Credits
Game Design: students of Le Hong Phong High School

