from ninja import Schema


class RoleIn(Schema):
    label: str


class RoleOut(Schema):
    label: str
    id: int


class CharacterOut(Schema):
    id: int
    name: str
    role: RoleOut
    alignment: str

class CharacterIn(Schema):
    name: str = None
    role: str = None
    alignment: str = None