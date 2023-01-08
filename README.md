# Project - Kabet mängiv robot Kalev (Checkers Robot Kalev)

## Team members

* Albert Unn
* Karl Väärtnõu
* Karl-Mattias Moor
* Epp Haavasalu

## Overwiew

Our project goal is to create a robotic checkers board, that a human player can play checkers against.
Since building a custom robot arm is really difficult, decided we to build a different kind of solution.
We will try to build a special checkers board that has a moving electromagnet under the board itself, that can move the checkers pieces by activating the electromagnet under them and dragging the pieces around the table. The pieces themselves will have small amount of metal in them. The movement of the electromagnet is a little bit more complicated.
We would like to build a 2 axis linear actuation system under the board, using two stepper motors. The system will be something akin to to 3d printers or cnc machines.
The movement logic will be controlled by a computer that will read the board and position of the pieces from an overhead webcam. It is going to be able to recognise opponent movement and using that information calculate and execute its next move.

## List of Necessary Components

| Item | Link to the item | We will provide | Need from instructors | 3D print | Total |
| ---- | ---------------- | --------------: | --------------------: | -------: | :---: |
| Stepper motor | | 0 | 2 | 0  | 2 |
| Stepper motor controller| L298N | 0 | 2 | 0 | 2 |
| Keermelatt 30cm | | 0 | 2 | 0  | 2 |
| Arduino Nano | | 0 | 1 | 0 | 1 |
| Mini USB kaabel | | 0| 1 | 0 | 1 |
| Jumper juhtmed| | 0  | 30 | 0 | 30 |
| Logitech C170 webcam | | 0 | 1 | 0 | 1 |
| Elektromagnet | | 0 | 1 | 0 | 1 |

## Link to Trello

<https://trello.com/invite/b/72wEh3fa/ATTI96578b2b7e0681afb163ae4c90d2dfa2F54F2999/project-board>

## Project instructor - Eva Mõtshärg

## KabeRobotKalev documentation

### Required python packages

    1. opencv-python
    2. numpy
    3. pyserial

### Setup

    1. Run setup.py.
    2. Align Checkersboard centre with the camera crosshair and press 'q'.
    3. The software displays the transformed picture, confirm that it is correct, press 'y'.
    4. Threshold the pieces in order:
    After each threshold press 'y' to confirm the threshold.
        1.The robots pieces
        2.The players pieces
        3.The robots crown pieces
        4.The players crown pieces
    5. The game is set up.

### Running the robot

    Before running the robot, change the COM port on line 23, to the COM port you have the arduino connected to.

    1. Make sure the camera is positioned correctly, and the setup procedure is done.
    2. Run main.py.
    3. Press 'space' for the robot's turn.
    3. To quit the game press 'Esc' key.