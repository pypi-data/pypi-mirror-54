#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Simple classes that handle threaded acquisition of data.
#  
#  License: MIT
#  
#  Copyright (c) 2019 Joerg Beckers

import threading
import time

class DataAcquisitionHandler():
    """ Base class for a handler which acquires new data and stored it in the supplied dictionary 'sharedDict'.
        Derive this class and override the 'acquireData' - methods to fill the 'sharedDict'.
    """
    
    def __init__(self, sharedDict=None):
        """ The contructor gets a dictionary which will be used to store any acquired data.
        """
        self.setSharedDict(sharedDict)

    def setSharedDict(self, sharedDict):
        """ Set the shared dictionary
        """
        self.sharedDict = sharedDict

    def prepare(self):
        """ This method is called before the data acquisition thread is started with this handler.
            So if you need to initialize parts of the shared dictionary you should override this method.
        """
        pass

    def acquireData(self):
        """ This method is called by a 'DataAcquisitionThread'. Override this method to retrieve data and save the data in 'sharedDict'.
        """
        pass

class DataAcquisitionThread(threading.Thread):
    """ A thread class which handles cyclic data acquisition.

        An instance of this class needs a lock - object for controlling access to its 'dataAcquisitionHandler', an event - object for 
        notifying the thread to exit and an object of a class derived from 'DataAcquisitionHandler'.
    """
    def __init__(self, threadSleep=0, shutdownFlag=None, dataLock=None, dataAcquisitionHandler=None):
        """ Contructs a new instance of 'DataAcquisitionThread'.
            
            Parameters:
            
            threadSleep             - milliseconds sleep time for the thread loop.
            shutdownFlag            - a threading.event() object for notifying the thread to exit.
            dataLock                - a threading.Lock() object for controlling access to the 'dataAcquisitionHandler'.
            dataAcquisitionHandler  - an object of a class derived from 'DataAcquisitionHandler'.
        """
        threading.Thread.__init__(self)

        self.threadSleep = threadSleep
        self.shutdownFlag = shutdownFlag
        self.dataLock = dataLock
        self.dataAcquisitionHandler = dataAcquisitionHandler
        
    def run(self):
        """ The thread loop runs until 'shutdownFlag' has been signaled. Sleep for 'threadSleep' milliseconds.
        """
        # Let the handler prepare it's section within the shared dictionary.
        self.dataLock.acquire()
        self.dataAcquisitionHandler.prepare()
        self.dataLock.release()

        while not self.shutdownFlag.is_set():
            # acquire lock
            self.dataLock.acquire()
            # call data acquisition handler
            self.dataAcquisitionHandler.acquireData()
            # release lock
            self.dataLock.release()
            self.shutdownFlag.wait(self.threadSleep)
