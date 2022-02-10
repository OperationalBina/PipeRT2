# PipeRT2

<p align="center">
<a href="https://github.com/OperationalBina/PipeRT2/actions"><img alt="Actions Status" src="https://github.com/OperationalBina/PipeRT2/workflows/Test/badge.svg"></a>
<a href="https://badge.fury.io/py/PipeRT"><img src="https://badge.fury.io/py/PipeRT.svg" alt="PyPI version" height="18"></a>  <a href='https://operationalbina.github.io/PipeRT2/'>
    <img src='https://github.com/OperationalBina/PipeRT2/actions/workflows/docs.yml/badge.svg' alt='Documentation Status' />
  </a>
<a href="https://codecov.io/gh/OperationalBina/PipeRT2">
    <img src="https://codecov.io/gh/OperationalBina/PipeRT2/branch/master/graph/badge.svg?token=ze7192iCby"/>
  </a>

PipeRT2 is an infrastructure for data processing with the ability 
of handling a high flow rate.

Design a complex dataflow dynamically can be done using PipeRT2. 
With a simple implementation of pipe's components a full dataflow can be dispatched. 

**Table of contents**
- [Requirements](#requirements)
- [Components](#components)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Advanced](#advanced)
- [The Events Mechanism](#the-events-mechanism)
- [Custom Events](#custom-events)
- [Using The Cockpit](#using-the-cockpit)
- [Running via RPC CLI](#running-via-rpc-cli)
- [Running via API](#running-via-api)
- [Synchroniser](#synchroniser)
- [Constant FPS](#constant-fps)
- [FAQ](#faq)
- [Contributing](#contributing)


# Requirements

- Python 3.6

# Components

**Routine** - The smallest component in the pipe.

Each routine has to implement a `main_logic` function that contains the business logic of the routine.

There are three types of routines - 

- **SourceRoutine** - The first routine in a pipe. Used for generating new data and streaming it 
through the pipeline. 
- **MiddleRoutine** - Consumes data from other routines in the pipeline. Perform desired operations on any given data and send the results into the next routine. 
- **DestinationRoutine** - The last routine of the pipe. Used for storing the results from all data manipulation. 

**Flow** - Contains multiple routines with the same context.

Each flow within the pipe runs as a seperate process. Utilizing this correctly will improve the pipes performence.

For example, if you have a pipe that includes multiple CPU heavy operations, it is better to seperate them into different routines within different flows.
Doing so will maximize your pipes performence.

**Pipe** - Controls the different elements and aspects of the system. Contains all flows. Distributing events through all components.

# Installation

We publish PipeRT2 as `PipeRT` package in PyPi. 

Run `pip3 install PipeRT` for installing the official PipeRT2 stable version.

# Getting Started 

For example, we're going to create a pipe which contains simple flows with very simple routines.

The First step is to create a 'SourceRoutine', which will be responsible for generating data inside our pipeline. 
    We create the source class that generates data:

```Python
from pipert2 import SourceRoutine

class GenerateData(SourceRoutine):

    def main_logic(self) -> dict:
        return {
            "value": "example"
        }
```

Then we create the destination routine to store (in our case print) the pipeline's result:

```Python
from pipert2 import DestinationRoutine

class PrintResult(DestinationRoutine):

    def main_logic(self, data: dict) -> None:
        print(data["value"])
```

Now we create new pipe that contains a flow made by those two routines:

```Python

from pipert2 import Pipe, QueueNetwork
from pipert2.utils.consts.event_names import START_EVENT_NAME, KILL_EVENT_NAME

# Creating the pipe.
example_pipe = Pipe()

# Create an instance of each routine.
generate_data_routine = GenerateData()
print_result_routine = PrintResult()

# Create a flow with the required routines.
example_pipe.create_flow("example_flow", True, generate_data_routine, print_result_routine)

# Build the pipe.
example_pipe.build()

# Run the pipe.
example_pipe.notify_event(START_EVENT_NAME)

# Force all the pipe's routines stop.
example_pipe.notify_event(KILL_EVENT_NAME)
```

For connecting routines in a different order we use `example_pipe.link` function, for example:

```Python
example_pipe.create_flow("example_flow", False, generate_data_routine, print_result_routine)
example_pipe.link(Wire(source=generate_data_routine, destinations=(print_result_routine,)))
```

For triggering an event for a specific flow or routine we add a dictionary of the required specific flows and routines:
- for example trigger all routines in `example_flow`: 
    ```Python
    example_pipe.notify_event(START_EVENT_NAME, {"example_flow": []})
    ```
- for example trigger specific routines in `example_flow`:
    ```Python
  example_pipe.notify_event(START_EVENT_NAME, {"example_flow": [generate_data_routine.name, print_result_routine.name]})  
  ```
  
### Custom Data Types

Instead of using the `Data` class to pass arguments throughout the pipe's routines, you can create custom class that will inherit from `Data` 
with your own parameters. 

For example: 

```Python
class Example(Data):
    def __init__(self):
        self.custom_param = "custom param"

class SrcRoutine(SourceRoutine):
    def main_logic(self) -> Example:
        return Example()

class MidRoutine(MiddleRoutine):
    def main_logic(self, example: Example) -> Example:
        print(example.custom_param) // output -> "custom param"
        example.custom_param = "change"
        
        return example

class DstRoutine(DestinationRoutine):
    def main_logic(self, example):
        print(example.custom_param) // output -> "change"
```



# Advanced
## The Routine
When inhereting the base routine class, there are 3 main functions to extend upon.

The first:
### main_logic
The `main_logic` function acts as the core of the routine. Each routine *has* to implement this method in order for it to work.  
The `main_logic` function occurs each time new data is being received from another routine. A routine that generates data will have its `main_logic` executed whenever possible.  
The `main_logic` function can serve a few porpouses according to the routines need:
```Python
# The first type of main logic for a generator type routine
def main_logic(self) -> Data:
    # This main logic will return a new `Data` object without any input required.
    # Usually this type of routine will be placed as a starting routine for the pipe/flow.

    # This main logic must return data as its return clause.

# The second type of main logic is for a 'computational' routine.
def main_logic(self, data: Data) -> Data:
    # This main logic will get input from a previous routine within the pipe, and send out new data.
    # This type of routine will most likely be the core of your pipe, doing manipulations on your data or whatever you desire it to do!

    # This main logic must return data as its return clause.

# The third type of main logic is for a final routine.
def main_logic(self, data: Data) -> None:
    # This main logic will get input from a previous routine within the pipe, and do whatever you define it to do.
    # This type of routine will usually be the finalizing process of your pipe, doing things such as: saving to a file, showing a resulting image, and so on.
```

The second:
### setup
The `setup` function of a routine happens right before the routine starts working.  
The `setup` function should be used to set a starting state for your routine.  
For example: opening a file, setting up a socket for a stream, resetting attributes of the routine, etc...  

The third:
### cleanup
The `cleanup` function acts as the counterpart to the `setup`.  
The `cleanup` function should be used to clean any resources left used by the routine.  
For example: releasing a file reader, closing a socket, etc...  

# The Events Mechanism
Events within the pipe can change its behaviour in real time.
Events can be called with the `Pipe` or `Routine` objects using the `notify_event` function in the following syntax:
```Python
# Notifies all of the flows within the pipe with the given event.
example_pipe.notify_event(<Event_name>)

# Notifies a specific flow or flows with the given event.
example_pipe.notify_event(<Event_name>, {<Flow_name1>: [], <Flow_name2>: []...})

# Notifies only specified routines with the given event.
example_pipe.notify_event(<Event_name>, {<Flow_name1>: [<routine_name1>, <routine_name2>...]})
    
# Same applies for routine except 
class SomeRoutine(Routine):
    ...
    def SomeFunc(self):
        # In order to notify event within the routine
        self.notify_event(<Event_name>, {<Flow_name1>: [<routine_name1>, <routine_name2>...]})
        # Same syntax used in notify_event of the pipe

# Or alternatively 
some_routine = SomeRoutine()
some_routine.notify_event(<Event_name>, {<Flow_name1>: [<routine_name1>, <routine_name2>...]})
```

The pipe package has a few builtin events already implemented, those events are:
- STOP_EVENT_NAME: Stops the specified routines.
- KILL_EVENT_NAME: Force stops the specified routines.
- START_EVENT_NAME: Starts the specified routines.

# Custom Events
When writing your routines, you can implement your own events to issue custom behaviour.

Here is an example routine that has two custom events:
```Python
class SomeRoutine(Routine):
    def __init__(self, name):
        super().__init__(name)
        self.cap = None

    # This event causes the routine to set its opencv reader.
    @events("CUSTOM_EVENT_NAME")
    def some_func(self):
        # Some logic
```
To call the new events `notify_event` is used just like any other event:
```Python
from pipert2 import Pipe
from pipert2.utils.consts.event_names import START_EVENT_NAME, KILL_EVENT_NAME

# Creating the pipe.
example_pipe = Pipe()

# Create an instance of each routine.
some_routine = SomeRoutine("some_routine")
print_result_routine = PrintResult()

# Create a flow with the required routines.
example_pipe.create_flow("example_flow", True, some_routine, print_result_routine)

# Notify the custom event
example_pipe.notify_event("CUSTOM_EVENT_NAME", {"example_flow": ["some_routine"]}, example_param1="some_value1", example_param2="some_value2"...)

# Start the pipe
example_pipe.notify_event(START_EVENT_NAME)
```

# Using The Cockpit
(Before you get started, make sure you have an instance of the cockpit up and running. For more information visit the [PipeRT-Cockpit repository](https://github.com/OperationalBina/PipeRT-Cockpit))  
In order for the pipe to be able to communicate with the cockpit a few things must be done.  
First create a `.env` file with the following contents:
```.env
SOCKET_LOGGER_URL="<cockpit url here (usually http://localhost:3000 if on the same system)>/api/socketio"
```  
After that your pipes default logger with the socket logger like so:
```Python
from pipert2 import Pipe
from pipert2.utils.logging_module_modifiers import get_socket_logger

# logger level indicates what logs will be sent, if logging.INFO is provided info logs and above will be sent and so on.
example_pipe = Pipe(logger=get_socket_logger("<desired base name here>", <logger level>))
```
And that's it!  
After that your pipe will send its logs to the cockpit!

# Running via RPC CLI

Firstly, in order to use this capability, you need to install the optional package via `pip install PipeRT[rpc]`  

The next step is running the RPC Server:
```Python
rpc_pipe = Pipe()
rpc_server = RPCPipeWrapper(pipe)
rpc_server.run_rpc_server(endpoint="<end_point>")
``` 
   
You can easily connect to the RPC server via Python and CLI following the example in the [ZeroRPC's page](https://pypi.org/project/zerorpc/)

In order to execute pipe events you need to run the `execute` function of the server.
Arguments to pipe events are passed in a JSON format:
- for example via python: 
    ```Python
    client.execute('start') # no arguments example
    client.execute('join', '{"to_kill":true}') # including arguments example
    ```
- for example via CLI:\
    `zerorpc tcp://0.0.0.0:1234 execute start`\
    `zerorpc tcp://0.0.0.0:1234 execute join '{"to_kill":true}'`
 

# Running via API
Firstly, in order to use this capability, you need to install the optional package via `pip install PipeRT[api]`  

After creating a pipeline, you need to call run_api_wrapper with your host and port:
```Python
pipe = Pipe()
...

api_wrapper = APIWrapper(host="<host>", port=<port>, pipe=pipe)
api_wrapper.run()
```

In order to execute pipe events you need to execute `GET` http calls for `your_host:your_port` address.

- To start the pipe, use route: `your_host:your_port/start`

- To pause the pipe, use route: `your_host:your_port/pause`

- To kill the pipe and kill the API server, use route: `your_host:your_port/kill`

- To start or stop a specific routine, use route: 
   - Start: `<your_host>:<your_port>/routines/<routine_name>/events/<start>/execute` 
   - Stop: `<your_host>:<your_port>/routines/<routine_name>/events/<stop>/execute` 


- To trigger a custom event for all of the routines, use route:`<your_host>:<your_port>/routines/events/<event_name>/execute` 

- To trigger a custom event on a specific routine, use route:`<your_host>:<your_port>/routines/<routine_name>/events/<custom_event>/execute` 

- For add additional arguments, add it to the body of the request as json as:
```JSON
{
  "extra_args": {
    "param1": value, "param2": value
  } 
}
```

# Synchroniser

In the pipe there is a synchronising mechanism which is used to synchronise the routine's FPS.
This mechanism forces routines to rest, if their FPS is significantly higher than that of the bottlenecks routines.
It saves resources, and should not affect the number of the processed routines. 

The best example of a case where the synchronising mechanism would be useful, is when there are fast routines
followed by routines with lower FPS.

To activate this mechanism, create the pipe should with `auto_pacing_mechanism` parameter as true, for example: 
```Python
pipe = Pipe(auto_pacing_mechanism=True)
```

# Constant FPS

How to set it? 
When initializing a routine, call the `set_const_fps` function with the required FPS.

```Python
class Example(DestinationRoutine):
    def __init__(self, required_fps):
        self.set_const_fps(required_fps)
```

# FAQ 
    
    Q: What will happen when nothing is returned from the main logic?
    A: Not returning anything from a function will return None.
       We detect when None is returned and just ignore it.
       So in short, you will not send anything to the next routine in line.
.
    
    Q: What happens if an exception is raised within the Pipe (main_logic, setup, cleanup)?
    A: setup and cleanup methods - The routine Thread will crash.
                                   It will cause the routine to stop working untill you 
                                   stop and start again.

       main_logic method - The crash will notify the user with the routine’s logger.
                           The crash won’t effect the routine’s execution because it will just 
                           take the next data inline from the message handler and will 
                           execute the main logic on it.
.
    
    Q: Why and how to use data transmitters?
    A: The user can decide to not transport the data of a message through the message broker 
       and choose different approach, for example via Shared memory or local file system.


# Contributing

For contributing please contact with [San-Moshe](https://github.com/San-Moshe) for accessing our Jira. 

Please follow the conventions using in the project and make sure all checks pass.

The PR name needs to be in the format of [jira_ticket_id] - [Task description] 

</p>
