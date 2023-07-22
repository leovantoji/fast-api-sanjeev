import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import Base
from app.database import get_db
from app.main import app
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = (
    f"""postgresql://{settings.database_username}:{settings.database_password}"""
    f"""@{settings.database_hostname}:{settings.database_port}/"""
    f"""{settings.database_name}_test"""
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def dummy_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "p@ssword123",
    }
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def dummy_user2(client):
    user_data = {
        "email": "test2@gmail.com",
        "password": "p@ssword123",
    }
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(dummy_user):
    return create_access_token({"user_id": dummy_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def dummy_posts(dummy_user, dummy_user2, session):
    posts_data = [
        {
            "title": "Test Post 1",
            "content": "Test Content 1",
            "owner_id": dummy_user["id"],
        },
        {
            "title": "Test Post 2",
            "content": "Test Content 2",
            "owner_id": dummy_user["id"],
        },
        {
            "title": "Test Post 3",
            "content": "Test Content 3",
            "owner_id": dummy_user["id"],
        },
        {
            "title": "Test Post 3",
            "content": "Test Content 3",
            "owner_id": dummy_user2["id"],
        },
    ]

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    return session.query(models.Post).all()


@pytest.fixture
def dummy_vote(session, dummy_user, dummy_posts):
    new_vote = models.Vote(post_id=dummy_posts[3].id, user_id=dummy_user["id"])
    session.add(new_vote)
    session.commit()
