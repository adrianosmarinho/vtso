import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import CompanyFactory, ShipFactory


class TestShipList:

    @pytest.mark.django_db
    def test_ship_list(self):
        # Arrange
        company = CompanyFactory(name="Hammer Industries")
        _ = ShipFactory(
            **{
                "name": "Ocean Pearl",
                "company": company,
            }
        )
        _ = ShipFactory(
            **{
                "name": "Titanic",
                "company": company,
            }
        )
        client = APIClient()
        url = reverse("ships")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_create_ship(self):
        """
        POST /ships should return 201
        """
        # Arrange
        client = APIClient()
        company = CompanyFactory(name="Hammer Industries")
        ship_data = {
            "company": company.id,
            "name": "Sea Master",
            "tonnage": 4000,
            "max_load_draft": 9,
            "dry_draft": 4,
            "flag": "Germany",
            "beam": 18,
            "length": 90,
            "year_built": "2012",
            "type": "tanker",
        }
        url = reverse("ships")

        # Act
        response = client.post(url, data=ship_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == ship_data["name"]

    @pytest.mark.django_db
    def test_create_ship_company_does_not_exist(self):
        """
        POST /ships should return return 400 as the View will not
        allow the creation of a Ship operated by a non-existent company
        """
        # Arrange
        client = APIClient()
        ship_data = {
            # there is no Company with id 10 in the database
            "company": 10,
            "name": "Sea Master",
            "tonnage": 4000,
            "max_load_draft": 9,
            "dry_draft": 4,
            "flag": "Germany",
            "beam": 18,
            "length": 90,
            "year_built": "2012",
            "type": "tanker",
        }
        url = reverse("ships")

        # Act
        response = client.post(url, data=ship_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_ship_without_company(self):
        """
        POST /ships should return return 400 as the View will not
        allow the creation of a Ship without a Company
        """
        # Arrange
        client = APIClient()
        ship_data = {
            "name": "Sea Master",
            "tonnage": 4000,
            "max_load_draft": 9,
            "dry_draft": 4,
            "flag": "Germany",
            "beam": 18,
            "length": 90,
            "year_built": "2012",
            "type": "tanker",
        }
        url = reverse("ships")

        # Act
        response = client.post(url, data=ship_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # @pytest.mark.django_db
    # def test_create_person_without_company(self):
    #     """
    #     POST /persons should return 400 as the View will not
    #     allow the creation of a Person without a Company
    #     """
    #     # Arrange
    #     client = APIClient()
    #     person_data = {
    #         "name": "John",
    #         "email": "john@example.com",
    #         "phone": "0412345678",
    #     }
    #     url = reverse("persons")

    #     # Act
    #     response = client.post(url, data=person_data)

    #     # Assert
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
