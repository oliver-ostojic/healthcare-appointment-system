from utils.specialty_helper import get_taxonomy_code

def test_get_taxonomy_code_found():
    result = get_taxonomy_code("Cardiology")
    # Assert the correct taxonomy code is returned
    assert result == "207RA0001X"

def test_get_taxonomy_code_not_found():
    result = get_taxonomy_code("UnknownSpecialty")
    assert result is None