#Pong-v0#
<p>By Kaihang 1400012727</p>
##Files##
<b><li>main.py</li></b>
This is the main code file. It only contains the test. Training is not included.
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

##How to test##
__Make sure you put model.pkl in the same dir with main.py__
<pre><code>$python3 main.py</code></pre>
<p>Then it should go like this:<p>
<pre><code>ubuntu@google:~/Learning/pong$ python3 main.py
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
##Render##
If you'd like to watch how it plays, you can uncomment the 40th line in main.py:
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