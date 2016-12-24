from flask import abort, Flask, jsonify, request
from flask_restful import Api, Resource
from newmansound.database import scoped_session
from newmansound.schema import AlbumSchema, ArtistSchema, PlaylistRequestSchema, SongSchema
from newmansound.service import AlbumService, ArtistService, AudioPlaybackService, JukeboxService, PlaylistService, \
    SongService

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


class BaseResource(Resource):
    def __init__(self, schema, service):
        self.schema = schema
        self.service = service

    def get(self, id):
        data = self.service.get(id)

        if not data:
            abort(404)

        json = self.schema.dump(data).data
        return json


class BaseListResource(Resource):
    def __init__(self, schema, service):
        self.schema = schema
        self.service = service

    def get(self):
        data = self.service.all()
        json = self.schema.dump(data, many=True).data
        return json


class AlbumList(BaseListResource):
    def __init__(self):
        super().__init__(AlbumSchema(), AlbumService(app.session))


class Album(BaseResource):
    def __init__(self):
        super().__init__(AlbumSchema(), AlbumService(app.session))


class ArtistList(BaseListResource):
    def __init__(self):
        super().__init__(ArtistSchema(), ArtistService(app.session))


class Artist(BaseResource):
    def __init__(self):
        super().__init__(ArtistSchema(), ArtistService(app.session))


class SongList(BaseListResource):
    def __init__(self):
        super().__init__(SongSchema(), SongService(app.session))


class Song(BaseResource):
    def __init__(self):
        super().__init__(SongSchema(), SongService(app.session))


api.add_resource(PlaylistRequest, '/playlist')
api.add_resource(AlbumList, '/album')
api.add_resource(Album, '/album/<id>')
api.add_resource(ArtistList, '/artist')
api.add_resource(Artist, '/artist/<id>')
api.add_resource(SongList, '/song')
api.add_resource(Song, '/song/<id>')


@app.teardown_appcontext
def shutdown_session(exception=None):
    scoped_session.remove()
