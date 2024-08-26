# Puzzle Champ - A Square Jigsaw Puzzle

This project contains two different puzzle games built using Pygame: a 2x2 puzzle and a 3x3 puzzle. The goal of the game is to drag and drop the puzzle pieces into the correct position to complete the final image.
Requirements

To run these puzzle games, you'll need the following
- Python 3.x
- Pygame library


You can install Pygame by running the following command:
 ```bash
pip install pygame
```

## Files
### puzzle2x2.py

This script implements a 2x2 puzzle game. The puzzle pieces are scrambled and the player needs to drag and drop them into the correct positions to complete the puzzle.

### puzzle3x3.py

This script implements a 3x3 puzzle game. Similar to the 2x2 game, the pieces are scrambled, and the player needs to assemble them correctly to win.


## How to Run

1. Ensure that you have the required resources folder in the same directory as the scripts. The resources folder should contain:
        background.png: Background image for the game.
        icon.png: Icon for the game window.
        static_logo.png: The logo displayed in the game.
        image1.jpg: The final image the player has to recreate by arranging the pieces.
        puzzles/2/: Directory containing 2x2 puzzle pieces in .jpg format.
        puzzles/3/: Directory containing 3x3 puzzle pieces in .jpg format.
        fonts/: Folder containing custom font files.

2. Run the Python script:

```bash

python puzzle2x2.py
```
or

```bash

python puzzle3x3.py
```
## Controls

- Drag and Drop: Click and hold a puzzle piece to drag it and release it in the desired grid position.
- Play Again: After completing the puzzle, press the "Play Again" button to reset the game.

The game will detect when all puzzle pieces are correctly placed and will display a win message. If the pieces are placed incorrectly, a retry option is provided. You can add or modify the images in the resources/puzzles/2/ or resources/puzzles/3/ directories to change the puzzle content.
