import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue
    total=os.listdir(top_dir)
    queue_buffer.put(top_dir,timeout=0.5)
    for i in total:
        direct=os.path.join(top_dir,i)
        if os.path.isdir(direct):
            producer(direct,queue_buffer)
            print(direct)

def consumer(queue_buffer):
    # search file in directory
    global file_count
    path=queue_buffer.get(timeout=0.5)
    num=os.listdir(path)
    for i in num:
        if os.path.isfile(os.path.join(path,i)):
            lock.acquire()
            file_count+=1
            lock.release()

def main():
    producer_thread = threading.Thread(target = producer, args = (r'.\testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    global file_count
    print(file_count, 'files found.')

if __name__ == "__main__":
    main()
