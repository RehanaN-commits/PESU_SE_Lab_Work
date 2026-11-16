
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- VISA FEE TESTS ----------------

def test_unknown_visa_type():
    with pytest.raises(ValueError):
        visa_fee("work", 2, "normal", "B")


def test_negative_entries():
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_extra_included_entry():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_student_group_a_no_extra_entry():
    assert visa_fee("student", 3, "normal", "A") == 40


def test_normal_processing_fee():
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_processing_fee():
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_more_than_five_extra_entries_normal():
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_more_than_five_extra_entries_express():
    assert visa_fee("tourist", 7, "express", "B") == 780


# ---------------- DOCUMENT TESTS ----------------

def test_renewal_with_one_form():
    assert documents_complete(1, 0, True) is True


def test_renewal_without_forms():
    assert documents_complete(0, 5, True) is False


def test_insufficient_photos():
    assert documents_complete(3, 1, False) is False


def test_insufficient_forms():
    assert documents_complete(2, 2, False) is False


def test_complete_documents():
    assert documents_complete(3, 2, False) is True


# ---------------- APPLICATION STATUS TESTS ----------------

def test_application_open():
    assert application_status(30, False, False) == "open"


def test_application_closing():
    assert application_status(20, False, False) == "closing"


def test_application_closed():
    assert application_status(10, False, False) == "closed"


def test_express_peak_season_cutoff():
    assert application_status(25, True, True) == "open"
