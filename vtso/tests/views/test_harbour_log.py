import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import (
    CompanyFactory,
    HarbourFactory,
    HarbourLogFactory,
    ShipFactory,
)


@pytest.mark.django_db
class TestHarbourLogList:

    @pytest.mark.django_db
    def test_harbourlog_list(self):
        # Arrange

        company = CompanyFactory(name="Stark Industries")
        ship = ShipFactory(name="USS Quinjet", company=company)
        harbour = HarbourFactory(
            name="Sydney Harbour", city="Sydney", country="Australia"
        )
        _ = HarbourLogFactory(
            **{
                "ship": ship,
                "harbour": harbour,
                "entry_time": "2023-05-26T10:15:30Z",
                "exit_time": "2023-05-26T14:30:00Z",
            }
        )
        _ = HarbourLogFactory(
            **{
                "ship": ship,
                "harbour": harbour,
                "entry_time": "2023-05-27T08:00:00Z",
                "exit_time": "2023-05-27T12:45:00Z",
            }
        )
        client = APIClient()
        url = reverse("harbourlogs")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_create_harbourlog(self):
        """
        POST /harbourlog should return 201
        """
        # Arrange
        client = APIClient()
        company = CompanyFactory(name="Stark Industries")
        ship = ShipFactory(name="USS Quinjet", company=company)
        harbour = HarbourFactory(
            name="Sydney Harbour", city="Sydney", country="Australia"
        )
        harbourlog_data = {
            "ship": ship.id,
            "harbour": harbour.id,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("harbourlogs")

        # Act
        response = client.post(url, data=harbourlog_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["ship"] == ship.id

    @pytest.mark.django_db
    def test_create_habourlog_without_ship(self):
        """
        POST /harbourlogs should return 400 as the View will not
        allow the creation of a HarbourLog without a Ship
        """
        # Arrange
        client = APIClient()
        harbourlog_data = {
            "harbour": 201,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("harbourlogs")

        # Act
        response = client.post(url, data=harbourlog_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_habourlog_without_harbour(self):
        """
        POST /harbourlogs should return 400 as the View will not
        allow the creation of a HarbourLog without a Harbour
        """
        # Arrange
        client = APIClient()
        harbourlog_data = {
            "ship": 101,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("harbourlogs")

        # Act
        response = client.post(url, data=harbourlog_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
