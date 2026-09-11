from backend import calculate_dna_statistics

def test_dna_statistics_length_and_counts():
    stats = calculate_dna_statistics("AATTGGCC")

    assert stats["length"] == 8
    assert stats["a_count"] == 2
    assert stats["t_count"] == 2
    assert stats["g_count"] == 2
    assert stats["c_count"] == 2

def test_gc_content():
    stats = calculate_dna_statistics("GGCCAT")

    assert round(stats["gc_content"], 2) == 66.67

def test_base_percentages():
    stats = calculate_dna_statistics("ATGC")

    assert stats["a_percent"] == 25.0
    assert stats["t_percent"] == 25.0
    assert stats["g_percent"] == 25.0
    assert stats["c_percent"] == 25.0