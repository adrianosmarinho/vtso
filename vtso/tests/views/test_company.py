import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from vtso.models import User
from vtso.tests.factories import CompanyFactory


@pytest.mark.django_db
class TestCompanyList:
    """
    Unit tests for vtso/companies
    """

    def test_list_companies_get_not_authenticated(self):
        """
        GET /companies should return 401 because this request is not authenticated.
        """
        # Arrange
        client = APIClient()
        CompanyFactory(name="")
        url = reverse("companies")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_list_companies_empty_name_get(self):
        """
        GET /companies should return 200 because our Model
        and View allow for the creation of a Company with empty name
        """
        # Arrange
        user = User.objects.create(username="test_user")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.force_authenticate(user=user, token=token)
        CompanyFactory(name="")
        url = reverse("companies")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_list_companies_happy_path_get(self):
        # Arrange
        client = APIClient()
        user = User.objects.create(username="test_user")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.force_authenticate(user=user, token=token)
        CompanyFactory(name="Company A")
        CompanyFactory(name="Company B")
        expected_response_length = 2
        url = reverse("companies")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_response_length

    def test_list_companies_happy_path_post(self):
        # Arrange
        client = APIClient()
        user = User.objects.create(username="test_user")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.force_authenticate(user=user, token=token)
        name = "Company C"
        url = reverse("companies")

        # Act
        response = client.post(url, data={"name": name})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == name
