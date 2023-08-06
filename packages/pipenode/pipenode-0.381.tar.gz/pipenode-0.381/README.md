# pipenode
pipenode supported mode:
* thread
* process
* coroutine

## example
 
```
import pipenode
import time
def work(**kwargs):
    print('my work', kwargs.get('name'))
    time.sleep(1)

server = pipenode.Server(run_type='thread|process|coroutine', max_workers=10)
_ = [server.add_worker(work, name='luo') for _ in range(10)]
server.run_executor()
```

## Extensions

Extensions folder include modulers or other tools someone sharing. You can push your code without bugs.


|logo|

|Build Status|


|Demo|

Documentation
-------------

* `HEAD `

GitHub.

Roadmap
-------

.. 