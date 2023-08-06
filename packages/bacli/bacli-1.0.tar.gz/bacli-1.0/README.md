# bacli
Born Again Command Line Interface.

Bacli is a module that wraps the command line argument parsing functionality of argparse for ease of use. Any Python function can be transformed into an entry point for the program. Simply add the `command` decorator, and you will be able to call the function directly from the command line (with parameters, documentation and correct types!).

### Usage

```
""" example.py: This file serves as a demonstration of the bacli functionality. """

import bacli

with bacli.cli(__doc__) as cli:

    @cli.command
    def run():
        """ Run the model. """
        print("Running")


    @cli.command
    def train(iterations: int, batch_size: int=32):
        """ Train the model. """
        print("Training model")
        print("{} iterations".format(iterations))
        print("batch size of {}".format(batch_size))

```

It can then be used as follows:  
```
> python example.py -h
usage: example.py [-h] subcommand ...

example.py: This file serves as a demonstration of the bacli functionality.

positional arguments:
  subcommand  Select one of the following subcommands:
    run       Run the model.
    train     Train the model.

optional arguments:
  -h, --help  show this help message and exit

```  

```
> python example.py run
Running

```

```
> python example.py train -h
usage: example.py train [-h] [--batch_size BATCH_SIZE] iterations

Train the model.

positional arguments:
  iterations            type: int

optional arguments:
  -h, --help            show this help message and exit
  --batch_size BATCH_SIZE
                        type: int, default=32

```

```
> python example.py train 10 --batch_size 64
Training model
10 iterations
batch size of 64

```


### Upcoming Features
 - Support for variable arguments (\*args and \*\*kwargs)
 - Support documentation of parameters
 - Support aliases of parameters (maybe use first leter as shortcut)
