import pytest

from backend import DNAValidationError, validate_dna

def test_validation_normalizes_spaces_and_lowercase():
    assert validate_dna("atg \n gaa") == "ATGGAA"

def test_empty_dna_is_rejected():
    with pytest.raises(DNAValidationError):
        validate_dna("   ")

def test_invalid_base_is_rejected():
    with pytest.raises(DNAValidationError):
        validate_dna("ATGX")

def test_max_length_is_enforced():
    with pytest.raises(DNAValidationError):
        validate_dna("ATGC", max_length=3)