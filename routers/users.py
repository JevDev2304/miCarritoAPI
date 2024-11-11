from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from connection import execute_query
from hashing.criptography import *
from schemas.CreateUser import CreateUserDTO
from schemas.LoginUser import LoginUserDTO

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

@usersRouter.post('/login',status_code=status.HTTP_200_OK)
async def login(loginUserDto: LoginUserDTO):
    query = 'SELECT * FROM users where mail = %s'
    params = ( loginUserDto.mail,)
    try:
        user = await execute_query(query, params)
        if len(user) == 1:
            if check_password(loginUserDto.password,user[0]['password']):
                del user[0]['password']
                return user[0]

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong credentials')
    except UniqueViolation :
        # Manejar el error con una respuesta adecuada
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Already exist an User with this email')
