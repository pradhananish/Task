# test_delete.py
import uuid
import pytest
from httpx import AsyncClient
from Task_1.main import app
from Task_1.apps.db import SessionLocal
from Task_1.apps.models import User, UserProfile, UserActivity, Upload
from Task_1.apps.redis_client import redis_client

@pytest.mark.asyncio
async def test_delete_user_and_artifacts():
    db = SessionLocal()
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"test+{user_id}@ex.com", name="Tester")
    db.add(user)
    db.add(UserProfile(user_id=user_id, bio="bio"))
    db.add(UserActivity(user_id=user_id, event={"act": "login"}))
    db.add(Upload(user_id=user_id, s3_key=f"fake/{user_id}.jpg"))
    db.commit()

    # put session in redis
    sid = str(uuid.uuid4())
    redis_client.set(f"session:{sid}", "{}", ex=3600)
    redis_client.sadd(f"user_sessions:{user_id}", sid)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.delete(f"/api/users/{user_id}", headers={"X-Actor": "test"})
    assert res.status_code == 200
    assert res.json()["success"]

    # verify DB cleanup
    assert db.query(User).filter_by(id=user_id).first() is None
    assert db.query(UserProfile).filter_by(user_id=user_id).count() == 0
    assert db.query(UserActivity).filter_by(user_id=user_id).count() == 0
    assert db.query(Upload).filter_by(user_id=user_id).count() == 0

    # verify Redis cleanup
    assert redis_client.smembers(f"user_sessions:{user_id}") == set()
