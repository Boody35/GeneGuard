from abc import ABC, abstractmethod

class Mutation(ABC):
    def __init__(self, position):
        self.position = position
    @abstractmethod
    def get_type(self):
        pass

class SubstitutionMutation(Mutation):
    def __init__(self, position, old_base, new_base):
        super().__init__(position)
        self.old_base = old_base
        self.new_base = new_base
    def get_type(self):
        return "Substitution"

class InsertionMutation(Mutation):
    def __init__(self, position, inserted_base):
        super().__init__(position)
        self.inserted_base = inserted_base
    def get_type(self):
        return "Insertion"

class DeletionMutation(Mutation):
    def __init__(self, position, deleted_base):
        super().__init__(position)
        self.deleted_base = deleted_base
    def get_type(self):
        return "Deletion"

def detect_mutations(reference, mutated):
    mutations = []
    if len(reference) == len(mutated):
        for i in range(len(reference)):
            if reference[i] != mutated[i]:
                mutation = SubstitutionMutation(i + 1,reference[i],mutated[i])
                mutations.append(mutation)
    elif len(mutated) > len(reference):
        i = 0
        while i < len(reference) and reference[i] == mutated[i]:
            i += 1
        for j in range(i + 1, len(mutated) + 1):
            if mutated[j:] == reference[i:]:
                mutation = InsertionMutation(i + 1,mutated[i:j])
                mutations.append(mutation)
                break
    elif len(reference) > len(mutated):
        i = 0
        while i < len(mutated) and reference[i] == mutated[i]:
            i += 1
        for j in range(i + 1, len(reference) + 1):
            if reference[j:] == mutated[i:]:
                mutation = DeletionMutation(i + 1,reference[i:j])
                mutations.append(mutation)
                break
    return mutations

CODON_TABLE = {
    "TTT": "Phe", "TTC": "Phe", "TTA": "Leu", "TTG": "Leu",
    "TCT": "Ser", "TCC": "Ser", "TCA": "Ser", "TCG": "Ser",
    "TAT": "Tyr", "TAC": "Tyr", "TAA": "STOP", "TAG": "STOP",
    "TGT": "Cys", "TGC": "Cys", "TGA": "STOP", "TGG": "Trp",
    "CTT": "Leu", "CTC": "Leu", "CTA": "Leu", "CTG": "Leu",
    "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "CAT": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "CGT": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "ATT": "Ile", "ATC": "Ile", "ATA": "Ile", "ATG": "Met",
    "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AAT": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "AGT": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val",
    "GCT": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "GAT": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",}

class TranslationAnalyzerError(Exception):
    pass

class TranslationAnalyzer:
    def split_into_codons(self, dna_sequence):
        dna_sequence = dna_sequence.upper()
        codons = []
        for index in range(0, len(dna_sequence), 3):
            codon = dna_sequence[index:index + 3]
            if len(codon) == 3:
                codons.append(codon)
        return codons

    def translate_codon(self, codon):
        codon = codon.upper()
        if len(codon) != 3:
            raise TranslationAnalyzerError("Codons must contain just 3 bases.")
        amino_acid = CODON_TABLE.get(codon)
        if amino_acid is None:
            raise TranslationAnalyzerError(f"Unknown codon: {codon}")
        return amino_acid

    def translate_sequence(self, dna_sequence):
        codons = self.split_into_codons(dna_sequence)
        amino_acids = []
        for codon in codons:
            amino_acid = self.translate_codon(codon)
            amino_acids.append(amino_acid)
            if amino_acid == "STOP":
                break
        return amino_acids

    def analyze_substitution(self,reference_dna,mutated_dna,position):
        codon_index = position // 3
        codon_start = codon_index * 3
        codon_end = codon_start + 3
        reference_codon = reference_dna[codon_start:codon_end]
        mutated_codon = mutated_dna[codon_start:codon_end]
        if len(reference_codon) != 3 or len(mutated_codon) != 3:
            raise TranslationAnalyzerError("The affected codon is incomplete.")
        reference_amino_acid = self.translate_codon(reference_codon)
        mutated_amino_acid = self.translate_codon(mutated_codon)
        if reference_amino_acid == mutated_amino_acid:
            impact = "Silent Mutation"
        elif (mutated_amino_acid == "STOP"and reference_amino_acid != "STOP"):
            impact = "Nonsense Mutation"
        elif (reference_amino_acid == "STOP"and mutated_amino_acid != "STOP"):
            impact = "Stop-loss Mutation"
        else:
            impact = "Missense Mutation"

        return {"affected_codon_number": codon_index + 1,
            "reference_codon": reference_codon,
            "mutated_codon": mutated_codon,
            "reference_amino_acid": reference_amino_acid,
            "mutated_amino_acid": mutated_amino_acid,
            "impact": impact,}

    def analyze_insertion_deletion(self,mutation_type,mutation_length,position):
        if mutation_length <= 0:
            raise TranslationAnalyzerError("Mutation length must be greater than zero.")
        affected_codon_number = (position // 3) + 1
        if mutation_length % 3 != 0:
            impact = "Frameshift Mutation"
        elif mutation_type == "insertion":
            impact = "In-frame Insertion"
        elif mutation_type == "deletion":
            impact = "In-frame Deletion"
        else:
            raise TranslationAnalyzerError(f"Unknown mutation type: {mutation_type}")
        return {"affected_codon_number": affected_codon_number,
            "mutation_length": mutation_length,"impact": impact,}

    def analyze_mutation_impact(self,reference_dna,mutated_dna,mutation_info):
        reference_dna = reference_dna.upper()
        mutated_dna = mutated_dna.upper()
        reference_codons = self.split_into_codons(reference_dna)
        mutated_codons = self.split_into_codons(mutated_dna)
        reference_protein = self.translate_sequence(reference_dna)
        mutated_protein = self.translate_sequence(mutated_dna)
        mutation_type = mutation_info["type"].lower()
        position = mutation_info["position"]
        if mutation_type == "substitution":
            impact_details = self.analyze_substitution(reference_dna,mutated_dna,position)
        elif mutation_type in ("insertion", "deletion"):
            mutation_length = mutation_info["length"]
            impact_details = self.analyze_insertion_deletion(mutation_type,mutation_length,position)
        elif mutation_type == "none":
            impact_details = {"impact": "No Mutation"}
        else:
            raise TranslationAnalyzerError(f"Unsupported mutation type: {mutation_type}")
        return {"reference_codons": reference_codons,
            "mutated_codons": mutated_codons,
            "reference_protein": reference_protein,
            "mutated_protein": mutated_protein,
            "mutation_details": impact_details,
            "mutation_impact": impact_details["impact"],}