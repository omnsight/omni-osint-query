from fastapi.testclient import TestClient
from omni_python_library import init_omni_library
from omni_python_library.clients.arangodb import ArangoDBClient

from omni_osint_query.main import app


class TestHealth:
    client: TestClient

    @classmethod
    def setup_class(cls):
        init_omni_library()
        cls.client = TestClient(app)

    def setUp(self):
        # Clear DB collections before each test
        for col_name in ArangoDBClient()._collections:
            ArangoDBClient()._collections[col_name].truncate()

    def test_health_check(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
