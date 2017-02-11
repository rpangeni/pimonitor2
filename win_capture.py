import numpy as np
import cv2
import emailapp
import logging
import os
import json
import logging.config

def setup_logging( default_path='pi_logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def doCapture():
    logger = logging.getLogger("WinCapture")
    logger.info("starting to capture")
    cap = cv2.VideoCapture(0)


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Completed the capture")

if __name__ == '__main__':
    setup_logging()
    doCapture()
