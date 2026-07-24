from app.models.user import User

class UserRepository:
    async def get_user_by_email(self, email: str) -> User | None:
        user = await User.find_one(User.email == email)
        return user
    
    async def get_user_by_id(self, user_id: str) -> User | None:
        user = await User.get(user_id)
        return user
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = await User.find_all().skip(skip).limit(limit).to_list()
        return users
    
    async def create_user(self, user: User) -> User:
        await user.create()
        return user
    
    async def update_user(self, user_id: str, user_data: dict) -> User | None:
        user = await User.get(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            await user.save()
            return user
        return None
    
    async def delete_user(self, user_id: str) -> bool:
        user = await User.get(user_id)
        if user:
            user.is_active = False
            await user.save()
            return True
        return False