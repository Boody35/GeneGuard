import pytest
from backend import DNAFileError, UnsupportedFileFormatError, read_dna_from_file

def test_read_valid_txt_file(tmp_path):
    dna_file = tmp_path / "dna.txt"
    dna_file.write_text("atg gaa", encoding="utf-8")

    assert read_dna_from_file(dna_file) == "ATGGAA"

def test_non_txt_file_is_rejected(tmp_path):
    dna_file = tmp_path / "dna.csv"
    dna_file.write_text("ATGGAA", encoding="utf-8")

    with pytest.raises(UnsupportedFileFormatError):
        read_dna_from_file(dna_file)

def test_empty_file_is_rejected(tmp_path):
    dna_file = tmp_path / "empty.txt"
    dna_file.write_text("", encoding="utf-8")

    with pytest.raises(DNAFileError):
        read_dna_from_file(dna_file)

def test_invalid_dna_file_is_rejected(tmp_path):
    dna_file = tmp_path / "invalid.txt"
    dna_file.write_text("ATGX", encoding="utf-8")

    with pytest.raises(DNAFileError):
        read_dna_from_file(dna_file)