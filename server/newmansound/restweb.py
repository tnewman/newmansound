from flask import abort, Flask, jsonify, request
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
        song, error = self.playlist_request_schema.load(json)

        if error:
            abort(400)

        self.playlist_service.enqueue_song(song['id'])
        app.session.commit()


class SongList(Resource):
    def __init__(self):
        self.song_schema = SongSchema()
        self.song_service = SongService(app.session)

    def get(self):
        songs = self.song_service.all()
        data = self.song_schema.dump(songs, many=True).data
        return data


class Song(Resource):
    def __init__(self):
        self.song_schema = SongSchema()
        self.song_service = SongService(app.session)

    def get(self, song_id):
        song = self.song_service.get(song_id)

        if not song:
            abort(404)

        data = self.song_schema.dump(song).data
        return data


api.add_resource(PlaylistRequest, '/playlist')
api.add_resource(SongList, '/song')
api.add_resource(Song, '/song/<song_id>')


@app.teardown_appcontext
def shutdown_session(exception=None):
    scoped_session.remove()
