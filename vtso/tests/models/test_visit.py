from datetime import timedelta

import pytest
from django.utils import timezone

from vtso.models import Company, Harbour, Ship, Visit


class TestVisit:
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
        visit = Visit.objects.create(
            ship=ship, harbour=harbour, entry_time=entry_time, exit_time=exit_time
        )

        # Assert
        assert visit.ship == ship
        assert visit.harbour == harbour
        assert visit.entry_time == entry_time
        assert visit.exit_time == exit_time
        assert Visit.objects.count() == 1
