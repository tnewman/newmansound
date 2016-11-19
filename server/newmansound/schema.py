from marshmallow import Schema, fields


class PlaylistRequestSchema(Schema):
    id = fields.Int()
