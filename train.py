import numpy as np
import gym
import pickle

def sigmoid(x): 
	return 1.0 / (1.0 + np.exp(-x))

def action(p):
	return 2 if np.random.uniform()<p else 3	
	
def rewardNormalization(rewards):
	return (rewards-np.mean(rewards))/np.std(rewards)

def imageInit(observation):
	observation=observation[35:195]
	observation=observation[::2,::2,0]
	observation[observation==109]=0
	observation[observation==144]=0
	observation[observation!=0]=1
	return observation.astype(np.float).ravel()	
	
def forwardPass(x,model):
	h=np.dot(model['W1'],x)
	h[h<0]=0
	p=sigmoid(np.dot(model['W2'],h))				
	return p,h 	

def discountRewards(rewards,gamma):
	discountedRewards=np.zeros_like(rewards)
	runningAdd=0
	for t in reversed(range(0,rewards.size)):
		if rewards[t]!=0:
			runningAdd=0
		runningAdd=runningAdd*gamma+rewards[t]
		discountedRewards[t]=runningAdd
	return discountedRewards

def backProp(hiddenLayers,gradients,images,model):
	dCdW2=np.dot(hiddenLayers.T,gradients).ravel()
	deltal2=np.outer(gradients,model['W2'])
	deltal2[hiddenLayers<=0]=0
	dCdW1=np.dot(deltal2.T,images)
	return {'W1':dCdW1,'W2':dCdW2}

def updateWeights(model,gradientBuffer,rms,decayRate,learningRate):
	for key,value in model.items():
		g=gradientBuffer[key]
		rms[key]=decayRate*rms[key]+(1-decayRate)*g**2
		model[key]+=learningRate*g/(np.sqrt(rms[key])+1e-5)
		gradientBuffer[key]=np.zeros_like(value)
		
def train():
	game="Pong-v0"
	resume=True 
	render=False
	isDebug=False
	batchSize=10
	gamma=0.99
	decayRate=0.99
	learningRate=1e-5
	
	inputDimensions=80*80  
	hiddenNeurons=200
	rewardSum=0	
	episode=0
	movingMean=None
	images,hiddenLayers,rewards,gradients=[],[],[],[]
	if resume:
		model,movingMean,episode=pickle.load(open('model.pkl','rb'))
		print("[INIT]Resume at Episode {} moving mean {}".format(episode,movingMean))
	else:
		model={}
		model['W1']=np.random.randn(hiddenNeurons,inputDimensions)/np.sqrt(inputDimensions)    
		model['W2']=np.random.randn(hiddenNeurons)/np.sqrt(hiddenNeurons)					   
		print("[INIT]New model is created.")

	backGradBuf = { k : np.zeros_like(v) for k,v in model.items() }
	rms = { k : np.zeros_like(v) for k,v in model.items() }
	env=gym.make(game)
	observation=env.reset()
	previousImage=None
	stepSum=0

	print("[TRAIN]Begin training {}".format(game))
	while True:
		if render:
			env.render()
		currentImage=imageInit(observation)				
		if previousImage is not None:
			image=currentImage-previousImage				
		else:
			image=np.zeros(inputDimensions)
		previousImage=currentImage  						
		stepSum=stepSum+1
		prob,h=forwardPass(image,model)
		actionResult=action(prob)
		images.append(image)
		hiddenLayers.append(h)
		if actionResult==2:
			gradients.append(1-prob)
		else:
			gradients.append(-prob)
		observation, reward, done, info = env.step(actionResult)
		rewardSum += reward
		rewards.append(reward)
		if (isDebug)and(reward!=0):
			print('[DEBUG]Reward {} in Step{}'.format(reward,stepSum))
		if done:
			episode+=1
			episodeImage=np.vstack(images)
			episodeHiddenLayer=np.vstack(hiddenLayers)
			episodeGradient=np.vstack(gradients)
			episodeRewards=np.vstack(rewards)
			images,hiddenLayers,rewards,gradients=[],[],[],[]
			episodeGradient*=rewardNormalization(discountRewards(episodeRewards,gamma))
			backProgGradient=backProp(episodeHiddenLayer,episodeGradient,episodeImage,model)
			for k in model:
				backGradBuf[k]+=backProgGradient[k] 
			if episode%batchSize==0: 
				for key,value in model.items():
					g=backGradBuf[key]
					rms[key]=decayRate*rms[key]+(1-decayRate)*g**2
					model[key]+=learningRate*g/(np.sqrt(rms[key])+1e-5)
					backGradBuf[key]=np.zeros_like(value)
			if movingMean is not None:
				movingMean=movingMean*0.99+rewardSum*0.01
				if rewardSum>0:
					averageStep=stepSum/(42-rewardSum)
				else:
					averageStep=stepSum/(42+rewardSum)
				print("[TRAIN][{}]Reward: {}. Moving mean: {}. TotalSteps: {}. StepPerMatch {}".format(episode,rewardSum,movingMean,stepSum,averageStep))
			else:
				movingMean=rewardSum
				
			if episode%1000==0:
				print("[BACKUP]Backup at {}".format(episode))
				backupName='backup_' + str(episode) + '_' + str(movingMean) + '.pkl'
				pickle.dump([model,movingMean,episode],open(backupName,'wb'))
			#elif (movingMean>0)and(episode%30==0):
				#print("[BACKUP]Special backup at {}".format(episode))
				#backupName='special_' + str(episode) + '_' + str(movingMean) + '.pkl'
				#pickle.dump([model,movingMean,episode],open(backupName,'wb'))
			stepSum=0
			rewardSum=0
			observation=env.reset()
			previousImage=None
		
train()