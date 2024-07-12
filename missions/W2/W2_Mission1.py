import multiprocessing
import time

tasks = [
    ('A', 3),
    ('B', 2),
    ('C', 1),
    ('D', 4)
]

def work_log(task):
    name, duration = task
    print(f"Task {name} is waiting for {duration} seconds")
    time.sleep(duration)
    print(f"Task {name} is finished")

if __name__ == '__main__':
    pool = multiprocessing.Pool(2)
    
    pool.map(work_log, tasks)
    
    pool.close()
    pool.join()
