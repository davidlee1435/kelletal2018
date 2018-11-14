# kelletal2018
Parameters for the neural network used in Kell, Yamins, Shook, Norman-Haignere, and McDermott. "A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy." Neuron, 2018. You can find the article <a href="https://www.cell.com/neuron/fulltext/S0896-6273(18)30250-2">here</a>.

Demo.ipynb is an iPython/Jupyter notebook that shows how to create a tensorflow graph for the network and gives an example of how to pass a sound into the network.

If you have any questions, please contact Alex Kell at < first_name >< last_name >@mit.edu.

### Setup
**Run these steps sequentially**

Clone the repository
```
$ git clone git@github.com:davidlee1435/kelletal2018.git
```

Run virtualenv and install dependencies. Make sure that your virtualenv uses Python 2.7
```
$ cd kelletal2018
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Install `pycochleagram`
```
$ cd ..
$ git clone https://github.com/mcdermottLab/pycochleagram
$ cd pycochleagram
$ python setup.py install
$ cd ../kelletal2018
$ rm -rf ../pycochleagram
```

Add the virtualenv kernel to iPython
```
$ ipython kernel install --user --name=venv
```

To run the demo, run:
```
$ jupyter notebook
```

You should be able to run all the cells.
