
Task purpose
------
Run tasks is an agent that allow the remote execution of tasks.

How to run?
----------
1. Run celery
 ```celery --app=src.utils.server_interface worker --pool=solo --loglevel=info ```
2. Create virtual environment using the requirements.txt file for package installation: <br>
``` pip install -r requirements.txt ``` 
3. Running the program by executing server.py file, port server is customizable.

RestAPI:
-------

The agent supports the below APIs:

POST ```http://localhost:<port>>/api/run-task/start_server``` <br>
Body:
```
{
    "port": "<port>",
    "uri": "<uri>",
    "data_to_return": "<data_to_return>"
}
```
Headers:
```
user: <username>
```

port - the access port to the new server
uri - the uri
data_to_return - the data that the new server will return

Response will be as follows:
```
{
    "status": "Task started",
    "task_id": "<id>"
}
```

Checking the server status: <br>
GET ``` http://localhost:<port>/api/run-task/server_status/<id> ```


Accessing the newly created server: <br>
GET ``` http://localhost:<port>/<uri> ```

Response:
```
<data_to_return>
Requested by: <user>
```



Perform HTTP get request, retrive a data from the provided url: <br>
POST ``` http://localhost:<port>/api/run-task/get_page ```
```
{
    "domain": "http://www.google.com",
    "port": <port>
}
```

Running DNS query for the provided domain: <br>
POST ``` http://localhost:5555/api/run-task/get_ip_dns ```
```
{
    "domain": "http://www.google.com"
}
```

Response:
```
{
    "IP": "142.250.75.132",
    "hostname": "www.google.com"
}
```
