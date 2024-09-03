import threading
import subprocess
import argparse

def run_command(command):
    """
    Execute a command in the shell.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def main(opt):
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
            if opt.use_yolo:
                command = f'python3 run_grid.py --use-yolo --source "{source}" --stream-idx "{idx}" --factor {opt.factor}'
            else:
                command = f'python3 run_grid.py --source "{source}" --stream-idx "{idx}" --factor {opt.factor}'
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

parser = argparse.ArgumentParser()
parser.add_argument('--factor', type=float, default=0.25, help='scale down factor')
parser.add_argument('--use-yolo', action='store_true', help='use yolo instead of HOG + Linear SVM')  
opt = parser.parse_args()

if __name__ == "__main__":
    try:
        main(opt)
    except KeyboardInterrupt:
        print("Exit")
