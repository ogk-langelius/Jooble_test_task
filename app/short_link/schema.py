from marshmallow import fields, Schema, validate


class LinkSchema(Schema):
    """schema for links"""
    linkId = fields.Number(attribute='link_id')
    originalLink = fields.String(attribute='original_link')
    shortId = fields.String(attribute='short_id')
    expiresAt = fields.DateTime(attribute='expires_at')


class CreateLinkSchema(Schema):
    """schema for short links creation"""
    linkId = fields.Number(attribute='link_id')
    originalLink = fields.String(attribute='original_link')
    daysToExpiration = fields.Number(attribute='days_to_expiration', validate=validate.Range(1, 365))
