from datetime import timedelta

import pytest
from django.utils import timezone

from vtso.models import Company, Harbour, HarbourLog, Ship


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
