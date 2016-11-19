from marshmallow import Schema, fields


class ArtistSchema():
    id = fields.Int()
    name = fields.String()


class AlbumSchema():
    id = fields.Int()
    name = fields.String()
    artist = fields.Nested('ArtistSchema')


class SongSchema():
    id = fields.Int()
    name = fields.String()
    album = fields.Nested('AlbumSchema')


class PlaylistRequestSchema(Schema):
    id = fields.Int()
