import subprocess
import sys 
import os
from logger import logging

logger1=logging.getLogger('Running')
logger1.setLevel(logging.DEBUG)

logger2=logging.getLogger('Error/Exception')
logger2.setLevel(logging.ERROR)


def install_requirements():
    logger1.critical('First time run detected. Installing requirements...')
    flag_file = os.getcwd() + '\\.first_run'
    if not os.path.exists(flag_file):
        print("First run detected. Installing requirements...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', f'{os.getcwd()}\\requirements.txt'])
        # Create flag file after successful installation
        with open(flag_file, 'w') as f:
            f.write('Installation completed')

install_requirements()


import cv2
import keyboard
from time import time

def start_fresh():
    print(' If you want to start fresh press "Enter", else press "Shift"')
    while True:

        if keyboard.is_pressed('enter'):
            try:
                os.remove(os.getcwd() + 'prevoius_elapsed_time')
                print("Starting fresh...")
                logger1.info('Starting fresh...')
            except FileNotFoundError:
                print("No previous session found. Starting fresh...")            
            return False
        elif keyboard.is_pressed('shift'):
            print('Continuing from previous session...')
            logger1.info('Continuing from previous session...')

            return False

class CodeArea:  
    
    def __init__(self):
        
        # Load the face cascade
        self.face_cascade = cv2.CascadeClassifier(f"{os.getcwd()}\\haarcascade_frontalface_alt.xml")

        # Initialize variables
        self.cap = cv2.VideoCapture(0)
        self.start_time = None  # Start time of the active session
        self.is_running = False  # Indicates whether the timer is running
        self.face_detected = False  # Tracks if a face is currently detected
        self.pause_start_time = 0  # Time when the pause started
        self.elapsed_time_before_pause = 0  # Total elapsed time before pause
        self.last_check_time = time()
        self.wait_time_face_detected = 60  # Time interval for checking face detection
        self.wait_time_face_not_detected = 5  # Time interval for checking face absence
        self.manual_pause = False  # Tracks if the system is manually paused
        self.current_time = None
        self.elapsed_pause_time = 0

    def save_prev_time(self, elapsed_time):
        with open(os.getcwd() + '\\prevoius_elapsed_time', 'w+') as time_record:
            time_record.write(str(elapsed_time))
            time_record.flush() 
            '''FLUSH() method is used to force the data written to a file or output stream to be immediately transferred from the internal buffer to the destination.'''
            logger1.critical('Previous time saved')
    
    def fetch_prev_time(self):
            try:
                with open(os.getcwd() + '\\prevoius_elapsed_time', 'r') as time_fetch:
                    elapsed_time = float(time_fetch.readline().strip())
                    return elapsed_time
            except:
                logger2.error('Unable to fetching previous time')
                return False
            

    def start_scan(self):
        while True:
            if not self.manual_pause:  # If not manually paused
                ret, img = self.cap.read()
                if not ret:
                    print("Failed to capture image.")
                    break

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = []

                self.current_time = time()
                elapsed_since_last_check = self.current_time - self.last_check_time

                # Face detection logic
                if (self.face_detected and elapsed_since_last_check >= self.wait_time_face_detected) or \
                        (not self.face_detected and elapsed_since_last_check >= self.wait_time_face_not_detected):

                    self.last_check_time = self.current_time
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

                    if len(faces) > 0:

                        if not self.is_running:
                            if self.start_time is None:
                                self.elapsed_time_before_pause = self.fetch_prev_time() or 0
                                self.start_time = time() - 3  # countering delay in process by adding 3sec
                            else:
                                self.start_time = time()
                            self.is_running = True
                            #self.start_time = time()
                            logger1.info('Face detected')


                        self.face_detected = True

                    else:
                        """No Face Detected: Pause Timer"""
                        if self.is_running:
                            self.elapsed_time_before_pause += time() - self.start_time
                            self.is_running = False
                            #self.
                            #  = ()
                        self.face_detected = False
                        logger1.warning('No face detected')

                # Display the timer on the frame
                if self.is_running:
                    elapsed_time = time() - self.start_time + self.elapsed_time_before_pause
                    hours = int(elapsed_time // 3600)
                    minutes = int((elapsed_time % 3600) // 60)
                    seconds = int(elapsed_time % 60)
                    time_text = f'Time: {hours:02}:{minutes:02}:{seconds:02}'
                    cv2.putText(img, time_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                cv2.imshow('img', img)

            # Manual pause and resume logic
            if keyboard.is_pressed('shift+w+e'):  # Pause manually
                if not self.manual_pause:
                    if self.is_running:
                        self.elapsed_time_before_pause += time() - self.start_time
                    self.is_running = False
                    self.manual_pause = True
                    #self.pause_start_time = time()
                    self.cap.release()
                    cv2.destroyWindow('img')
                    print('Paused...')
                    logger1.info('Paused')

            elif keyboard.is_pressed('shift+q+e'):  # Resume manually
                if self.manual_pause:
                    self.cap = cv2.VideoCapture(0)
                    self.manual_pause = False
                    self.start_time = time()
                    #self.is_running = True
                    self.last_check_time = time() - 60 
                    print('Resumed...')
                    logger1.info('Resumed')

            if cv2.waitKey(1) & 0xFF == 27:  # Exit on ESC
                if self.is_running:
                    self.elapsed_time_before_pause += time() - self.start_time
                    self.save_prev_time(self.elapsed_time_before_pause)
                print('Exiting...')
                logger1.warning('Exiting...')
                break

        def __del__(self):
            self.running = False
            cv2.destroyAllWindows()

            ''' hasattr is a built-in Python function used to check if an object has a specific attribute. 
            It returns True if the attribute exists, otherwise False.'''    
            if hasattr(self, 'cap'): 
                self.cap.release() 
                logger2.critical('Camera released sucessfully')
    
        '''if self.cap.isOpened():

            self.cap.release()

        cv2.destroyAllWindows()''' 
        



# Instantiate the CodeArea class and start the scan
if __name__ == "__main__":
    try:
        start_fresh()
        code = CodeArea()
        code.start_scan()
    except:
        code.save_prev_time(code.elapsed_time_before_pause)