# QLearning_GridWorld

Implementation of Q-Learning algorithm (reinforcement learning) using grid-world environment.

## Usage
Require arguments:<br>
<b>File with world description </b> (eg. world1.txt)<br>
<br>
Optional arguments: <br>
<b>-q</b> -> Run the q-learning algorithm and print the result as standard output <br>
<b>-qi</b> -> Change the number of iterations (default: 10000) <br>
<b>-sh</b> -> show the results as figures <br>


https://user-images.githubusercontent.com/44849247/143001869-749deca0-72a3-49f9-8f09-6aa5a23c3c3f.mp4




<b>-s</b> -> save the results to tmp.* file <br>
<b>-sfn</b> -> change the filename for saved files <br>

## Example of usage
<b>1) Run q-learning for world1 and 100000 iterations</b><br>
python main.py world1.txt -q -qi 100000

![2020-06-24_19h13_17](https://user-images.githubusercontent.com/44849247/85602576-ce6ad180-b64f-11ea-8a55-6f487a1304f0.png)

<b>2) Show the results graphically</b><br>
python main.py world1.txt -q -qi 100000 -sh

![2020-06-24_19h13_07](https://user-images.githubusercontent.com/44849247/85602585-cf9bfe80-b64f-11ea-92d4-1d534b448ce6.png)
![2020-06-24_19h13_03](https://user-images.githubusercontent.com/44849247/85602590-d0cd2b80-b64f-11ea-9a79-9e7cacced91a.png)

<b>3) Show the results graphically and save them to "figures" file</b><br>
python main.py world0.txt -q -qi 100000 -sh -s -sfn figures

## World file structure
The world must be created using the following symbols in .txt file:
![obraz](https://user-images.githubusercontent.com/44849247/85588710-3830ae80-b643-11ea-9804-a712a75668ef.png)

