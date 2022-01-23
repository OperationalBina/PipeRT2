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
- [Running via RPC CLI](#running-via-rpc-cli)
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

# Running via RPC CLI

Firstly, you need to install the zerorpc python package via `pip3 install zerorpc`
    
Then, you need to add a flag in the Pipe object creation:
```Python
rpc_pipe = Pipe(run_rpc_cli=True)
```
   
The next step is running the RPC Server:
```Python
endpoint = 'tcp://0.0.0.0:1234'
rpc_pipe.run_rpc_server(endpoint=endpoint)
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
