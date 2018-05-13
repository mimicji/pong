#Pong-v0#
<p>By Kaihang 1400012727</p>
##Files##
<b><li>test.py</li></b>
This is the file for training.
<b><li>test.py</li></b>
This is the main code file for test. It only contains the test. Training is not included.
<b><li>model.pkl</li></b>
This the model dmp by pickle.
<b><li>README.md</li></b>
This file.
##Environment##
<li>Ubuntu 16.04</li>
<li>Python 3.5.2</li>
<li>numpy</li>
<li>gym</li>
<li>pickle</li>

##How to use test.py##
__Make sure you put model.pkl in the same dir with test.py__
<pre><code>$python3 test.py</code></pre>
<p>Then it should go like this:<p>
<pre><code>ubuntu@google:~/Learning/pong$ python3 test.py
[INIT]Resume at Episode 32500 MovingMean=-0.9483063444039457
[PLAY]Begin playing Pong-v0
[GAME 1]Episode:32501 Reward: -3.0. StepPerMatch: 208.0.
[GAME 2]Episode:32502 Reward: -1.0. StepPerMatch: 196.34146341463415.
[GAME 3]Episode:32503 Reward: 11.0. StepPerMatch: 168.2258064516129.
...
</code></pre>
<li>'Episode' is the episode number.</li> 
<li>'Reward' is the goal differece: the goal this program gets to the goal its opponent gets in one game. </li>
<li>'StepPerMatch' is the average step per match in this game.</li>
###Render###
If you'd like to watch how it plays, you can uncomment the 40th line in test.py:
<pre><code>...
[39]	while True:
[40]		#env.render()
[41]		curImage = imageInit(image)		
...
</code></pre>
After:
<pre><code>...
[39]	while True:
[40]		env.render()
[41]		curImage = imageInit(image)		
...
</code></pre>
Save and run.

##How to use train.py##
###Resume training###
Resume training from *model.pkl* in the same dir.
<pre><code>$python3 train.py</code></pre>	
<p>Then it should go like this:<p>
<pre><code>ubuntu@google:~/Learning/pong$ python3 train.py
[INIT]Resume at Episode 32500 moving mean -0.9483063444039457
[TRAIN]Begin training Pong-v0
[TRAIN][32501]Reward: 5.0. Moving mean: -0.8888232809599061. TotalSteps: 6405. StepPerMatch 173.1081081081081
[TRAIN][32502]Reward: -10.0. Moving mean: -0.9799350481503071. TotalSteps: 6434. StepPerMatch 201.0625
[TRAIN][32503]Reward: 5.0. Moving mean: -0.920135697668804. TotalSteps: 7142. StepPerMatch 193.02702702702703
...
</code></pre>
It will save for every 250 episodes. Names of autosave files are "backup\_($episode\_num)\_($running\_mean).pkl".
###Start a new train###
In Line 54,
<pre><code>...
[53]	game="Pong-v0"
[54]	resume=True
[55]	render=False
...
</pre></code>
Set *resume* as *False*
<pre><code>...
[53]	game="Pong-v0"
[54]	resume=False
[55]	render=False
...
</pre></code>
Then run *train.py*.