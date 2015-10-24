# Introduction #

This project implements a basic 2D billiards game in python using pygame. It was originally written by Prashant Agrawal. Later, Pankaj Pandey joined him and now is an active member of this project.


# Salient Features #

Some of the salient features of the game include:
  * Replay function (immensely useful for debugging purposes, plus, looks cool :P)
  * Slow movement (so that you don't miss your critical shots)
  * Play/pause features at any time during the play
  * Balls move randomly with SPACE button if you're too lazy to take the aim with the cue and just want to see balls moving.
  * Fancy sounds on collision of balls, when they go to holes and on finishing the game.
  * A white ball is used to hit all other balls like real billiards game.
  * Command-line scoreboard functionality for multi-player game is implemented.


# Things yet to do #

  * Fix clinging of balls during near-tangential collision
  * Fix replay operation which sometimes doesn't reproduce exact track of balls (probably due to clinging itself)
  * Fix slight non-synchronous nature of sounds
  * Extend the current command line scoreboard to display it on screen.
  * Implement collision of the cue with the edge of the ball (currently, the cue always hits the ball in center)
  * Simulate spinning of balls.
  * Better arena and holes (like a real billiards game)