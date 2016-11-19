from flask import Flask, request
from flask_restful import Api, Resource
from newmansound.database import scoped_session
from newmansound.schema import PlaylistRequestSchema, SongSchema
from newmansound.service import AudioPlaybackService, JukeboxService, PlaylistService, SongService

app = Flask('newmansoundrestweb')
api = Api(app)
app.session = scoped_session


class PlaylistRequest(Resource):
    def __init__(self):
        self.playlist_service = PlaylistService(app.session)
        self.playlist_request_schema = PlaylistRequestSchema()

    def post(self):
        json = request.get_json()
        song = self.playlist_request_schema.load(json).data
        self.playlist_service.enqueue_song(song['id'])
        app.session.commit()


class SongRequest(Resource):
    def __init__(self):
        self.song_schema = SongSchema()
        self.song_service = SongService(app.session)

    def get(self):
        songs = self.song_service.all()
        return self.song_schema.dump(songs)


api.add_resource(PlaylistRequest, '/playlist')
api.add_resource(SongRequest, '/song')


@app.teardown_appcontext
def shutdown_session(exception=None):
    scoped_session.remove()
