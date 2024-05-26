import pytest
from django.core.exceptions import ValidationError

from vtso.models import Company


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
