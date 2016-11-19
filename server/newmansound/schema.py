from marshmallow import Schema, fields


class ArtistSchema(Schema):
    id = fields.Int()
    name = fields.String()


class AlbumSchema(Schema):
    id = fields.Int()
    name = fields.String()
    artist = fields.Nested('ArtistSchema')


class SongSchema(Schema):
    id = fields.Int()
    name = fields.String()
    album = fields.Nested('AlbumSchema')


class PlaylistRequestSchema(Schema):
    id = fields.Int()
