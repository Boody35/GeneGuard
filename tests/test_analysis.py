from analysis import TranslationAnalyzer, detect_mutations

def test_multiple_substitutions():
    mutations = detect_mutations("ATGGAA", "ACGGAT")
    assert len(mutations) == 2
    assert all(mutation.get_type() == "Substitution" for mutation in mutations)

def test_simple_insertion():
    mutations = detect_mutations("ATGGAA", "ATGCGAA")
    assert len(mutations) == 1
    assert mutations[0].get_type() == "Insertion"
    assert mutations[0].inserted_base == "C"

def test_simple_deletion():
    mutations = detect_mutations("ATGCGAA", "ATGGAA")
    assert len(mutations) == 1
    assert mutations[0].get_type() == "Deletion"
    assert mutations[0].deleted_base == "C"

def test_silent_mutation():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_substitution("GAA", "GAG", 2)
    assert result["impact"] == "Silent Mutation"

def test_missense_mutation():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_substitution("GAA", "GAT", 2)
    assert result["impact"] == "Missense Mutation"

def test_nonsense_mutation():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_substitution("GAA", "TAA", 0)
    assert result["impact"] == "Nonsense Mutation"

def test_stop_loss_mutation():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_substitution("TAA", "CAA", 0)
    assert result["impact"] == "Stop-loss Mutation"

def test_frameshift_insertion():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_insertion_deletion("insertion", 1, 3)
    assert result["impact"] == "Frameshift Mutation"

def test_in_frame_deletion():
    analyzer = TranslationAnalyzer()
    result = analyzer.analyze_insertion_deletion("deletion", 3, 3)
    assert result["impact"] == "In-frame Deletion"