# apps/deletion_service.py

def delete_user(user_id: str, actor: str = "system") -> dict:
    print(f"Deleting user {user_id} by {actor}")
    return {"success": True, "message": f"User {user_id} deleted by {actor}"}
