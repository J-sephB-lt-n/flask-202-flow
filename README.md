# flask-202-flow

Illustration of a Flask endpoint which continues to run code *after* a 202 response is sent to the client.

```bash
# host HTTP server #
gunicorn --bind :5000 --workers 1 --threads 4 --timeout 30 main:app
```

```bash
# send a request #
curl --request POST \
'http://localhost:5000/202_flow_example?wait_n_secs_after_response=10'
```
```
Endpoint Response:  ACCEPTED (202) at 20:56:54.379
2023-11-27 20:56:54,380 INFO started after response code
2023-11-27 20:56:55,385 INFO waited 1 seconds
2023-11-27 20:56:56,390 INFO waited 2 seconds
2023-11-27 20:56:57,394 INFO waited 3 seconds
2023-11-27 20:56:58,399 INFO waited 4 seconds
2023-11-27 20:56:59,403 INFO waited 5 seconds
2023-11-27 20:57:00,408 INFO waited 6 seconds
2023-11-27 20:57:01,411 INFO waited 7 seconds
2023-11-27 20:57:02,417 INFO waited 8 seconds
2023-11-27 20:57:03,420 INFO waited 9 seconds
2023-11-27 20:57:04,423 INFO waited 10 seconds
2023-11-27 20:57:04,427 INFO finished waiting 10 seconds
```

A request not generating a `202` response will not run the *after response* code:
```bash
# send a request #
curl --request POST \
'http://localhost:5000/202_flow_example?wait_n_secs_after_response=99999'
```
```
Endpoint Response:  FORBIDDEN (403) at 20:58:45.598
```