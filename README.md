# PipeRT2

<p align="center">
<a href="https://github.com/OperationalBina/PipeRT2/actions"><img alt="Actions Status" src="https://github.com/OperationalBina/PipeRT2/workflows/Test/badge.svg"></a>
<a href="https://badge.fury.io/py/PipeRT"><img src="https://badge.fury.io/py/PipeRT.svg" alt="PyPI version" height="18"></a>  <a href='https://operationalbina.github.io/PipeRT2/'>
    <img src='https://github.com/OperationalBina/PipeRT2/actions/workflows/docs.yml/badge.svg' alt='Documentation Status' />
  </a>
<a href="https://codecov.io/gh/OperationalBina/PipeRT2">
    <img src="https://codecov.io/gh/OperationalBina/PipeRT2/branch/master/graph/badge.svg?token=ze7192iCby"/>
  </a>

PipeRT2 is an infrastructure for analyze videos with the ability 
of handling a high FPS rate.

Design a complex dataflow dynamically can be done using PipeRT2. 
With a simple implementation of pipe's components a full dataflow can be dispatched. 

**Table of contents**
- [Requirements](#requirements)
- [Components](#components)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Requirements

- Python 3.6

## Components

**Routine** - the smallest component in the pipe.

Each routine has to implement a `main_logic` function that contains the business logic of the routine.

There are three types of routines - 

- **SourceRoutine** - The first routine in a pipe. Using for generating new data and producing it 
to the pipeline. 
- **MiddleRoutine** - Consumes data and produce its manipulation into the pipeline. 
- **DestinationRoutine** - The last routine of the pipe. Using for storing the results from all data manipulation. 

**Flow** - Contains a multiple routines with a same logic.

**Pipe** - Contains all flows. Notifies events through all its components.

## Getting Started 

We publish PipeRT2 as `PipeRT` package in PyPi. 
Run `pip3 install PipeRT` for installing the official PipeRT2 stable version. 

For example, we're going to create a pipe contains simple flows created by routines.

First we create the source class that generates data:

```'''Python
from pipert2 import SourceRoutine

class GenerateData(SourceRoutine):

    def main_logic(self) -> dict:
        return {
            "value": "example"
        }
```

Then we create the destination routine to store (in our case print) the pipeline's result:

```'''Python
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
example_pipe = Pipe(QueueNetwork())

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

# Contributing

For contributing please contact with [San-Moshe](https://github.com/San-Moshe) for accessing our Jira. 

Please follow the conventions using in the project and make sure all checks pass.

The PR name needs to be in the format of [jira_ticket_id] - [Task description] 

</p>
