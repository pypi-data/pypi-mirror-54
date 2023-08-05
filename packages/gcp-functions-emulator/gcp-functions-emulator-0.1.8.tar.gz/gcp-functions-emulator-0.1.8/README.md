# Google Cloud Functions Python Emulator

This module tries to emulate the environment in Google Cloud Functions for
Python. It serves the given function on the given module.

For example. lets imagine we have the following cloud function
```python
# mycloudfunction.py
def api(request):
  return 'important data'
```
To emulate we have to call it tipically like so:
```
$ gcpfemu --module <path/to/my/module.py> --function <function_name>
```
For example, with the code above we will call it:
```
$ gcpfemu --module mycloudfunction.py --function api
```
And to access the data we can use for example curl:
```
$ curl localhost:5000/api
important data
```

If you want to run the emulator programatically you can do drun the server 
from a terminal, you have to disable the debug. It is
disabled by default thoug. Flask looks for file changes, but in interactive
terminal there's no file.
```python
from gcpfemu import http 
port = 1234 # use a different port
module_path = 'mycloudfunction.py' # set the path to the code itself
function_name = 'api' # set the function name
http(module_path, function_name, port, debug) # load and serve the function
```
For further help
```
gcpfemu --help
Usage: gcpfemu [OPTIONS]

  Serve functions using Flask

Options:
  -m, --module TEXT    path to the module containing the function  [required]
  -f, --function TEXT  name of the function as you wrote in the code [required]
  -e, --endpoint TEXT  name of the endpoint to use if differente from the function name
  -p, --port INTEGER   port number to use in the server
  -h, --http-methods [GET|POST]  http methods that server will be answering
  --help               Show this message and exit.
```
