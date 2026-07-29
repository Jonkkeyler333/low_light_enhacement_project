import pytest

@pytest.mark.usefixtures("client")
class TestHealth:
    def test_health_app_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "message": "API is running successfully"}
    
    def test_health_app_check_invalid_endpoint(self, client):
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
        
    def test_model_health_check(self, client):
        response = client.get("/api/enhance/check/")
        assert response.status_code == 200
        assert response.json() == {
            "model_loaded": True,
            "trainable_parameters": 258,
            "eval_mode": True
        }
        
    def test_model_settings_check(self, client):
        response = client.get("/api/enhance/settings/")
        assert response.status_code == 200
        assert response.json() == {
            "image_size_max": 1280,
            "allowed_extensions": ["image/png", "image/jpg", "image/jpeg", "image/tiff", "image/bmp"],
            "max_content_length": 10485760
        }