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
    client.routine_execute('start') # no arguments example
    client.routine_execute('join', '{"to_kill":true}') # including arguments example
    ```
- for example via CLI:\
    `zerorpc tcp://0.0.0.0:1234 execute start`\
    `zerorpc tcp://0.0.0.0:1234 execute join '{"to_kill":true}'`
 

# Running via API

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

- For start/stop specific flows, add it as dictionary to `specific_flows_routine` parameter in the url. 
For example, use route: `your_host:your_port/execute?event_name=start/stop&specific_flows_routine={"flow_name": []}` 

For custom requests:

- To call custom event use execute route and add `event_name` parameter in the url: `url/execute?event_name=custom_event_name`

- To call a specific flows use execute route and add `specific_flows_routine` parameters in the url: `url/execute?event_name=custom_event_name&specific_flow_routines={"flow_name": [], ...}`

- To call specific routines in flows use execute route and add `specific_flows_routine` parameters in the url: `url/execute?event_name=custom_event_name&specific_flow_routines={"flow_name": ["r1", "r2", ...], ...}`

- To add external parameters use execute route and add them to the url: `url/execute?event_name=custom_event_name&param1=0&param2=0&...`

# Contributing

For contributing please contact with [San-Moshe](https://github.com/San-Moshe) for accessing our Jira. 

Please follow the conventions using in the project and make sure all checks pass.

The PR name needs to be in the format of [jira_ticket_id] - [Task description] 

</p>
