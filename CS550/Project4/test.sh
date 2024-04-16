#!/bin/bash

output=$(./play 2)
expected="Written by: Abraham J. Reines
Paper, Scissors, Rock: 2 iterations
Referee started, waiting for players...
Go Players [1]
Player 1: SCISSORS
Player 2: ROCK
Player 2 Wins
Go Players [2]
Player 1: PAPER
Player 2: ROCK
Player 1 Wins
Final Score:
Player 1: 1
Player 2: 1"

if [ "$output" == "$expected" ]; then
  echo "Test Passed"
else
  echo "Test Failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
fi
