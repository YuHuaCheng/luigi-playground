# LuigiPlayground
Anything you need to play with to understand Luigi's dark magic

## project prerequisites

* python2.7
* docker

## project setup

**1. Launch the local luigi central scheduler by running**

*For more info, https://github.com/sspinc/docker-luigid*
```
docker run -p 8082:8082 -d sspinc/luigid:2.3.0
```
*Then you could go to http://localhost:8082/ to see Luigi UI*


**2. Install python dependencies**
```
python setup.py install
```

## Usage

**`cd` to project directory LuigiPlayground first, then,**

**- basic example** 
```
python src/examples/example_task_wrapper.py
```

**- with multiple workers** 
```
python src/examples/example_task_wrapper.py --workers 4
```

*After hitting any command above, go to <a>http://localhost:8082</a> to see the visualization*