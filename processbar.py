# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 09:24:28 2015

@author: ydzhao
"""

import os  
import sys  
import cmd  
import unicodedata  
from threading import Thread  
from time import sleep  
  
class ProgressBar(Thread):  
    """A simple text progress bar control."""  
  
    def __init__(self):  
        self.running = True  
        self.percent = -1  
        self.msg = ""  
        Thread.__init__(self)  
  
    def run(self):  
        i = 1  
        while self.running and self.percent < 100:  
            display = '\r'  
  
            if self.msg != "":   
                display += self.msg + ' '  
  
            if self.percent >= 0:  
                display += str(self.percent) + '% '  
                display += '-' * (40 * self.percent / 100)  
  
            if i + 1 + len(display) > 80:   
                i = 1  
  
            display += '-' * i  
            display += '>'  
            display += ' ' * (80 - len(display))  
            sys.stderr.write(display)  
  
            i += 1  
            sleep(0.5)  
  
        sys.stderr.write('\r' + ' ' * 79 + '\r')  
        sys.stderr.flush()  
  
    def stop(self):  
        """Stop displaying progress bar. 
 
        Note: there may be latency to stop. You'd better wait for the thread 
        stops. See _stop_progress(t_bar). 
 
        """  
        self.running = False  
  
    def set_percent(self, percent, msg = ""):  
        """Call back method for owner of progress bar."""  
        self.percent = int(percent)  
        self.msg = msg  
      
    def is_alive(self):  
        return self.isAlive()  
  
  
def _start_progress():  
    """Display a progress bar"""  
    t_bar = ProgressBar()  
    t_bar.start()  
    return t_bar   
  
def _stop_progress(t_bar):  
    """Hide the progress bar"""  
    if hasattr(t_bar, "is_alive"):  
        alive = t_bar.is_alive()  
    else:  
        alive = t_bar.isAlive()  
  
    if t_bar and alive:  
        t_bar.stop()  
        t_bar.join()  
  
def _set_progress(t_bar,percent,msg = ""):  
    t_bar.set_percent(percent,msg)  
      
def _print_msg(t_bar, *args):  
    """Hide the progress bar and print message"""  
  
    assert t_bar is None or isinstance(t_bar, ProgressBar)  
  
    if t_bar and t_bar.is_alive():   
        _stop_progress(t_bar)  
  
    print ' '.join(args)  
  
def _unicode_str_width(text):  
    """Calculate the exact width of unicode string."""  
  
    width = 0  
    for char in text:  
        if isinstance(char, unicode):  
            if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):  
                width += 2  
            else:  
                width += 1  
        else:  
            width += 1  
  
    return width  
      
#Test the progress bar      
if __name__ == "__main__":  
    t_bar = _start_progress()  
    count = 0;  
    while count<100:  
        _set_progress(t_bar,count)  
        sleep(0.1)  
        count = count+1  
          
    _stop_progress(t_bar)  
    print "Done!"  