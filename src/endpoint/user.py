from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from model.data.user import User, UserRegister
from beanie import PydanticObjectId
from depends import sample_depends


userRouter = APIRouter()


@userRouter.get("")
async def retrieve_a_user_by_user_id(userId: PydanticObjectId):
    user = await User.get(userId)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@userRouter.post("", response_model=User, dependencies=[Depends(sample_depends)])
async def post_a_user(body: User):
    await body.create()
    return body


@userRouter.patch("", response_model=User)
async def post_a_user(body: UserRegister):
    user = await User(userName=body.userName).get(body.id)
    user.firstName = body.firstName
    user.lastName = body.lastName
    user.userName = body.userName
    user.address = user.address
    user.locate = user.locate
    user.oreRegister = False
    user.updatedAt = datetime.utcnow()
    await user.save_changes()
    return user
