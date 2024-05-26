import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import HarbourFactory


@pytest.mark.django_db
class TestHarbourList:
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
