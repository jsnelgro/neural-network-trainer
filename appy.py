from gevent import monkey
monkey.patch_all()

import uuid
import base64
import numpy as np
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, disconnect
from PIL import Image
import StringIO
import os


from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
import nntester as nn
# from flask.ext.heroku import Heroku


app = Flask(__name__, static_url_path='')
# heroku = Heroku(app)
app.debug = True
socketio = SocketIO(app)
thread = None

# TODO: these variables can't be global if this is to support multiple users
# Probably have to queue users for training if I want to scale this project
# Or maybe nevermind... I think Flask encapsulates socket connections
training = False
testing = False
labels = []
trainingData = []
net = None
trainer = None
numOfDatapoints = 0

######## ASSOCIATE ###########

@socketio.on('associate', namespace='/test')
def save_association(message):
    global numOfDatapoints
    global trainingData
    global training
    global testing
    global labels
    if not training:
        img, label = process_association(message)
        trainingData.append((img,label))
        numOfDatapoints += 1
        print numOfDatapoints



@socketio.on('set network', namespace='/test')
def init_network(message):
    global trainingData
    global net
    global trainer
    if trainingData:
        trndata = nn.buildDataset(labels, trainingData)
        net, trainer = nn.getNetwork(trndata)
        emit('networkBuilt')


######################### TRAIN ##############################

@socketio.on('start training', namespace='/test')
def train_network():
    global thread
    global training
    if not training:
        thread = Thread(target=training_thread)
        thread.name = 'trainingThread'
        emit('training started', thread.name)
        thread.start()
        training = True


def training_thread():
    """Start a new thread for training the network"""
    global trainer
    global net
    nn.doTraining(net, trainer)
    # if trainingData:
        # trndata = nn.buildDataset(labels, trainingData)
        # print trndata, tstdata    
        # net, trainer = nn.getNetwork(trndata)


@socketio.on('getTrainingStatus', namespace='/test')
def check_status(message):
    global thread
    global training
    if thread:
        training = thread.is_alive()
        if not training and message == thread.name:
            emit('training complete')
    else:
        training = False



########################### TEST ###############################

@socketio.on('run test', namespace='/test')
def test_network(message):
    global training
    global trainer
    global testing
    if not training and not testing and net:
        testing = True
        # do test on message data here and return results
        img = process_association(message)[0]
        res = net.activate(img.ravel())
        print res
        emit('test result', res.tolist())
        testing = False



############ MISC, ROUTING, AND SOCKET FUNCS ###############



############ UTILS ############

def from_b64(b64):
    im = Image.open(StringIO.StringIO(base64.b64decode(b64)))
    return np.array(im)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def process_association(message):
    head, body = message['data'].split(',', 1)
    img = rgb2gray(from_b64(body))
    label = labels.index(str(message['behavior']))
    return (img, label)

###############################





########### ROUTING ##########

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

##############################





########### SOCKET FUNCS ################


@socketio.on('set labels', namespace='/test')
def set_labels(message):
    global labels
    labels = [str(x) for x in message['labels']]

# @socketio.on('disconnect request', namespace='/test')
# def disconnect_request():
#     print 'trying to disconnect...'
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('disconnected',
#          {'data': 'Disconnected!', 'count': session['receive_count']})
#     disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    print 'connected'

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print 'disconnected'


#########################################

if __name__ == '__main__':
    socketio.run(app)
