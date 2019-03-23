![TOP WINNER](http://myazo.wailau.net/data/34613eaaa0b3f981bcc2c63e.png)
![game_pic](http://myazo.wailau.net/data/d6fd715bce20027d62317341.png)

# C-O-M-P-4-7-2
ダブルカード C ○ M P 4 7 2 ●

This is written in Python 3. You may need to `sudo pip3 install colorama`. It is recommended to `sudo pip3 install ipdb`.

### Design Idea

For speed, it might be better to avoid some OOP conventions:
Classes should be stateless singletons (when it makes sense), this allows for components to be reused by the AI. 

In other words, the main game loop should keep track of the data, it will pass this data to other classes to be manipulated.

For example, here is how the BoardSynth class can be used:
```py
board = board_synth.new()
board_synth.apply(board, '01E1')
board_synth.render(board)
```
```
12
11
10
9
8
7
6
5
4
3
2
1      ○●
   ABCDEFGH
```
```py
board_synth.apply(board, '01G1','01G2')
board_synth.render(board)
```
```
12
11
10
9
8
7
6
5
4
3
2        ○●
1      ○●○●
   ABCDEFGH
```
The main loop should keep track of the moves that have been played in order to recycle moves during that stage.

To run on the school computer for demo purposes: 
1. Download coloroma and copy paste files into the repository directory
2. cd into the repository directory 
3. Type in: `"C:\Program Files (x86)\Python36-32\python.exe" game.py`

