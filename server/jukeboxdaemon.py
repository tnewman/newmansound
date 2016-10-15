import signal
import sys
import time
from newmansound.model import Base
from newmansound.service import AudioPlaybackService, JukeboxService, PlaylistService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///newmansound.db')
Session = sessionmaker(bind=engine)

stop_daemon = False


def run_jukebox_daemon():
    Base.metadata.create_all(bind=engine)
    signal.signal(signal.SIGINT, stop_jukebox_daemon)

    while not stop_daemon:
        session = Session()

        playback_service = AudioPlaybackService()
        playlist_service = PlaylistService(session)
        jukebox_service = JukeboxService(playback_service, playlist_service)

        try:
            jukebox_service.play_next_song()
            session.commit()
        except Exception:
            session.rollback()
            raise

        time.sleep(0.1)


def stop_jukebox_daemon(signal, frame):
    global stop_daemon
    stop_daemon = True
    sys.exit(0)

if __name__ == '__main__':
    run_jukebox_daemon()
