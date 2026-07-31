import pytest

@pytest.mark.usefixtures("async_client", "normal_user", "valid_image_bytes")
@pytest.mark.anyio
class TestEnhance:
    async def test_enhance_image(self, authenticated_client, normal_user, valid_image_bytes):
        response = await authenticated_client.post(
            "/api/enhance/",
            files = {"image": ("79.png", valid_image_bytes, "image/png")}
        )
        assert response.status_code == 200
        assert response.headers['content-type'] == "image/png"
        assert float(response.headers['content-length']) > 0.0
        
    async def test_enhance_image_invalid_file_type(self, authenticated_client, normal_user, invalid_file):
        response = await authenticated_client.post(
            "/api/enhance/",
            files = {"image": ("hola.pdf", invalid_file, "application/pdf")}
        )
        assert response.status_code == 400
        assert response.json() == {"detail":"File type do not support"}