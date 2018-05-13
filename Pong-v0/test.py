import numpy as np
import gym
import pickle

def sigmoid(x): 
	return 1.0 / (1.0 + np.exp(-x))

def action(p):
	return 2 if np.random.uniform()<p else 3
	
def imageInit(image):
	image=image[35:195]
	image=image[::2,::2,0]
	image[image == 109] = 0
	image[image == 144] = 0
	image[image != 0] = 1
	return image.astype(np.float).ravel()	
	
def policyForward(img,model):
	h=np.dot(model['W1'],img)
	h[h < 0] = 0
	p = sigmoid(np.dot(model['W2'],h))				
	return p
	
def play():
	game = "Pong-v0"
	dimension = 80*80  
	rewardSum = 0	
	episode = 0
	movingMean = None
	model, movingMean, episode = pickle.load(open('model.pkl','rb'))
	print("[INIT]Resume at Episode {} MovingMean={}".format(episode, movingMean))
	env = gym.make(game)
	image = env.reset()
	prevImage = None
	stepSum = 0
	gameId = 0
	print("[PLAY]Begin playing {}".format(game))
	while True:
		#env.render()
		curImage = imageInit(image)				
		image = curImage - prevImage if prevImage is not None else np.zeros(dimension)				
		prevImage = curImage  						
		prob = policyForward(image, model)
		actionResult = action(prob)
		image, reward, done, info = env.step(actionResult)
		rewardSum += reward
		stepSum += 1
		if done:
			gameId += 1
			episode += 1
			averageStep = stepSum/(42 - abs(rewardSum))
			print("[GAME {}]Episode:{} Reward: {} StepPerMatch: {}".format(gameId, episode, rewardSum, averageStep))
			stepSum = 0
			rewardSum = 0
			image = env.reset()
			prevImage = None
		
play()