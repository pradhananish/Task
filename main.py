# main.py
from fastapi import FastAPI, Header
from apps.deletion_service import delete_user as delete_user_and_artifacts


app = FastAPI()

@app.delete("/api/users/{user_id}")
def delete_user(user_id: str, x_actor: str = Header("system")):
    result = delete_user_and_artifacts(user_id, actor=x_actor)
    if not result["success"]:
        return {"success": False, "message": "User not found"}
    return result
