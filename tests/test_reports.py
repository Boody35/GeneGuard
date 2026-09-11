from analysis import TranslationAnalyzer, detect_mutations
from backend import calculate_dna_statistics
from report_formatter import generate_professional_report, generate_summary_report


def build_report_data(reference, mutated):
    mutations = detect_mutations(reference, mutated)
    analyzer = TranslationAnalyzer()
    impacts = []

    for mutation in mutations:
        mutation_info = {"type": mutation.get_type(),
            "position": mutation.position - 1,}

        if mutation.get_type() == "Insertion":
            mutation_info["length"] = len(mutation.inserted_base)
        elif mutation.get_type() == "Deletion":
            mutation_info["length"] = len(mutation.deleted_base)

        impacts.append(
            analyzer.analyze_mutation_impact(reference,mutated,mutation_info)
        )

    translation = {
        "reference_codons": analyzer.split_into_codons(reference),
        "mutated_codons": analyzer.split_into_codons(mutated),
        "reference_protein": analyzer.translate_sequence(reference),
        "mutated_protein": analyzer.translate_sequence(mutated),}

    return (mutations,
        calculate_dna_statistics(reference),
        calculate_dna_statistics(mutated),
        translation,
        impacts,)


def test_full_report_contains_expected_sections_without_missing_placeholders():
    reference = "GAA"
    mutated = "GAT"
    mutations, reference_stats, mutated_stats, translation, impacts = (
        build_report_data(reference, mutated))

    report = generate_professional_report(
        reference,
        mutated,
        mutations,
        reference_stats,
        mutated_stats,
        translation,
        impacts,
        True,)

    assert "MUTATION SUMMARY" in report
    assert "CODON AND PROTEIN ANALYSIS" in report
    assert "DNA STATISTICS" in report
    assert "Missense Mutation" in report
    assert "N/A" not in report


def test_summary_report_contains_counts_and_impact():
    reference = "GAA"
    mutated = "GAT"
    mutations, reference_stats, mutated_stats, _, impacts = build_report_data(
        reference,
        mutated,)

    report = generate_summary_report(
        reference,
        mutated,
        mutations,
        reference_stats,
        mutated_stats,
        impacts,
        True,)

    assert "Total Mutations:  1" in report
    assert "Substitutions:    1" in report
    assert "Missense Mutation" in report