import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from vtso.tests.factories import CompanyFactory, ShipFactory, VisitFactory


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


class TestShipDetail:
    @pytest.mark.django_db
    def test_ship_detail_view(self):
        """
        GET /ships/id should return 200 if the Ship with the
        given id exists in the database.
        """
        # Arrange
        company = CompanyFactory(name="Roxxon")
        ship_data = {
            "company": company,
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
        ship = ShipFactory(**ship_data)
        client = APIClient()
        url = reverse("ship_detail", kwargs={"pk": ship.id})

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == ship.id

    @pytest.mark.django_db
    def test_ship_detail_invalid_id(self):
        """
        GET /ships/id should return 404 if the Ship with the
        given id does not exist in the database.
        """
        # Arrange
        client = APIClient()
        url = reverse("ship_detail", kwargs={"pk": 999})

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_ship_update(self):
        # Arrange
        company = CompanyFactory(name="Roxxon")
        ship_data = {
            "company": company,
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
        ship = ShipFactory(**ship_data)
        client = APIClient()
        url = reverse("ship_detail", kwargs={"pk": ship.id})
        data = {"name": "Titanic"}

        # Act
        response = client.patch(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]


class TestShipVisits:

    @pytest.mark.django_db
    def test_ship_visits_multiple_visits(self):
        """
        GET /ships/<int:pk>/visits should return 200 with
        2 Harbours listed.
        """

        client = APIClient()

        ship = ShipFactory()
        _ = VisitFactory.create_batch(2, ship=ship)
        url = reverse("ship_visits", kwargs={"pk": ship.pk})

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_ship_visits_no_visits(self):
        """
        GET /ships/<int:pk>/visits should return 200 with
        no data if the Ship did not visit any Harbous.
        """
        client = APIClient()

        ship_no_visits = ShipFactory()
        url_no_visits = reverse("ship_visits", kwargs={"pk": ship_no_visits.pk})

        response_no_visits = client.get(url_no_visits)

        assert response_no_visits.status_code == status.HTTP_200_OK
        assert len(response_no_visits.data) == 0

    @pytest.mark.django_db
    def test_ship_visits_error_cases(self):
        """
        GET /ships/<int:pk>/visits should return 200 with
        no data if the Ship did not visit any Harbous.
        """
        client = APIClient()

        # Error case: Ship does not exist
        url_ship_not_found = reverse("ship_visits", kwargs={"pk": 999})

        response = client.get(url_ship_not_found)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Ship not found" in response.data["detail"]
