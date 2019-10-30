# PONGer

Hackathon project from 2017 that uses openCV to track two objects in specified color spaces. The objects are used to control the paddles in a Pong game (open sourced project modified to read output from a file as control).

When the program first starts, the first few seconds tracks the max Y coordinates (as percentages of the total camera view) to calibrate for how far the users are. Then as the colored objects are moved up and down, the paddle moves the same percentage up and down relative to the max and min Y coordinates.


We discovered openCV used BGR rather than RGB color values, over the course of many hours. Rushing to "connect" parts of the project, the coordinate values of the control objects are written to a file, that is read by the Pong game 😆, which may account for why the input values are occassionally sporatic.
