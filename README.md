GeneGuard is a Python Tool for comparing two DNA sequences and detecting genetic mutations.

The user enters a reference DNA sequence and a mutated DNA sequence manually or imports them from TXT files. The program validates the sequences, detects mutations, translates codons, analyzes the mutation effect, and generates a report or a summary.

This project was developed as part of our Python training project.

Features:
	•	Manual DNA sequence input
	•	Import DNA sequences from TXT files
	•	DNA validation
	•	Substitution detection
	•	Insertion detection
	•	Deletion detection
	•	Codon splitting
	•	DNA translation to amino acids
	•	Mutation impact detection
	•	DNA statistics and GC content
	•	Summary report
	•	Full analysis report
	•	TXT report export
	•	CustomTkinter GUI
	•	Error handling
	•	Automated tests using pytest

Mutation Impact
GeneGuard can classify mutation effects such as:
	•	Silent Mutation
	•	Missense Mutation
	•	Nonsense Mutation
	•	Stop-loss Mutation
	•	Frameshift Mutation
	•	In-frame Insertion
	•	In-frame Deletion

Project Structure
GeneGuard/
├── main.py
├── gui.py
├── analysis.py
├── backend.py
├── report_formatter.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    ├── test_analysis.py
    ├── test_edge_cases.py
    ├── test_files.py
    ├── test_reports.py
    ├── test_statistics.py
    └── test_validation.py

Main Files
main.py: Starts the application.
gui.py: Contains the CustomTkinter graphical interface and connects the user with the analysis functions.
analysis.py: Contains mutation classes, mutation detection, codon translation, and mutation impact analysis.
backend.py: Handles DNA validation, file reading, exceptions, and DNA statistics.
report_formatter.py: Creates the summary and full analysis reports.
tests: Contains the automated tests for the main parts of the project.

Requirements
	•	Python 3.10 or newer
	•	CustomTkinter
	•	pytest
Install the required packages using:
pip install -r requirements.txt

Running the Project
Run:
python main.py
The GeneGuard interface will open.
Enter the Reference DNA and Mutated DNA manually, or import them from TXT files, then click Analyze.
Example
Reference DNA:
ATGCGTACG
Mutated DNA:
ATGCGTTCG
The program compares both sequences and displays the detected mutation and its possible effect.

Reports
GeneGuard provides two export options:
	•	Summary Report
	•	Full Analysis Report
The reports can be saved as TXT files.

Testing
The project uses pytest for automated testing.
Run all tests using:
python -m pytest
Current result:
26 tests passed
The tests cover mutation analysis, DNA validation, file handling, reports, statistics, and edge cases.

Team Work
The project was divided between four team members:
	•	Person 1: Input, Validation, Files, and Exceptions
	•	Person 2: Mutation Detection, OOP, Inheritance, and Abstract Classes
	•	Person 3: Codons, Translation, and Mutation Impact
	•	Person 4: Main Menu, Reports, Testing, and Project Integration

Current Limitations
The current version supports substitutions and simple single-region insertions and deletions.
More complex DNA alignment and multiple insertion/deletion regions are outside the current project scope.
