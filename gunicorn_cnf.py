import multiprocessing
import os


size = int(os.getenv('SIZE', 1))
# Maximum 5 worker per 128MB
workers = min(multiprocessing.cpu_count() * 2 + 1, size * 5)
timeout = 120
