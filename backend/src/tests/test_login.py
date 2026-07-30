import pytest

@pytest.mark.usefixtures("async_client", "admin_user")
@pytest.mark.anyio
class TestLogin:  
    async def test_admin_login(self, async_client, admin_user):
        response = await async_client.post("/api/auth/login", json = {
            "email": "test@example.com",
            "plain_password": "test_password"
        })
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "Login successful"
        }
        
    async def test_admin_login_invalid_credentials(self, async_client, admin_user):
        response = await async_client.post("/api/auth/login", json = {
            "email": "invalid@example.com",
            "plain_password": "invalid_password"
        })
        print(response.cookies)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Invalid credentials"
        }