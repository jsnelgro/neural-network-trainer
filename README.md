README
=====================
*johnny.snelgrove@gmail.com*

Installation
---------------------

1. Make sure you have the python package manager "pip" installed.
2. cd into the project directory
3. `pip install -r requirements.txt`
4. `python appy.py`
5. open a browser and point it to `http://localhost:5000`

note: you may also test the system by going to [http://still-lowlands-4107.herokuapp.com/](http://still-lowlands-4107.herokuapp.com/). However, this is a small free server and is **very** slow. It may also timeout while training. You will also need make sure your browser allows the page to run *unsafe scripts*. Otherwise the websocket will not be able to connect the server and client.

Usage
---------------------

1. Click the *Add Behavior* button.
2. Give your behavior a name.
3. Click inside the box to start editing the code. This code will be run when this behavior is the result of testing. You can write any javascript to modify the output (it's a `<div>` element). Helper methods `output.log()` and `output.clear()` are available to easily print results. In addition, you can access the raw output of the network which is in the form of an object called `data`. The data object has two fields: `data.dominantIndex` and `data.response`. The first field is the index of the highest response, and the second field is the array of output values.
4. When you are finished, click the `Add` button.
5. Tip: You can also click the menu in the top left corner and select *color defaults* if you want to use red, green, and blue outputs to quickly move on to the associating step.
6. After you have written all of your output scripts, press the up and down arrow keys to highlight an output script, then hold the spacebar to associate the current video frames with that output.
7. Once you are finished creating the associations, click the `init` button. The button will change to say `train`. Click it again and the network will start training on the associations.
8. The training step may take awhile depending on the speed of your computer, and the number and complexity of the associations.
9. When training is complete, a notification will pop up and the train button will switch to a `Run` button. Click run to start interacting with the network!