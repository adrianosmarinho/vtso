# from django.test import TestCase
import pytest
from django.core.exceptions import ValidationError

from vtso.models import Company, Person


# Create your tests here.
def test_example():
    assert False


class TestCompany:
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
