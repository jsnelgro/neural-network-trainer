from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure import RecurrentNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer


def buildDataset(labels, data):
	'''
	builds and returns training and test datasets from user image mappings 
	'''
	DS = ClassificationDataSet(len(data[0][0].ravel()), 1, nb_classes=len(labels), class_labels=labels)
	
	for img, label in data:
		DS.addSample(img.ravel(), [label])
	DS._convertToOneOfMany()
	return DS

def getNetwork(trndata):
	n = RecurrentNetwork()
	n.addInputModule(LinearLayer(trndata.indim, name='in'))
	n.addModule(SigmoidLayer(100, name='hidden'))
	n.addOutputModule(LinearLayer(trndata.outdim, name='out'))
	n.addConnection(FullConnection(n['in'], n['hidden'], name='c1'))
	n.addConnection(FullConnection(n['hidden'], n['out'], name='c2'))
	n.addRecurrentConnection(FullConnection(n['hidden'], n['hidden'], name='c3'))
	n.sortModules()


	# fnn = buildNetwork( trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer )
	trainer = BackpropTrainer( n, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)
	
	# TODO: return network and trainer here. Make another function for training
	# for i in range(20):
		# trainer.trainEpochs(1)
	# trainer.trainUntilConvergence(maxEpochs=100)

	# trnresult = percentError( trainer.testOnClassData(),trndata['class'] )
	# tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )

	# print "epoch: %4d" % trainer.totalepochs, \
	# 	"  train error: %5.2f%%" % trnresult

	# out = fnn.activateOnDataset(tstdata)
	# out = out.argmax(axis=1)  # the highest output activation gives the class
	return (n, trainer)


def doTraining(network, trainer):
	trainer.trainUntilConvergence(maxEpochs=100)
	# trnresult = percentError( trainer.testOnClassData(),trainer.dataset['class'] )
	# print "epoch: %4d" % trainer.totalepochs, \
		# "  train error: %5.2f%%" % trnresult
