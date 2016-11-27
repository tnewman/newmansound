from marshmallow import Schema, fields


class BaseSchema(Schema):
    id = fields.Int()
    name = fields.String()


class ArtistSchema(BaseSchema):
    pass


class AlbumSchema(BaseSchema):
    artist = fields.Nested('ArtistSchema')


class SongSchema(BaseSchema):
    album = fields.Nested('AlbumSchema')


class PlaylistRequestSchema(Schema):
    id = fields.Int(required=True)
