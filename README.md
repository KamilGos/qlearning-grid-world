<!-- image -->
<div align="center" id="top"> 
  <img src=images/idea.png width="400" />
  &#xa0;
</div>

<h1 align="center"> qlearning-grid-world </h1>
<h2 align="center"> Implementation of Q-Learning algorithm (reinforcement learning) using grid-world environment </h2>

<!-- https://shields.io/ -->
<p align="center">
  <img alt="Top language" src="https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python">
  <img alt="Status" src="https://img.shields.io/badge/Status-done-green?style=for-the-badge">
  <img alt="Code size" src="https://img.shields.io/github/languages/code-size/KamilGos/qlearning-grid-world?style=for-the-badge">
</p>

<!-- table of contents -->
<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#package-content">Content</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#eyes-implementation">Implementation</a> &#xa0; | &#xa0;
  <a href="#microscope-tests">Tests</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#technologist-author">Author</a> &#xa0; | &#xa0;
</p>

<br>

---

<center>

You can find the implementation of Markov Decision Process using grid-world environment here: [github.com/KamilGos/markov-decision-process-grid-world](https://github.com/KamilGos/markov-decision-process-grid-world)

</center>

---


## :dart: About ##
Project is an implementation of reinforcement learning algorithm, named Q-Learning using "Grid World". 


## :package: Content
 * [data](data) - three example worlds
 * [sources](sources) - source files
 * [main.py](main.py) - main executable file

## :checkered_flag: Starting ##
```bash
# Clone this project
$ git clone https://github.com/KamilGos/qlearning-grid-world

# Access
$ cd qlearning-grid-world

# Run the project
usage: main.py [-h] [-q] [-qi QITER] [-sh] [-s] [-sfn SAVE_FILENAME] world_filename

positional arguments:
  world_filename        Chosen world filename. Eg. "world1.txt"

optional arguments:
  -h, --help            show this help message and exit
  -q, --qrun            Run Q-learning algorithm for 10000 iteration.To change number of iteration use: -qi [num]
  -qi QITER, --qiter QITER
                        Change number of iteration for Q-learning algorithm. Use: -qi [num]
  -sh, --show           Show figures
  -s, --save            Save figures and data to tmp.* To change filename use: -sfn [filename]
  -sfn SAVE_FILENAME, --save_filename SAVE_FILENAME
                        Change saved figures file names. Use -sfn [filename] (DO NOT USE FILE EXTENSION!)

# Example of usage:

# Run q-learning for world1 and 100000 iterations
$ python main.py data/world1.txt -q -qi 100000  

# Run q-learning for world1 and 100000 iterations and show the results graphically
$ python main.py data/world1.txt -q -qi 100000 -sh

# Show the results graphically and save them to "figures" file
$ python main.py data/world0.txt -q -qi 100000 -sh -s -sfn figures
```

https://user-images.githubusercontent.com/44849247/143001869-749deca0-72a3-49f9-8f09-6aa5a23c3c3f.mp4

## :eyes: Implementation ##
<h2>Grid World</h2>
Inside 'data' folder you can find three prepared, ready world. Hovever you can create your own world using the following file structure:

<div align="center">

| Structure   | Exampple    |
|--------------- | --------------- |
|   <img src=images/world_structure.png width="600" />  |   <img src=images/world1_structure.png width="100" /> |

</div>

The graphical representation of these worlds is shown in picture below. White colour means that the considered state is **normal**. Colour black was used **forbidden** states, the colour green was used for **terminal** states, yellow for **special** states and blue for start state. The figures also indicate the numbering of coordinates that is used in the program output. The 0.0 utility in green state means that this is terminal state. 

<div align="center" id="put_id"> 
  <img src=images/world1_graph.png width="250" />
  &#xa0;
</div>

<h2>Variables</h2>

 * **Epsilon** - exploration ratio
 * **NOI** - Number of iterations

## :microscope: Tests ##
The Q-learning with exploration algorithm was implemented and tested using World1 for different exploration ratio {0.05, 0.2} and for a different number of iterations (NOI). Utility and policy are presented for each considered case. In addition, for every case, information about the time of algorithm execution has been attached (called Exe.time). All calculations were carried out onthe same computer.

<h2>Epsilon: 0.05, NOI: 10000, Exe.time: 1.94s</h2>

<div align="center" id="put_id"> 
  <img src=images/test1.png width="500" />
  &#xa0;
</div>

<h2>Epsilon: 0.05, NOI: 100000, Exe.time: 18.45s</h2>

<div align="center" id="put_id"> 
  <img src=images/test2.png width="500" />
  &#xa0;
</div>

<h2>Epsilon: 0.05, NOI: 1000000, Exe.time: 179.4s</h2>

<div align="center" id="put_id"> 
  <img src=images/test3.png width="500" />
  &#xa0;
</div>

<h2>Epsilon: 0.2, NOI: 10000, Exe.time: 2.15s</h2>

<div align="center" id="put_id"> 
  <img src=images/test4.png width="500" />
  &#xa0;
</div>

<h2>Epsilon: 0.2, NOI: 100000, Exe.time: 22.23s</h2>

<div align="center" id="put_id"> 
  <img src=images/test5.png width="500" />
  &#xa0;
</div>

<h2>Epsilon: 0.2, NOI: 1000000, Exe.time: 234.5s</h2>

<div align="center" id="put_id"> 
  <img src=images/test6.png width="500" />
  &#xa0;
</div>
<h2>Conclustions</h2>
For all cases, the agent found the optimal policy (best path). We can see that for almost all states the more iterations cause the higher utility values (as expected). For examples with exploration parameter set to 0.2, we can see that the execution time of a q-learning algorithm is higher than for cases with Epsilon=0.05. This is because the agent more often enters the procedure of generating a new state, which lasts longer than the exploitation, which is just taking the value from the array. Using a fixed epsilon value is not a perfect idea. A better idea seems to be using exploration parameter that changes during algorithm work. At the begging of learning about the environment, the probability of selecting a random state should be higher to visit all possible states earlier, then the parameter should be lower to optimise the path. For example, exponential decay can be used. 

## :memo: License ##

This project is under license from MIT.

## :technologist: Author ##

Made with :heart: by <a href="https://github.com/KamilGos" target="_blank">Kamil Goś</a>

&#xa0;

<a href="#top">Back to top</a>



<!-- ADDONS -->
<!-- images -->
<!-- <h2 align="left">1. Mechanics </h2>
<div align="center" id="inventor"> 
  <img src=images/model_1.png width="230" />
  <img src=images/model_2.png width="236" />
  <img src=images/model_3.png width="228" />
  &#xa0;
</div> -->

<!-- one image -->
<!-- <h2 align="left">2. Electronics </h1>
<div align="center" id="electronics"> 
  <img src=images/electronics.png width="500" />
  &#xa0;
</div> -->


<!-- project dockerized -->
<!-- <div align="center" id="status"> 
  <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png" alt="simulator" width="75" style="transform: scaleX(-1);"/>
   <font size="6"> Project dockerized</font> 
  <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png" alt="simulator" width="75"/>
  &#xa0;
</div>
<h1 align="center"> </h1> -->
