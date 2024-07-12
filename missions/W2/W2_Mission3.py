import multiprocessing
import time

def push_items(queue, items):
    print("pushing items to queue:")
    for i, item in enumerate(items):
        print(f"item no: {i} {item}")
        queue.put((i, item))
        time.sleep(0.5)  

def pop_items(queue):
    print("\npopping items from queue:")
    while not queue.empty():
        i, item = queue.get()
        print(f"item no: {i} {item}")
        time.sleep(0.5) 

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    items = ['red', 'green', 'blue', 'black']
    
    p1 = multiprocessing.Process(target=push_items, args=(queue, items))
    p2 = multiprocessing.Process(target=pop_items, args=(queue,))
    
    p1.start()
    p1.join()  
    
    p2.start()
    p2.join()
