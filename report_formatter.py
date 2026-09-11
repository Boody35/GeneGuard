from datetime import datetime

def _mutation_change(mutation):
    mutation_type = mutation.get_type()
    if mutation_type == "Substitution":
        return f"{mutation.old_base} -> {mutation.new_base}"
    if mutation_type == "Insertion":
        return f"+{mutation.inserted_base}"
    if mutation_type == "Deletion":
        return f"-{mutation.deleted_base}"
    return mutation_type

def _mutation_counts(mutations):
    counts = {"Substitution": 0,"Insertion": 0,"Deletion": 0,}
    for mutation in mutations:
        mutation_type = mutation.get_type()
        if mutation_type in counts:
            counts[mutation_type] += 1
    return counts

def _format_list(values):
    return " ".join(values) if values else "None"

def _format_percent(value):
    return f"{value:.2f}%"

def generate_summary_report(
    reference_dna,
    mutated_dna,mutations,
    reference_stats,mutated_stats,
    impacts,supported=True,):
    counts = _mutation_counts(mutations)
    gc_change = mutated_stats["gc_content"] - reference_stats["gc_content"]

    lines = [
        "=" * 58,
        "GENEGUARD - ANALYSIS SUMMARY",
        "=" * 58,
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        f"Reference Length: {reference_stats['length']} bp",
        f"Mutated Length:   {mutated_stats['length']} bp",
        f"Reference GC:     {_format_percent(reference_stats['gc_content'])}",
        f"Mutated GC:       {_format_percent(mutated_stats['gc_content'])}",
        f"GC Change:        {gc_change:+.2f}%",
        "",
        f"Total Mutations:  {len(mutations)}",
        f"Substitutions:    {counts['Substitution']}",
        f"Insertions:       {counts['Insertion']}",
        f"Deletions:        {counts['Deletion']}",
        "",]

    if not supported:
        lines.extend(["Status: Unsupported change pattern",
            "The sequences differ, but the current detector supports only",
            "substitutions and simple single-region insertions/deletions.",])
    elif not mutations:
        lines.append("Status: No mutations detected")
    else:
        lines.append("Mutation Results:")
        for index, mutation in enumerate(mutations, 1):
            impact = impacts[index - 1].get("mutation_impact", "Unavailable")
            lines.append(f"{index}. {mutation.get_type()} at position "
                f"{mutation.position}: {_mutation_change(mutation)} | {impact}")
    lines.extend(["", "=" * 58])
    return "\n".join(lines)

def generate_professional_report(reference_dna,
    mutated_dna, mutations, reference_stats,
    mutated_stats, translation,impacts,
    supported=True,):

    counts = _mutation_counts(mutations)
    gc_change = mutated_stats["gc_content"] - reference_stats["gc_content"]

    lines = [
        "=" * 64,
        "                         GENEGUARD",
        "                 DNA MUTATION ANALYSIS REPORT",
        "=" * 64,
        "",
        "Analysis Status: COMPLETE",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        "-" * 64,
        "1. SEQUENCE INFORMATION",
        "-" * 64,
        "",
        "Reference DNA:",
        reference_dna,
        "",
        "Mutated DNA:",
        mutated_dna,
        "",
        f"Reference Length: {reference_stats['length']} bp",
        f"Mutated Length:   {mutated_stats['length']} bp",
        "",
        "-" * 64,
        "2. MUTATION SUMMARY",
        "-" * 64,
        "",
        f"Total Mutations: {len(mutations)}",
        f"Substitutions:   {counts['Substitution']}",
        f"Insertions:      {counts['Insertion']}",
        f"Deletions:       {counts['Deletion']}",
        "",]

    if not supported:
        lines.extend([
            "A sequence difference was detected, but this change pattern is",
            "outside the scope of the current simple mutation detector.",
            "Supported patterns: substitutions and simple single-region",
            "insertions/deletions.",
            "",])
        
    elif not mutations:
        lines.extend(["No mutations detected.", ""])
    else:
        for index, mutation in enumerate(mutations, 1):
            impact_data = impacts[index - 1]
            details = impact_data.get("mutation_details", {})
            impact = impact_data.get("mutation_impact", "Unavailable")

            lines.extend([
                f"Mutation #{index}",
                f"Type: {mutation.get_type()}",
                f"Position: {mutation.position}",
                f"Change: {_mutation_change(mutation)}",
                f"Impact: {impact}",])

            if "affected_codon_number" in details:
                lines.append(
                    f"Affected Codon Number: {details['affected_codon_number']}")

            if mutation.get_type() == "Substitution" and details:
                lines.extend([
                    f"Codon: {details['reference_codon']} -> "
                    f"{details['mutated_codon']}",
                    f"Amino Acid: {details['reference_amino_acid']} -> "
                    f"{details['mutated_amino_acid']}",])
            elif mutation.get_type() == "Insertion":
                lines.append(
                    f"Mutation Length: {len(mutation.inserted_base)} base(s)")
            elif mutation.get_type() == "Deletion":
                lines.append(
                    f"Mutation Length: {len(mutation.deleted_base)} base(s)")

            if "error" in impact_data:
                lines.append(f"Translation Note: {impact_data['error']}")
            lines.append("")

    lines.extend([ "-" * 64,
        "3. CODON AND PROTEIN ANALYSIS",
        "-" * 64,
        "",
        "Reference Codons: " + _format_list(translation["reference_codons"]),
        "Mutated Codons:   " + _format_list(translation["mutated_codons"]),
        "Reference Protein: " + _format_list(translation["reference_protein"]),
        "Mutated Protein:   " + _format_list(translation["mutated_protein"]),
        "",
        "-" * 64,
        "4. DNA STATISTICS",
        "-" * 64,
        "",
        f"Reference GC Content: {_format_percent(reference_stats['gc_content'])}",
        f"Mutated GC Content:   {_format_percent(mutated_stats['gc_content'])}",
        f"GC Content Change:    {gc_change:+.2f}%",
        "",
        "Reference Base Composition:",
        f"A: {reference_stats['a_count']} ({reference_stats['a_percent']:.2f}%)",
        f"T: {reference_stats['t_count']} ({reference_stats['t_percent']:.2f}%)",
        f"G: {reference_stats['g_count']} ({reference_stats['g_percent']:.2f}%)",
        f"C: {reference_stats['c_count']} ({reference_stats['c_percent']:.2f}%)",
        "",
        "Mutated Base Composition:",
        f"A: {mutated_stats['a_count']} ({mutated_stats['a_percent']:.2f}%)",
        f"T: {mutated_stats['t_count']} ({mutated_stats['t_percent']:.2f}%)",
        f"G: {mutated_stats['g_count']} ({mutated_stats['g_percent']:.2f}%)",
        f"C: {mutated_stats['c_count']} ({mutated_stats['c_percent']:.2f}%)",
        "",
        "-" * 64,
        "5. ANALYSIS SUMMARY",
        "-" * 64,
        "",])

    if not supported:
        lines.append("Result: Sequence difference detected - unsupported pattern.")
    elif not mutations:
        lines.append("Result: No mutations detected.")
    else:
        impact_names = [
            item.get("mutation_impact", "Unavailable")
            for item in impacts]
        lines.append(f"Result: {len(mutations)} mutation(s) detected.")
        lines.append("Detected Impact(s): " + ", ".join(impact_names))

    lines.extend(["",
        "GeneGuard is an educational analysis tool and is not intended for",
        "medical, clinical, or diagnostic use.",
        "",
        "=" * 64,
        "                       ANALYSIS COMPLETE",
        "=" * 64,])
    return "\n".join(lines)