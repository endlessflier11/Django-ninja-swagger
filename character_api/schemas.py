from ninja import Schema


class RoleIn(Schema):
    label: str


class RoleOut(Schema):
    label: str
    id: int
