from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from cassandra.cqlengine.management import sync_table

from app.schema.user_schema import UserSchema


from . import config, db
from .user_model.models import User


app = FastAPI()
# settings = config.get_settings()


@app.on_event('startup')
def on_startup():
    print('Hello World')
    db.get_session()
    sync_table(User)


@app.get('/')
def home_page():
    return {'hello': 'world'}


#! This endpoint List all the users in the database
@app.get('/users')
def get_all_users():
    qs = User.objects.all().limit(10)
    return list(qs)


#! This endpoint create/add new user to the database
@app.post('/users', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    email = User.objects.filter(email=user.email)

    # ! Check if email already exist in the database
    if email.count() != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{user.email} already exists!')
    user = User.objects.create(email=user.email, password=user.password)
    user.save()
    return user
