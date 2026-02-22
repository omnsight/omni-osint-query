import jwt
from fastapi.testclient import TestClient
from omni_python_library import init_omni_library
from omni_python_library.clients.arangodb import ArangoDBClient
from omni_python_library.dal.osint_data_access_layer import OsintDataAccessLayer
from omni_python_library.models.osint import (
    EventMainData,
    OrganizationMainData,
    PersonMainData,
    RelationMainData,
    SourceMainData,
    WebsiteMainData,
)
from omni_python_library.utils.config import UserRole

from omni_osint_query.main import app


class TestNeighbors:
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

    def test_get_neighbors(self):
        dal = OsintDataAccessLayer()
        person = dal.create_person(
            PersonMainData(first_name="John", last_name="Doe"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        event = dal.create_event(EventMainData(title="Test Event"), owner="test-user-id-123", roles=[UserRole.ADMIN])
        org = dal.create_organization(
            OrganizationMainData(name="Test Org"), owner="test-user-id-123", roles=[UserRole.ADMIN]
        )
        source = dal.create_source(SourceMainData(name="Test Source"), owner="test-user-id-123", roles=[UserRole.ADMIN])
        website = dal.create_website(
            WebsiteMainData(url="http://test.com"), owner="test-user-id-123", roles=[UserRole.ADMIN]
        )

        dal.create_relation(
            RelationMainData(from_id=event.id, to_id=person.id, name="participant"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        dal.create_relation(
            RelationMainData(from_id=event.id, to_id=org.id, name="location"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        dal.create_relation(
            RelationMainData(from_id=event.id, to_id=source.id, name="mentioned_in"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )
        dal.create_relation(
            RelationMainData(from_id=event.id, to_id=website.id, name="mentioned_in"),
            owner="test-user-id-123",
            roles=[UserRole.ADMIN],
        )

        response = self.client.post("/query/neighbors", json={"entity_id": event.id})

        assert response.status_code == 200
        data = response.json()

        assert len(data["persons"]) == 1, f"{data}"
        assert data["persons"][0]["_id"] == person.id
        assert len(data["organizations"]) == 1
        assert data["organizations"][0]["_id"] == org.id
        assert len(data["sources"]) == 1
        assert data["sources"][0]["_id"] == source.id
        assert len(data["websites"]) == 1
        assert data["websites"][0]["_id"] == website.id
        assert len(data["relations"]) == 4

    def test_get_neighbors_exception(self):
        from unittest.mock import patch

        with patch("omni_osint_query.routers.query_neighbors.search_entity_neighborhood") as mock_search:
            mock_search.side_effect = Exception("Test exception")
            response = self.client.post("/query/neighbors", json={"entity_id": "any_id"})
            assert response.status_code == 500
            assert response.json() == {"detail": "Internal server error"}
