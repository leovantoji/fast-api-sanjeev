from fastapi import status


def test_vote_on_post(authorized_client, dummy_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": dummy_posts[3].id,
            "dir": 1,
        },
    )
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice_on_post(authorized_client, dummy_posts, dummy_vote):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": dummy_posts[3].id,
            "dir": 1,
        },
    )
    assert res.status_code == status.HTTP_409_CONFLICT


def test_vote_not_exist(authorized_client, dummy_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": 999,
            "dir": 1,
        },
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_vote(authorized_client, dummy_posts, dummy_vote):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": dummy_posts[3].id,
            "dir": 0,
        },
    )
    assert res.status_code == status.HTTP_201_CREATED


def test_delete_vote_not_exist(authorized_client, dummy_posts):
    res = authorized_client.post(
        "/vote/",
        json={
            "post_id": dummy_posts[3].id,
            "dir": 0,
        },
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_on_post_unauthorized_user(client, dummy_posts):
    res = client.post(
        "/vote/",
        json={
            "post_id": dummy_posts[3].id,
            "dir": 1,
        },
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
