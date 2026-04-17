from pydantic import BaseModel

class UserTessituraRequest(BaseModel):
    tessitura: str