from signal import pause

from sessions import Session

if __name__ == '__main__':
    sesh = Session()
    sesh.start()
    pause()