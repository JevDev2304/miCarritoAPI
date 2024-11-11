from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation
from connection import execute_query
from hashing.criptography import *
from schemas.CreateUser import CreateUserDTO
from schemas.LoginUser import LoginUserDTO
from schemas.UpdateUser import UpdateUserDTO

usersRouter = APIRouter(prefix="/users",
    tags=["Users"])


@usersRouter.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(createUserDto: CreateUserDTO):
    query = 'INSERT INTO users (mail, password, itsadmin, address) VALUES (%s, %s, %s, %s) RETURNING *'
    password =hash_password(createUserDto.password)
    params = (createUserDto.mail, password, createUserDto.itsadmin, createUserDto.address)

    try:
        user = await execute_query(query, params)
        del user[0]['password']
        return user[0]
    except UniqueViolation :
        # Manejar el error con una respuesta adecuada
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Already exist an User with this email')


@usersRouter.put('/',status_code=status.HTTP_200_OK)
async def update_user(updateUserDto: UpdateUserDTO):
    users = await get_user_by_email(updateUserDto.mail)
    if len(users) == 1:
        if updateUserDto.password is None:
            updateUserDto.password=users[0]['password']
        else:
            updateUserDto.password = hash_password(updateUserDto.password)
        if updateUserDto.itsadmin is None:
            updateUserDto.itsadmin= users[0]['itsadmin']
        if updateUserDto.address is None:
            updateUserDto.address = users[0]['address']
        before_update_user = users[0]
        print(before_update_user)
        print(updateUserDto)
        before_update_user.update(**dict(updateUserDto))
        try:
            query = 'UPDATE users SET  password=%s, itsadmin=%s, address=%s WHERE mail = %s RETURNING *'
            params = (
            before_update_user['password'], before_update_user['itsadmin'], before_update_user['address'], before_update_user['mail'])
            await execute_query(query, params)
            del before_update_user['password']
            return before_update_user
        except UniqueViolation :
            # Manejar el error con una respuesta adecuada
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Already exist an User with this email')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    elif len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are not users  with this email')
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@usersRouter.post('/login',status_code=status.HTTP_200_OK)
async def user_login(loginUserDto: LoginUserDTO):
    user = await get_user_by_email(loginUserDto.mail)
    if len(user) == 1:
        if check_password(loginUserDto.password, user[0]['password']):
            del user[0]['password']
            return user[0]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong credentials')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Does not exist an User with these credentials')






async def get_user_by_email(email: str):
    query = 'SELECT * FROM users where mail = %s'
    params = (email,)
    users = await execute_query(query, params)
    return users

