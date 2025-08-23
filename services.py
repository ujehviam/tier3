import models

def register_user(username, password):
    try:
        models.add_user(username, password)
        return True, "User registered successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def authenticate_user(username, password):
    user = models.get_user(username, password)
    return user is not None

def get_all_users():
    return models.list_user_table()