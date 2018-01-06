# luigi playground

Anything you need to play with to understand Luigi's dark magic.

Luigi is an open sourced python package developed by Spotify, that helps 
 you build complex pipelines of batch jobs. See the the doc page here,
 http://luigi.readthedocs.io/en/stable/index.html
 
The motivation behind this luigi-playground project is to help you try out some simple task workflow and see how it actually works on Luigi's central scheduler server, through their Visualizer UI. 

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

**`cd` to project directory luigi-playground first, then,**

**- basic task example** 
```
python src/examples/example_simple_task.py --task-id 1
```

**- wrapper task with multiple workers** 
```
python src/examples/example_wrapper_task.py --workers 4
```

**- successful event handler task** 
```
python src/examples/example_event_handler_task.py EventHandlerTask --task-id 3
```

**- failed event handler task** 
```
python src/examples/example_event_handler_task.py FailedEventHandlerTask --task-id 0
```


*After hitting any command above, it will direct you to <a>http://localhost:8082</a> to see the visualization*

*Task output will be stored in ./output/directory, and it will be overrode on every task run*
