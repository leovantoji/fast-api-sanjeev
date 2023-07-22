import pytest
from fastapi import status

from app import schemas


def test_get_all_posts(authorized_client, dummy_posts):
    res = authorized_client.get("/posts/")
    posts_list = [schemas.PostOut(**post) for post in res.json()]

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(posts_list)


def test_get_all_posts_unauthorized_user(client, dummy_posts):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client, dummy_posts):
    res = authorized_client.get("/posts/999")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post_unauthorized_user(client, dummy_posts):
    res = client.get(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post(authorized_client, dummy_posts):
    res = authorized_client.get(f"/posts/{dummy_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == dummy_posts[0].id


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("dummy post 1", "dummy content 1", True),
        ("dummy post 2", "dummy content 2", True),
        ("dummy post 3", "dummy content 3", False),
    ],
)
def test_create_post(authorized_client, dummy_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published,
        },
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == dummy_user["id"]


def test_create_post_default_published(authorized_client, dummy_user):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": "test title",
            "content": "test content",
        },
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True  # noqa: E712
    assert created_post.owner_id == dummy_user["id"]


def test_create_post_unauthorized_user(client):
    res = client.post(
        "/posts/",
        json={
            "title": "test title",
            "content": "test content",
        },
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(authorized_client, dummy_posts):
    res = authorized_client.delete(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_forbidden(authorized_client, dummy_posts):
    res = authorized_client.delete(f"/posts/{dummy_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_delete_post_not_exist(authorized_client, dummy_posts):
    res = authorized_client.delete("/posts/999")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post_unauthorized_user(client, dummy_posts):
    res = client.delete(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post(authorized_client, dummy_user, dummy_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": dummy_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{dummy_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.owner_id == dummy_user["id"]


def test_update_post_forbidden(authorized_client, dummy_user2, dummy_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": dummy_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{dummy_posts[3].id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post_not_exist(authorized_client, dummy_posts):
    res = authorized_client.put(
        f"/posts/{999}",
        json={
            "title": "updated title",
            "content": "updated content",
            "id": 999,
        },
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_post_unauthorized_user(client, dummy_posts):
    res = client.put(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
