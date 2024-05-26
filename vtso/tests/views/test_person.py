import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import CompanyFactory, PersonFactory


class TestPersonList:

    @pytest.mark.django_db
    def test_person_list(self):
        # Arrange
        company = CompanyFactory(name="Stark Industries")
        _ = PersonFactory(
            **{
                "name": "John",
                "email": "john@example.com",
                "phone": "0412345678",
                "company": company,
            }
        )
        _ = PersonFactory(
            **{
                "name": "Alice",
                "email": "alice@example.com",
                "phone": "0398765432",
                "company": company,
            }
        )
        client = APIClient()
        url = reverse("persons")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # @pytest.mark.parametrize(
        # "persons_data, expected_status_code, test_id",
        # [
        #     ([{'first_name': 'John', 'email': 'john@example.com', 'phone': '0412345678', 'company': CompanyFactory()}], status.HTTP_200_OK, 'test_001'),
        #     ([{'first_name': 'Alice', 'email': 'alice@example.com', 'phone': '0398765432', 'company': CompanyFactory()}], status.HTTP_200_OK, 'test_002'),
        #     ([], status.HTTP_200_OK, 'test_003')
        # ]
        # )

    @pytest.mark.django_db
    def test_create_person(self):
        """
        POST /persons should return 201
        """
        # Arrange
        client = APIClient()
        company = CompanyFactory(name="Stark Industries")
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
            "company": company.id,
        }
        url = reverse("persons")

        # Act
        response = client.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == person_data["name"]

    @pytest.mark.django_db
    def test_create_person_company_does_not_exist(self):
        """
        POST /persons should return 400 as the View will not
        allow the creation of a Person employed by a non-existent company
        """
        # Arrange
        client = APIClient()
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
            # there is no Company with id 10 in the database
            "company": 10,
        }
        url = reverse("persons")

        # Act
        response = client.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_person_without_company(self):
        """
        POST /persons should return 400 as the View will not
        allow the creation of a Person without a Company
        """
        # Arrange
        client = APIClient()
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
        }
        url = reverse("persons")

        # Act
        response = client.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
