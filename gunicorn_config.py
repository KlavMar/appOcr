import multiprocessing

# bind to 0.0.0.0:8000 for external access
bind = "0.0.0.0:5000"

# number of worker processes to spawn
workers = multiprocessing.cpu_count() //2 

# set the maximum number of simultaneous clients
worker_connections = 1000

# set the timeout for a worker to complete a request
timeout = 400

# set the maximum number of requests a worker will process before restarting
max_requests = 1000

# log to stdout
accesslog = '-'
errorlog = '-'
