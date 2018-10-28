import threading
import multiprocessing
import numpy as np
import tensorflow as tf
import example_controllers.behavior_reflex.playGame_DDPG as playGame_DDPG 
import os
from random import choice
from time import sleep
from time import time

import sys
import json
#import pymp

if __name__ == "__main__":

        config_dict = None
        num_workers = 3

        if len(sys.argv) > 1:
                json_config = sys.argv[1]

                with open(json_config, 'r') as f:
                        config_dict = json.load(f)
                
                num_workers = config_dict['num_agents']

                

        with tf.device("/cpu:0"): 
                # num_workers = 3 #multiprocessing.cpu_count() #use this when you want to use all the cpus
                print("numb of workers is" + str(num_workers))

        with tf.Session() as sess:
                worker_threads = []
        #with pymp.Parallel(4) as p:		#uncomment this for parallelization of threads
                for i in range(num_workers):
                        worker_work = lambda: (playGame_DDPG.playGame(f_diagnostics=""+str(i), train_indicator=1, port=3001+i, config_dict=config_dict))
                        t = threading.Thread(target=(worker_work))
                        t.start()
                        sleep(0.5)
                        worker_threads.append(t)
