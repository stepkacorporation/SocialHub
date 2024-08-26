from fastapi import FastAPI

from app.routers import social_profiles
from app.routers.auth import routes as auth

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {
        'project': 'SocialHub',
        'author': 'Kornev Stepan',
        'GitHub': 'https://github.com/stepkacorporation/SocialHub.git'
    }


app.include_router(auth.router)
app.include_router(social_profiles.router)
