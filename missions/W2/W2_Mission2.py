import multiprocessing

def print_continent_name(continent="Asia"):
    print(f"The name of continent is : {continent}")

if __name__ == '__main__':
    continents = ["America", "Europe", "Asia", "Africa"]
    
    
    processes = []

    for continent in continents:
        process = multiprocessing.Process(target=print_continent_name, args=(continent,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
