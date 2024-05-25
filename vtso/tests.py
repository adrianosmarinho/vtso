# from django.test import TestCase
from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from vtso.models import Company, Harbour, HarbourLog, Person, Ship


class TestCompany:
    """
    Unit tests for the Company model.
    """

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "company_name, expected_name",
        [
            ("Tech Innovations", "Tech Innovations"),  # Valid name
            ("", ""),  # Empty name
            (None, None),  # name is None
            (" " * 256, " " * 256),  # name is 256 whitespaces
            ("A" * 256, "A" * 256),  # names 256 "A"
        ],
    )
    def test_company_name_variations(self, company_name, expected_name):
        # Arrange
        company = Company(name=company_name)

        # Act
        company.full_clean()  # This will raise ValidationError if any fields are invalid
        company.save()
        retrieved_company = Company.objects.get(id=company.id)

        # Assert
        assert retrieved_company.name == expected_name

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "company_name",
        [
            ("A" * 257),  # error case: name too long
        ],
    )
    def test_company_name_errors(self, company_name):
        # Arrange
        company = Company(name=company_name)

        # Act & Assert
        with pytest.raises(ValidationError):
            # This should raise an error due to max_length constraint
            company.full_clean()


class TestPerson:
    """
    Unit tests for the Person model.
    """

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "company_id, name, email, phone, expected_exception",
        [
            # Test ID: 1 - All fields are valid
            (1, "John Doe", "john.doe@example.com", "+61412345678", None),
            # Test ID: 2 - Name is None
            (1, None, "jane.doe@example.com", "+61498765432", None),
            # Test ID: 3 - Email is None
            (1, "Jane Doe", None, "+61456789012", None),
            # Test ID: 4 - Phone is None
            (1, "John Smith", "john.smith@example.com", None, None),
            # Test ID: 5 - Name is blank
            (1, "", "blank.name@example.com", "+61432109876", None),
            # Test ID: 6 - Email is blank
            (1, "Blank Email", "", "+61455556666", None),
            # Test ID: 7 - Phone is blank
            (1, "Blank Phone", "blank.phone@example.com", "", None),
        ],
    )
    def test_person_creation(self, company_id, name, email, phone, expected_exception):
        # Arrange
        company = Company.objects.create(id=company_id, name="Test Company")

        # Act
        if expected_exception:
            with pytest.raises(expected_exception):
                Person.objects.create(
                    company=company, name=name, email=email, phone=phone
                )
        else:
            person = Person.objects.create(
                company=company, name=name, email=email, phone=phone
            )

        # Assert
        if not expected_exception:
            assert person.name == name
            assert person.email == email
            assert person.phone == phone
            assert person.company == company


class TestHarbour:
    """
    Unit tests for the Harbour model.
    """

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "name, max_berth_depth, harbour_master, city, country",
        [
            # Test ID: 1 - All fields provided correctly
            ("Port Royale", 30, "John Doe", "Kingston", "Jamaica"),
            # Test ID: 2 - Optional fields left blank
            ("Port Royale", 30, "", "", ""),
            # Test ID: 3 - Maximum length edge case for strings
            ("A" * 256, 30, "B" * 256, "C" * 256, "D" * 256),
            # Test ID: 6 - Null values for required fields
            (None, 30, "John Doe", "Kingston", "Jamaica"),
        ],
        ids=[
            "happy_path_all_fields_provided",
            "happy_path_optional_fields_blank",
            "edge_case_max_length_strings",
            "error_case_null_required_fields",
        ],
    )
    def test_valid_harbour_creation(
        self, name, max_berth_depth, harbour_master, city, country
    ):
        """
        TODO: adjust to test to retrieve object

        Args:
            name (_type_): _description_
            max_berth_depth (_type_): _description_
            harbour_master (_type_): _description_
            city (_type_): _description_
            country (_type_): _description_
        """
        # Act
        harbour = Harbour(
            name=name,
            max_berth_depth=max_berth_depth,
            harbour_master=harbour_master,
            city=city,
            country=country,
        )
        harbour.full_clean()  # Validate model fields

        # Assert
        assert harbour.name == name
        assert harbour.max_berth_depth == max_berth_depth
        assert harbour.harbour_master == harbour_master
        assert harbour.city == city
        assert harbour.country == country
        # Ensure not saved to db
        assert not Harbour.objects.filter(name=name).exists()

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "name, max_berth_depth, harbour_master, city, country",
        [
            # Test ID: 4 - Negative depth value
            ("Port Royale", -1, "John Doe", "Kingston", "Jamaica"),
            # Test ID: 5 - Exceeding max length for strings
            ("A" * 257, 30, "B" * 257, "C" * 257, "D" * 257),
        ],
        ids=[
            "error_case_negative_depth",
            "error_case_exceeding_max_length",
        ],
    )
    def test_invalid_harbour_creation(
        self, name, max_berth_depth, harbour_master, city, country
    ):
        # Act & Assert
        with pytest.raises(ValidationError):
            harbour = Harbour(
                name=name,
                max_berth_depth=max_berth_depth,
                harbour_master=harbour_master,
                city=city,
                country=country,
            )
            harbour.full_clean()  # This will raise the ValidationError for invalid data


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


class TestHarbourLog:
    # TODO: review this test to check if we should use datetime.now()
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "ship_name, harbour_name, entry_time, exit_time, test_id",
        [
            (
                "Titanic",
                "Port Royal",
                timezone.now(),
                timezone.now() + timedelta(hours=1),
                "HP-1",
            ),
            (
                "Queen Mary",
                "Cape Town Harbour",
                timezone.now(),
                timezone.now() + timedelta(days=1),
                "HP-2",
            ),
            ("Endeavour", "Sydney Harbour", timezone.now(), timezone.now(), "EC-1"),
            ("Yamato", "Tokyo Bay", None, None, "EC-2"),
            (
                "Santa Maria",
                "Marina Bay",
                timezone.now(),
                timezone.now() + timedelta(hours=1),
                "ER-1",
            ),
        ],
    )
    def test_harbour_log_creation(
        self, ship_name, harbour_name, entry_time, exit_time, test_id
    ):
        # Arrange
        company = Company.objects.create(name="Test Company")
        harbour = Harbour.objects.create(name=harbour_name)
        ship = Ship.objects.create(name=ship_name, company=company)

        # Act
        harbour_log = HarbourLog.objects.create(
            ship=ship, harbour=harbour, entry_time=entry_time, exit_time=exit_time
        )

        # Assert
        assert harbour_log.ship == ship
        assert harbour_log.harbour == harbour
        assert harbour_log.entry_time == entry_time
        assert harbour_log.exit_time == exit_time
        assert HarbourLog.objects.count() == 1
