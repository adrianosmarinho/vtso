import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from vtso.models import User
from vtso.tests.factories import CompanyFactory, PersonFactory


class TestPersonList:
    """
    Unit tests for /vtso/persons/.
    """

    @pytest.fixture
    def api_client_authenticated(self):
        user = User.objects.create(username="test_user")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.force_authenticate(user=user, token=token)
        return client

    @pytest.mark.django_db
    def test_person_list(self, api_client_authenticated):
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
        url = reverse("persons")

        # Act
        response = api_client_authenticated.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_create_person(self, api_client_authenticated):
        """
        POST /persons should return 201
        """
        # Arrange
        company = CompanyFactory(name="Stark Industries")
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
            "company": company.id,
        }
        url = reverse("persons")

        # Act
        response = api_client_authenticated.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == person_data["name"]

    @pytest.mark.django_db
    def test_create_person_unauthenticated(self):
        """
        POST /persons/ should return 401.
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
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    @pytest.mark.django_db
    def test_create_person_company_does_not_exist(self, api_client_authenticated):
        """
        POST /persons/ should return 400 as the View will not
        allow the creation of a Person employed by a non-existent company
        """
        # Arrange
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
            # there is no Company with id 10 in the database
            "company": 10,
        }
        url = reverse("persons")

        # Act
        response = api_client_authenticated.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_person_without_company(self, api_client_authenticated):
        """
        POST /persons/ should return 400 as the View will not
        allow the creation of a Person without a Company
        """
        # Arrange
        person_data = {
            "name": "John",
            "email": "john@example.com",
            "phone": "0412345678",
        }
        url = reverse("persons")

        # Act
        response = api_client_authenticated.post(url, data=person_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
