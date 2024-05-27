from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import HarbourFactory, HarbourLogFactory, ShipFactory


@pytest.mark.django_db
class TestHarbourList:
    """
    Unit tests for /harbours/
    """

    @pytest.mark.parametrize(
        "harbours_count, expected_status_code, test_id",
        [
            (0, status.HTTP_200_OK, "test_happy_path_no_harbours"),
            (5, status.HTTP_200_OK, "test_happy_path_multiple_harbours"),
            (10, status.HTTP_200_OK, "test_happy_path_max_harbours"),
        ],
    )
    def test_harbour_list_various_counts(
        self, harbours_count, expected_status_code, test_id
    ):
        """
        GET /harbours should return 200.
        """
        # Arrange
        HarbourFactory.create_batch(harbours_count)
        client = APIClient()
        url = reverse("harbours")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == expected_status_code
        assert len(response.data) == harbours_count

    @pytest.mark.parametrize(
        "invalid_method, expected_status_code, test_id",
        [
            (
                "put",
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "test_error_put_method_not_allowed",
            ),
            (
                "delete",
                status.HTTP_405_METHOD_NOT_ALLOWED,
                "test_error_delete_method_not_allowed",
            ),
        ],
    )
    def test_harbour_list_invalid_methods(
        self, invalid_method, expected_status_code, test_id
    ):
        """
        PUT and DELETE /harbours should return 405
        """
        # Arrange
        client = APIClient()
        method = {"put": client.put, "delete": client.delete}
        url = reverse("harbours")

        # Act
        response = method[invalid_method](url, {})

        # Assert
        assert response.status_code == expected_status_code

    @pytest.mark.django_db
    def test_create_harbour(self):
        """
        POST /harbours should return 201
        """
        # Arrange
        client = APIClient()
        harbour_data = {
            "name": "Sydney Harbour",
            "max_berth_depth": 18,
            "harbour_master": "Michael Brown",
            "city": "Sydney",
            "country": "Australia",
        }
        url = reverse("harbours")

        # Act
        response = client.post(url, data=harbour_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == harbour_data["name"]


class TestHarbourDetails:
    """
    Unit tests for /harbours/<int:pk>/details/
    """

    @pytest.mark.django_db
    def test_harbour_details_view(self):
        """
        GET /harbours/id/details should return 200
        and contain one ship docked.
        """
        client = APIClient()

        # Arrange
        harbour = HarbourFactory()
        ships = ShipFactory.create_batch(2)
        current_time = datetime.now()
        _ = HarbourLogFactory(
            ship=ships[0],
            harbour=harbour,
            entry_time=current_time - timedelta(days=5),
            exit_time=current_time - timedelta(days=2),
        )
        _ = HarbourLogFactory(
            ship=ships[1],
            harbour=harbour,
            entry_time=current_time - timedelta(days=4),
            exit_time=current_time + timedelta(days=2),
        )
        url = reverse("harbour_details", kwargs={"pk": harbour.id})

        # Act
        response = client.get(url)

        # # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["current_ships"]) == 1

    @pytest.mark.django_db
    def test_harbour_details_view_non_existent_harbour(self):
        """
        GET /harbours/id/details should return 404.
        """
        client = APIClient()

        # Arrange
        url = reverse("harbour_details", kwargs={"pk": 999})

        # Act
        response = client.get(url)

        # # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
