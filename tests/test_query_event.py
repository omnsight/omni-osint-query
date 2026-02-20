import jwt
from fastapi.testclient import TestClient
from omni_python_library import init_omni_library
from omni_python_library.clients.arangodb import ArangoDBClient
from omni_python_library.dal.osint_data_access_layer import OsintDataAccessLayer
from omni_python_library.dal.query_tools.event_search import search_events
from omni_python_library.models.osint import (
    EventMainData,
    RelationMainData,
)
from omni_python_library.utils.user import UserRole

from omni_osint_query.main import app


class TestEvent:
    client: TestClient
    no_roles_client: TestClient

    @classmethod
    def setup_class(cls):
        init_omni_library()
        # Client with admin roles
        payload = {"sub": "test-user-id-123", "roles": [UserRole.ADMIN]}
        token = jwt.encode(payload, key=None, algorithm="none")
        cls.client = TestClient(app)
        cls.client.headers = {"Authorization": f"Bearer {token}"}

        # Client with no roles
        no_roles_payload = {"sub": "test-user-id-456", "roles": []}
        no_roles_token = jwt.encode(no_roles_payload, key=None, algorithm="none")
        cls.no_roles_client = TestClient(app)
        cls.no_roles_client.headers = {"Authorization": f"Bearer {no_roles_token}"}

    def setUp(self):
        # Clear DB collections before each test
        for col_name in ArangoDBClient()._collections:
            ArangoDBClient()._collections[col_name].truncate()

    def test_execute_query(self):
        event1 = OsintDataAccessLayer().create_event(
            EventMainData(
                title="Test Event 1",
                happened_at=124,
            ),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        event2 = OsintDataAccessLayer().create_event(
            EventMainData(
                title="Test Event 2",
                happened_at=2000,
            ),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        relation = OsintDataAccessLayer().create_relation(
            RelationMainData(from_id=event1.id, to_id=event2.id, name="related_to"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        results = search_events(
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
            date_range=(0, 2500),
        )
        assert len(results) == 3, f"{results}"

        response = self.client.post(
            "/query/events",
            json={
                "date_start": 0,
                "date_end": 1000000000,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["events"]) == 2
        assert {e["_id"] for e in data["events"]} == {event1.id, event2.id}
        assert len(data["relations"]) == 1
        assert data["relations"][0]["_id"] == relation.id

    def test_execute_query_exception(self):
        from unittest.mock import patch

        with patch("omni_osint_query.routers.query_events.search_events") as mock_search:
            mock_search.side_effect = Exception("Test exception")
            response = self.client.post("/query/events", json={})
            assert response.status_code == 500
            assert response.json() == {"detail": "Internal server error"}
