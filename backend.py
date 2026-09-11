from pathlib import Path

class DNAValidationError(ValueError):
    pass

class DNAFileError(OSError):
    pass

class UnsupportedFileFormatError(DNAFileError):
    pass

VALID_BASES = frozenset("ATGC")

def normalize_dna(sequence):
    if not isinstance(sequence, str):
        raise DNAValidationError("DNA sequence must be a string.")
    return "".join(sequence.split()).upper()

def find_invalid_bases(sequence):
    sequence = normalize_dna(sequence)
    return sorted({base for base in sequence if base not in VALID_BASES})

def validate_dna(sequence, min_length=1, max_length=None):
    sequence = normalize_dna(sequence)
    if not sequence:
        raise DNAValidationError("DNA sequence cannot be empty.")
    invalid_bases = find_invalid_bases(sequence)
    if invalid_bases:
        invalid_text = ", ".join(invalid_bases)
        raise DNAValidationError(f"Invalid DNA base(s): {invalid_text}. "
            "Only A, T, G, and C are allowed.")
    if not isinstance(min_length, int) or min_length < 1:
        raise ValueError("min_length must be a positive integer.")
    if len(sequence) < min_length:
        raise DNAValidationError(f"DNA sequence must contain at least "f"{min_length} bases.")
    if max_length is not None:
        if not isinstance(max_length, int):
            raise ValueError("max length must be None or integer.")

        if max_length < min_length:
            raise ValueError("max_length cannot be smaller than min_length.")

        if len(sequence) > max_length:
            raise DNAValidationError(f"DNA sequence cannot contain more than "
                f"{max_length} bases.")
    return sequence

SUPPORTED_EXTENSIONS = {".txt"}

def validate_file_extension(filename):
    path = Path(filename)
    extension = path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileFormatError(f"Unsupported file format: {extension}. "
            "Only .txt files are supported.")
    return extension

def read_dna_from_file(filename,min_length=1,max_length=None):
    path = Path(filename)
    validate_file_extension(path)
    if not path.exists():
        raise DNAFileError(f"DNA file was not found: {path}")
    if not path.is_file():
        raise DNAFileError(f"The path is not a file: {path}")
    try:
        content = path.read_text(encoding="utf-8")
    except PermissionError as error:
        raise DNAFileError(f"Permission denied while reading: {path}") from error

    except UnicodeDecodeError as error:
        raise DNAFileError(f"Could not decode DNA file: {path}") from error
    except OSError as error:
        raise DNAFileError(f"Could not read DNA file: {path}") from error
    if not content.strip():
        raise DNAFileError(f"DNA file is empty: {path}")
    try:
        return validate_dna(content,min_length=min_length,max_length=max_length)
    except DNAValidationError as error:
        raise DNAFileError(f"Invalid DNA data inside file: {path}. {error}") from error

def calculate_dna_statistics(sequence):
    sequence = validate_dna(sequence)
    length = len(sequence)
    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    a_percent = (a_count / length) * 100
    t_percent = (t_count / length) * 100
    g_percent = (g_count / length) * 100
    c_percent = (c_count / length) * 100
    gc_content = ((g_count + c_count) / length) * 100
    return {"length": length,
        "a_count": a_count,
        "t_count": t_count,
        "g_count": g_count,
        "c_count": c_count,
        "a_percent": a_percent,
        "t_percent": t_percent,
        "g_percent": g_percent,
        "c_percent": c_percent,
        "gc_content": gc_content,}

def generate_report(reference, mutated, mutations):
    report = []
    report.append("========== GeneGuard Report ==========")
    report.append(f"Reference DNA: {reference}")
    report.append(f"Mutated DNA:   {mutated}")
    if not mutations:
        report.append("")
        report.append("No mutations detected.")
    else:
        report.append("")
        report.append(f"Mutations detected: {len(mutations)}")
        for mutation in mutations:
            report.append("")
            report.append(f"Mutation type: {mutation.get_type()}")
            report.append(f"Position: {mutation.position}")

            if mutation.get_type() == "Substitution":
                report.append(f"Old base: {mutation.old_base}")
                report.append(f"New base: {mutation.new_base}")

            elif mutation.get_type() == "Insertion":
                report.append(
                    f"Inserted base: {mutation.inserted_base}"
                )

            elif mutation.get_type() == "Deletion":
                report.append(f"Deleted base: {mutation.deleted_base}")
    report.append("======================================")
    return "\n".join(report)