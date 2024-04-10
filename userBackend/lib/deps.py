from bson.objectid import ObjectId
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from lib.db import get_database
from utils.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        database = await get_database()
        payload = decode_access_token(token)
        userId: str = payload.get("id")
        if userId is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except AttributeError:
        raise credentials_exception
    user =  database.users.find_one({"_id": ObjectId(userId)})
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "userName": user["userName"],
        "balance": user["balance"]
    }