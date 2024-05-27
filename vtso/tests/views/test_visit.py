import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import (
    CompanyFactory,
    HarbourFactory,
    ShipFactory,
    VisitFactory,
)


@pytest.mark.django_db
class TestVisitList:

    @pytest.mark.django_db
    def test_visit_list(self):
        # Arrange

        company = CompanyFactory(name="Stark Industries")
        ship = ShipFactory(name="USS Quinjet", company=company)
        harbour = HarbourFactory(
            name="Sydney Harbour", city="Sydney", country="Australia"
        )
        _ = VisitFactory(
            **{
                "ship": ship,
                "harbour": harbour,
                "entry_time": "2023-05-26T10:15:30Z",
                "exit_time": "2023-05-26T14:30:00Z",
            }
        )
        _ = VisitFactory(
            **{
                "ship": ship,
                "harbour": harbour,
                "entry_time": "2023-05-27T08:00:00Z",
                "exit_time": "2023-05-27T12:45:00Z",
            }
        )
        client = APIClient()
        url = reverse("visits")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_create_visit(self):
        """
        POST /visit should return 201
        """
        # Arrange
        client = APIClient()
        company = CompanyFactory(name="Stark Industries")
        ship = ShipFactory(name="USS Quinjet", company=company)
        harbour = HarbourFactory(
            name="Sydney Harbour", city="Sydney", country="Australia"
        )
        visit_data = {
            "ship": ship.id,
            "harbour": harbour.id,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("visits")

        # Act
        response = client.post(url, data=visit_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["ship"] == ship.id

    @pytest.mark.django_db
    def test_create_habourlog_without_ship(self):
        """
        POST /visits should return 400 as the View will not
        allow the creation of a Visit without a Ship
        """
        # Arrange
        client = APIClient()
        visit_data = {
            "harbour": 201,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("visits")

        # Act
        response = client.post(url, data=visit_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_habourlog_without_harbour(self):
        """
        POST /visits should return 400 as the View will not
        allow the creation of a Visit without a Harbour
        """
        # Arrange
        client = APIClient()
        visit_data = {
            "ship": 101,
            "entry_time": "2023-05-26T10:15:30Z",
            "exit_time": "2023-05-26T14:30:00Z",
        }
        url = reverse("visits")

        # Act
        response = client.post(url, data=visit_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
