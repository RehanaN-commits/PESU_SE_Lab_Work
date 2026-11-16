
from visa_application import visa_fee, documents_complete, application_status
import pytest


# VISA FEE TESTS

def test_invalid_visa():
    with pytest.raises(ValueError):
        visa_fee("work", 2, "normal", "B")


def test_negative_entries():
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_non_student():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_group_b():
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_group_a_student():
    assert visa_fee("student", 3, "normal", "A") == 40


def test_no_extra_entries():
    assert visa_fee("business", 3, "normal", "B") == 0


def test_normal_speed():
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_express_speed():
    assert visa_fee("tourist", 2, "express", "B") == 100


def test_normal_more_than_five_extra():
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_express_more_than_five_extra():
    assert visa_fee("tourist", 7, "express", "B") == 780


# DOCUMENT TESTS

def test_renewal_true():
    assert documents_complete(1, 0, True) is True


def test_renewal_false():
    assert documents_complete(3, 2, False) is True


def test_renewal_without_forms():
    assert documents_complete(0, 2, True) is False


def test_insufficient_photos():
    assert documents_complete(3, 1, False) is False


def test_sufficient_photos_but_insufficient_forms():
    assert documents_complete(2, 2, False) is False


# APPLICATION STATUS TESTS

def test_express_processing():
    assert application_status(10, True, False) == "open"


def test_normal_processing():
    assert application_status(30, False, False) == "open"


def test_peak_season():
    assert application_status(45, False, True) == "open"


def test_not_peak_season():
    assert application_status(30, False, False) == "open"


def test_open_status():
    assert application_status(30, False, False) == "open"


def test_closing_status():
    assert application_status(20, False, False) == "closing"


def test_closed_status():
    assert application_status(10, False, False) == "closed"


def test_express_peak_season():
    assert application_status(25, True, True) == "open"
