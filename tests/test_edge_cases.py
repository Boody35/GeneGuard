import pytest
from analysis import TranslationAnalyzer, TranslationAnalyzerError, detect_mutations
from backend import DNAFileError, read_dna_from_file

def test_no_mutation_detected_for_identical_sequences():
    assert detect_mutations("ATGGAA", "ATGGAA") == []

def test_incomplete_affected_codon_is_rejected():
    analyzer = TranslationAnalyzer()

    with pytest.raises(TranslationAnalyzerError):
        analyzer.analyze_substitution("ATGGA", "ATGGT", 4)

def test_missing_txt_file_is_rejected(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(DNAFileError):
        read_dna_from_file(missing_file)

def test_complex_change_pattern_remains_outside_simple_detector_scope():
    mutations = detect_mutations("ATGCAA", "ACTGGAA")
    assert mutations == []