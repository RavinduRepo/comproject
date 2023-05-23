import multiprocessing
import time

def secondary_process(stop_flag):
    while not stop_flag.value:
        print("Secondary process running...")
        time.sleep(1)

    print("Secondary process stopped.")

if __name__ == '__main__':
    # Create a shared variable to signal the secondary process to stop
    stop_flag = multiprocessing.Value('i', 0)

    # Create the secondary process
    process = multiprocessing.Process(target=secondary_process, args=(stop_flag,))
    print("started")
    # Wait for some time before starting the secondary process
    time.sleep(5)

    # Start the secondary process
    process.start()
    

    # Wait for some more time before stopping the secondary process
    time.sleep(5)

    # Set the stop flag to terminate the secondary process
    stop_flag.value = 1

    # Wait for the secondary process to finish
    process.join()

    print("Main code execution continued.")
