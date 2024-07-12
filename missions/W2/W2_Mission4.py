import multiprocessing
import time

def worker(task_queue, done_queue, process_id):
    while True:
        try:
            task = task_queue.get_nowait()
        except multiprocessing.queues.Empty:
            break
        else:
            print(f"Process-{process_id} executing Task no {task}")
            time.sleep(0.5) 
            done_queue.put(f"Task no {task} is done by Process-{process_id}")

if __name__ == '__main__':
    tasks_to_accomplish = multiprocessing.Queue()
    tasks_that_are_done = multiprocessing.Queue()
    
    for task in range(10):
        tasks_to_accomplish.put(task)
    
    processes = []
    for process_id in range(1, 5):
        process = multiprocessing.Process(target=worker, args=(tasks_to_accomplish, tasks_that_are_done, process_id))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())
