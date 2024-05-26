from datetime import datetime
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from vtso.models import Company, Ship
from vtso.tests.factories import ShipFactory


@pytest.mark.django_db
class TestShip:
    @pytest.mark.parametrize(
        "company_id, name, tonnage, max_load_draft, dry_draft, flag, beam, length, year_built, ship_type, expected_exception",
        [
            # Test ID: 1 - Error case, year_built invalid (non-numeric)
            (
                1,
                "Error Ship",
                5000,
                500,
                300,
                "Italy",
                30,
                100,
                "abcd",
                Ship.ShipType.TANKER,
                ValidationError,
            ),
            # Test ID: 2 - Error case, year_built invalid (out of range)
            (
                1,
                "Error Ship",
                5000,
                500,
                300,
                "Italy",
                30,
                100,
                "10000",
                Ship.ShipType.TANKER,
                ValidationError,
            ),
            # Test ID: 3 - Error case, negative tonnage
            (
                1,
                "Negative Tonnage",
                -100,
                500,
                300,
                "Japan",
                30,
                100,
                "1980",
                Ship.ShipType.BULK_CARRIER,
                ValidationError,
            ),
        ],
    )
    def test_ship_model_with_exception(
        self,
        company_id,
        name,
        tonnage,
        max_load_draft,
        dry_draft,
        flag,
        beam,
        length,
        year_built,
        ship_type,
        expected_exception,
    ):
        company = Company.objects.create(id=company_id, name="Test Company")

        with pytest.raises(expected_exception):
            ship = Ship(
                company=company,
                name=name,
                tonnage=tonnage,
                max_load_draft=max_load_draft,
                dry_draft=dry_draft,
                flag=flag,
                beam=beam,
                length=length,
                year_built=year_built,
                type=ship_type,
            )
            ship.full_clean()
            ship.save()

    @pytest.mark.parametrize(
        "company_id, name, tonnage, max_load_draft, dry_draft, flag, beam, length, year_built, ship_type, expected_exception",
        [
            # Test ID: 4 - Happy path, all fields provided correctly
            (
                1,
                "Titanic",
                46000,
                3000,
                2000,
                "UK",
                92,
                269,
                "1912",
                Ship.ShipType.CRUISE_SHIP,
                None,
            ),
            # Test ID: 5 - Happy path, minimal valid input (only required fields)
            (1, None, None, None, None, None, None, None, None, None, None),
            # Test ID: 6 - Edge case, maximum string length for name and flag
            (
                1,
                "A" * 256,
                10000,
                1000,
                500,
                "A" * 256,
                50,
                150,
                "2000",
                Ship.ShipType.BULK_CARRIER,
                None,
            ),
            # Test ID: 7 - Edge case, year_built at boundary value (earliest)
            (
                1,
                "Old Ship",
                5000,
                500,
                300,
                "Greece",
                30,
                100,
                "0000",
                Ship.ShipType.FISHING,
                None,
            ),
            # Test ID: 8 - Edge case, year_built at boundary value (latest)
            (
                1,
                "Future Ship",
                70000,
                4000,
                2500,
                "USA",
                100,
                350,
                "9999",
                Ship.ShipType.SUBMARINE,
                None,
            ),
        ],
    )
    def test_ship_model(
        self,
        company_id,
        name,
        tonnage,
        max_load_draft,
        dry_draft,
        flag,
        beam,
        length,
        year_built,
        ship_type,
        expected_exception,
    ):
        company = Company.objects.create(id=company_id, name="Test Company")

        ship = Ship.objects.create(
            company=company,
            name=name,
            tonnage=tonnage,
            max_load_draft=max_load_draft,
            dry_draft=dry_draft,
            flag=flag,
            beam=beam,
            length=length,
            year_built=year_built,
            type=ship_type,
        )

        assert ship.company == company
        assert ship.name == name
        assert ship.tonnage == tonnage
        assert ship.max_load_draft == max_load_draft
        assert ship.dry_draft == dry_draft
        assert ship.flag == flag
        assert ship.beam == beam
        assert ship.length == length
        assert ship.year_built == year_built
        assert ship.type == ship_type
        assert Ship.objects.count() == 1


@pytest.mark.django_db
class TestShipAgeProperty:
    """
    Unit tests for the age property of a Ship.
    """

    @pytest.mark.parametrize(
        "year_built, expected_age, test_id",
        [
            ("2000", 23, "happy_path_2000"),
            ("1990", 33, "happy_path_1990"),
            ("1950", 73, "happy_path_1950"),
            ("2023", 0, "edge_case_current_year"),
            ("2024", -1, "edge_case_future_year"),
            ("", None, "edge_case_blank_year"),
            (None, None, "edge_case_null_year"),
        ],
    )
    def test_ship_age_property(self, year_built, expected_age, test_id):
        # Arrange
        ship = ShipFactory(year_built=year_built)

        # Act
        with patch("vtso.models.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1)
            age = ship.age

        # Assert
        assert (
            age == expected_age
        ), f"Test ID {test_id}: Expected age {expected_age}, got {age}"

    @pytest.mark.parametrize(
        "year_built, test_id",
        [
            ("not_a_year", "error_case_non_integer_year"),
        ],
    )
    def test_ship_age_property_with_invalid_input(self, year_built, test_id):
        # Arrange
        ship = ShipFactory.build(year_built=year_built)

        # Act and Assert
        with pytest.raises(ValidationError), patch(
            "datetime.datetime"
        ) as mock_datetime:
            ship.full_clean()
            mock_datetime.now.return_value = datetime(2023, 1, 1)
            _ = ship.age
            pytest.fail(
                f"Test ID {test_id}: Expected ValidationError for year_built={year_built}"
            )
