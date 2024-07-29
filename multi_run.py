import threading
import subprocess

def run_command(command):
    """
    Execute a command in the shell.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def main():
    # read source streams 
    with open("source.streams","r") as f:
        sources = f.readlines()
    sources = [item.strip("\n") for item in sources]

    # make sure we "zero-pad" the sources to 6 sources
    while len(sources) < 6:
        sources.append('zero-pad')

    # define list to store all threads
    threads  = []

    # loop all source
    for idx, source in enumerate(sources):
        # command
        try:
            command = f'python3 run_grid.py --use-yolo --source "{source}" --stream-idx "{idx}"'
        except:
            raise NotImplementedError

        # thread
        thread = threading.Thread(target=run_command, args=(command,))
        threads.append(thread)        

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
