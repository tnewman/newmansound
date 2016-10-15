from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from newmansound.database import scoped_session
from newmansound.service import AudioPlaybackService, JukeboxService, PlaylistService

app = Flask('newmansoundrestweb')
api = Api(app)
app.session = scoped_session

parser= reqparse.RequestParser()
parser.add_argument('song_id', int)


class PlaylistRequest(Resource):
    def __init__(self):
        self.playlist_service = PlaylistService(app.session)

    def post(self):
        args = parser.parse_args()
        song_id = args['song_id']
        self.playlist_service.enqueue_song(song_id)
        app.session.commit()


api.add_resource(PlaylistRequest, '/playlist')

@app.teardown_appcontext
def shutdown_session(exception=None):
    scoped_session.remove()
