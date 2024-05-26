# from django.test import TestCase

import pytest
from django.core.exceptions import ValidationError

from vtso.models import Harbour


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
