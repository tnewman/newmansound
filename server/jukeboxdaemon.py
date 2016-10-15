import signal
import sys
import time
import newmansound.database
from newmansound.service import AudioPlaybackService, JukeboxService, PlaylistService

stop_daemon = False


def run_jukebox_daemon():
    newmansound.database.init_db()
    signal.signal(signal.SIGINT, stop_jukebox_daemon)

    session = newmansound.database.session()
    playback_service = AudioPlaybackService()
    playlist_service = PlaylistService(session)
    jukebox_service = JukeboxService(playback_service, playlist_service)

    while not stop_daemon:
        try:
            jukebox_service.play_next_song()
            session.commit()
        except Exception:
            session.rollback()
            raise

        time.sleep(0.1)

    session.close()


def stop_jukebox_daemon(signal, frame):
    global stop_daemon
    stop_daemon = True
    sys.exit(0)

if __name__ == '__main__':
    run_jukebox_daemon()
