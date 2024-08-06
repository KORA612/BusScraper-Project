import threading
import itertools
import time
import sys
import multiprocessing
import subprocess


name = "scrape.py"


# ['.', 'o', 'O', '()']
# ['|  /  -', '/  -  \\', '-  \\  |', '\\  |  /']

def loading_animation(done_flag):
    for c in itertools.cycle(['. . .', 'o o o', 'O O O', '0 0 0', '0 0 0', 'O O O', 'o o o', '. . .']):
        if done_flag.is_set():
            break
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     \n')


def run_smth_script():
    subprocess.run(["python", name])


def run_main_task_with_animation():
    done_flag = threading.Event()

    # Create and start the loading animation thread
    loading_thread = threading.Thread(
        target=loading_animation, args=(done_flag,))
    loading_thread.start()

    # Create and start the smth.py process
    smth_process = multiprocessing.Process(target=run_smth_script)
    smth_process.start()

    # Wait for the smth.py process to complete
    smth_process.join()

    # Signal the loading animation to stop and wait for it to finish
    done_flag.set()
    loading_thread.join()


if __name__ == "__main__":
    run_main_task_with_animation()

