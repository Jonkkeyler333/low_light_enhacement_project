import pytest

@pytest.mark.usefixtures("async_client", "admin_user", "normal_user")
@pytest.mark.anyio
class TestLogin:  
    async def test_admin_login(self, async_client, admin_user):
        response = await async_client.post("/api/auth/login", json = {
            "email": "test@example.com",
            "plain_password": "test_password"
        })
        
        assert "access_token" in response.cookies
        assert response.status_code == 200
        assert response.json() == {
            "message": "Login successful"
        }
        
    async def test_admin_login_invalid_credentials(self, async_client, admin_user):
        response = await async_client.post("/api/auth/login", json = {
            "email": "invalid@example.com",
            "plain_password": "invalid_password"
        })
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Invalid credentials"
        }
        assert response.cookies.get("access_token") is None
        
    async def test_logout(self, async_client, admin_user):
        response = await async_client.post("/api/auth/logout")
        assert response.status_code == 204
        assert response.cookies.get("access_token") is None
    
    async def test_user_login(self, async_client, normal_user):
        response = await async_client.post("/api/auth/login", json = {
            "email": "hola@gmail.com",
            "plain_password": "test_password_xd"
        })
        
        assert response.status_code == 200
        assert response.cookies.get("access_token")
        assert response.json() == {
            "message": "Login successful"
        }
        
    async def test_get_me(self, async_client, normal_user):
        await async_client.post("/api/auth/login", json = {
            "email": "hola@gmail.com",
            "plain_password": "test_password_xd"
        })
        response = await async_client.get("/api/auth/me")
        need_fields = ['_id', 'name', 'last_name', 'email', 'is_active', 'role', 'last_login']
        response_fields = list(response.json().keys())
        assert response_fields >= need_fields
        assert response.status_code == 200
    