import customtkinter as ctk
from tkinter import filedialog, messagebox

from backend import (
    DNAFileError,
    DNAValidationError,
    calculate_dna_statistics,
    generate_report,
    read_dna_from_file,
    validate_dna,
)
from analysis import (
    TranslationAnalyzer,
    TranslationAnalyzerError,
    detect_mutations,
)
from report_formatter import (
    generate_professional_report,
    generate_summary_report,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GeneGuardApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("GeneGuard")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.BG = "#080A09"
        self.CARD = "#111412"
        self.INPUT = "#181B19"
        self.BORDER = "#343934"

        self.GREEN = "#7CF567"
        self.GREEN_HOVER = "#68DA57"

        self.WHITE = "#F4F4F4"
        self.GRAY = "#979D98"

        self.configure(fg_color=self.BG)
        self.export_options_visible = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_interface()

    def create_interface(self):
        main_card = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=28,
            border_width=1,
            border_color=self.BORDER
        )

        main_card.grid(
            row=0,
            column=0,
            padx=45,
            pady=40,
            sticky="nsew"
        )

        main_card.grid_columnconfigure(0, weight=1)
        main_card.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            main_card,
            text="GeneGuard",
            font=("Segoe UI", 32, "bold"),
            text_color=self.WHITE
        ).grid(
            row=0,
            column=0,
            padx=35,
            pady=(30, 0),
            sticky="w"
        )

        ctk.CTkLabel(
            main_card,
            text=(
                "Enter the two DNA sequences manually or import each one "
                "from a TXT file."
            ),
            font=("Segoe UI", 13),
            text_color=self.GRAY
        ).grid(
            row=2,
            column=0,
            padx=35,
            pady=(0, 12),
            sticky="w"
        )

        inputs_frame = ctk.CTkFrame(
            main_card,
            fg_color="transparent"
        )

        inputs_frame.grid(
            row=3,
            column=0,
            padx=35,
            pady=(0, 20),
            sticky="nsew"
        )

        inputs_frame.grid_columnconfigure(0, weight=1)
        inputs_frame.grid_columnconfigure(1, weight=1)
        inputs_frame.grid_rowconfigure(0, weight=1)

        reference_card = self.create_sequence_card(
            inputs_frame,
            title="Reference DNA",
            placeholder="Enter original DNA sequence...",
            column=0,
            import_command=lambda: self.import_txt("reference")
        )

        mutated_card = self.create_sequence_card(
            inputs_frame,
            title="Mutated DNA",
            placeholder="Enter mutated DNA sequence...",
            column=1,
            import_command=lambda: self.import_txt("mutated")
        )

        self.reference_text = reference_card
        self.mutated_text = mutated_card

        actions = ctk.CTkFrame(
            main_card,
            fg_color="transparent"
        )

        actions.grid(
            row=4,
            column=0,
            padx=35,
            pady=(0, 30),
            sticky="ew"
        )

        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=0)
        actions.grid_columnconfigure(2, weight=0)
        actions.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(
            actions,
            text="Analyze",
            width=180,
            height=52,
            corner_radius=16,
            fg_color="#F2F2F2",
            hover_color="#DADADA",
            text_color="#111111",
            font=("Segoe UI", 14, "bold"),
            command=self.show_results
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        ctk.CTkButton(
            actions,
            text="Export Report",
            width=180,
            height=52,
            corner_radius=16,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            text_color="#081008",
            font=("Segoe UI", 14, "bold"),
            command=self.export_report
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        self.export_options_frame = ctk.CTkFrame(
            main_card,
            fg_color=self.INPUT,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )
        self.export_options_frame.grid(
            row=5,
            column=0,
            padx=35,
            pady=(0, 30),
            sticky="ew"
        )
        self.export_options_frame.grid_columnconfigure(1, weight=1)
        self.export_options_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            self.export_options_frame,
            text="Choose export type",
            font=("Segoe UI", 14, "bold"),
            text_color=self.WHITE
        ).grid(
            row=0,
            column=0,
            padx=(18, 14),
            pady=16,
            sticky="w"
        )

        ctk.CTkButton(
            self.export_options_frame,
            text="Export Summary",
            height=42,
            corner_radius=13,
            fg_color="#F2F2F2",
            hover_color="#DADADA",
            text_color="#111111",
            font=("Segoe UI", 13, "bold"),
            command=lambda: self.save_export("summary")
        ).grid(
            row=0,
            column=1,
            padx=6,
            pady=12,
            sticky="ew"
        )

        ctk.CTkButton(
            self.export_options_frame,
            text="Export Full Report",
            height=42,
            corner_radius=13,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            text_color="#081008",
            font=("Segoe UI", 13, "bold"),
            command=lambda: self.save_export("full")
        ).grid(
            row=0,
            column=2,
            padx=(6, 18),
            pady=12,
            sticky="ew"
        )

        self.export_options_frame.grid_remove()

    def create_sequence_card(
        self,
        parent,
        title,
        placeholder,
        column,
        import_command
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        card.grid(
            row=0,
            column=column,
            padx=(0, 10) if column == 0 else (10, 0),
            sticky="nsew"
        )

        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=self.WHITE
        ).grid(
            row=0,
            column=0,
            pady=(0, 8),
            sticky="w"
        )

        text_box = ctk.CTkTextbox(
            card,
            height=190,
            corner_radius=18,
            fg_color=self.INPUT,
            border_width=1,
            border_color=self.BORDER,
            text_color="#C0FFB8",
            font=("Consolas", 15),
            wrap="word"
        )

        text_box.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=placeholder,
            font=("Segoe UI", 11),
            text_color=self.GRAY
        ).grid(
            row=2,
            column=0,
            pady=(7, 6),
            sticky="w"
        )

        ctk.CTkButton(
            card,
            text="Import TXT",
            width=125,
            height=38,
            corner_radius=13,
            fg_color="#242824",
            hover_color="#343934",
            border_width=1,
            border_color=self.BORDER,
            text_color=self.WHITE,
            font=("Segoe UI", 13, "bold"),
            command=import_command
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        return text_box

    @staticmethod
    def get_textbox_sequence(text_box):
        return text_box.get("1.0", "end")

    def check_inputs(self):
        reference_raw = self.get_textbox_sequence(self.reference_text)
        mutated_raw = self.get_textbox_sequence(self.mutated_text)

        try:
            reference = validate_dna(reference_raw)
        except DNAValidationError as error:
            messagebox.showerror(
                "Invalid Reference DNA",
                str(error)
            )
            return None

        try:
            mutated = validate_dna(mutated_raw)
        except DNAValidationError as error:
            messagebox.showerror(
                "Invalid Mutated DNA",
                str(error)
            )
            return None

        return reference, mutated

    @staticmethod
    def format_list(values):
        if not values:
            return "None"
        return " ".join(values)

    @staticmethod
    def collect_report_data(reference, mutated):
        mutations = detect_mutations(reference, mutated)
        reference_stats = calculate_dna_statistics(reference)
        mutated_stats = calculate_dna_statistics(mutated)
        analyzer = TranslationAnalyzer()

        translation = {
            "reference_codons": analyzer.split_into_codons(reference),
            "mutated_codons": analyzer.split_into_codons(mutated),
            "reference_protein": analyzer.translate_sequence(reference),
            "mutated_protein": analyzer.translate_sequence(mutated),
        }

        impacts = []
        for mutation in mutations:
            mutation_type = mutation.get_type()
            mutation_info = {
                "type": mutation_type,
                "position": mutation.position - 1,
            }

            if mutation_type == "Insertion":
                mutation_info["length"] = len(mutation.inserted_base)
            elif mutation_type == "Deletion":
                mutation_info["length"] = len(mutation.deleted_base)

            try:
                impact = analyzer.analyze_mutation_impact(
                    reference,
                    mutated,
                    mutation_info
                )
            except TranslationAnalyzerError as error:
                impact = {
                    "mutation_details": {},
                    "mutation_impact": "Unavailable",
                    "error": str(error),
                }

            impacts.append(impact)

        return {
            "mutations": mutations,
            "reference_stats": reference_stats,
            "mutated_stats": mutated_stats,
            "translation": translation,
            "impacts": impacts,
            "supported": reference == mutated or bool(mutations),
        }

    @staticmethod
    def build_difference_lines(reference, mutated, mutations):
        if reference == mutated:
            return reference, mutated

        if len(mutations) == 1:
            mutation = mutations[0]
            index = mutation.position - 1

            if mutation.get_type() == "Insertion":
                inserted = mutation.inserted_base
                reference_line = (
                    reference[:index]
                    + "-" * len(inserted)
                    + reference[index:]
                )
                return reference_line, mutated

            if mutation.get_type() == "Deletion":
                deleted = mutation.deleted_base
                mutated_line = (
                    mutated[:index]
                    + "-" * len(deleted)
                    + mutated[index:]
                )
                return reference, mutated_line

        width = max(len(reference), len(mutated))
        return reference.ljust(width, "-"), mutated.ljust(width, "-")

    @staticmethod
    def build_statistics_section(reference, mutated):

        reference_stats = calculate_dna_statistics(reference)
        mutated_stats = calculate_dna_statistics(mutated)

        lines = [
            "",
            "================ DNA Statistics ================",
            f"Reference Length: {reference_stats['length']} bp",
            f"Mutated Length:   {mutated_stats['length']} bp",
            f"Reference GC Content: {reference_stats['gc_content']:.2f}%",
            f"Mutated GC Content:   {mutated_stats['gc_content']:.2f}%",
            "Reference Base Percentages: "
            f"A {reference_stats['a_percent']:.2f}% | "
            f"T {reference_stats['t_percent']:.2f}% | "
            f"G {reference_stats['g_percent']:.2f}% | "
            f"C {reference_stats['c_percent']:.2f}%",
            "Mutated Base Percentages:   "
            f"A {mutated_stats['a_percent']:.2f}% | "
            f"T {mutated_stats['t_percent']:.2f}% | "
            f"G {mutated_stats['g_percent']:.2f}% | "
            f"C {mutated_stats['c_percent']:.2f}%",
            "================================================",
        ]

        return "\n".join(lines)

    @staticmethod
    def build_translation_section(reference, mutated, mutations):
        analyzer = TranslationAnalyzer()

        lines = [
            "",
            "====== Codons + Translation + Mutation Impact ======",
            "Reference Codons: "
            + GeneGuardApp.format_list(
                analyzer.split_into_codons(reference)
            ),
            "Mutated Codons:   "
            + GeneGuardApp.format_list(
                analyzer.split_into_codons(mutated)
            ),
            "Reference Protein: "
            + GeneGuardApp.format_list(
                analyzer.translate_sequence(reference)
            ),
            "Mutated Protein:   "
            + GeneGuardApp.format_list(
                analyzer.translate_sequence(mutated)
            ),
        ]

        for mutation in mutations:
            mutation_type = mutation.get_type()
            mutation_info = {
                "type": mutation_type,
                "position": mutation.position - 1,
            }

            if mutation_type == "Insertion":
                mutation_info["length"] = len(mutation.inserted_base)
            elif mutation_type == "Deletion":
                mutation_info["length"] = len(mutation.deleted_base)

            try:
                result = analyzer.analyze_mutation_impact(
                    reference,
                    mutated,
                    mutation_info
                )

                details = result["mutation_details"]
                impact = result["mutation_impact"]

                if impact == "Silent Mutation":
                    impact = "Synonymous (Silent) Mutation"

                lines.append("")
                lines.append(
                    f"{mutation_type} at position {mutation.position}:"
                )
                lines.append(f"Impact: {impact}")

                if "affected_codon_number" in details:
                    lines.append(
                        "Affected codon number: "
                        f"{details['affected_codon_number']}"
                    )

                if mutation_type == "Substitution":
                    lines.append(
                        f"Codon: {details['reference_codon']} -> "
                        f"{details['mutated_codon']}"
                    )
                    lines.append(
                        "Amino acid: "
                        f"{details['reference_amino_acid']} -> "
                        f"{details['mutated_amino_acid']}"
                    )
                elif mutation_type == "Insertion":
                    lines.append(
                        f"Inserted bases: {mutation.inserted_base}"
                    )
                    lines.append(
                        f"Mutation length: {len(mutation.inserted_base)} base(s)"
                    )
                elif mutation_type == "Deletion":
                    lines.append(
                        f"Deleted bases: {mutation.deleted_base}"
                    )
                    lines.append(
                        f"Mutation length: {len(mutation.deleted_base)} base(s)"
                    )

            except TranslationAnalyzerError as error:
                lines.append("")
                lines.append(
                    f"{mutation_type} at position {mutation.position}:"
                )
                lines.append(
                    "Translation impact unavailable: "
                    f"{error}"
                )

        lines.append("====================================================")
        return "\n".join(lines)

    @staticmethod
    def get_mutation_display_data(reference, mutated, mutation):

        analyzer = TranslationAnalyzer()
        mutation_type = mutation.get_type()

        if mutation_type == "Substitution":
            change = f"{mutation.old_base} -> {mutation.new_base}"
        elif mutation_type == "Insertion":
            change = f"+{mutation.inserted_base}"
        else:
            change = f"-{mutation.deleted_base}"

        mutation_info = {
            "type": mutation_type,
            "position": mutation.position - 1,
        }

        if mutation_type == "Insertion":
            mutation_info["length"] = len(mutation.inserted_base)
        elif mutation_type == "Deletion":
            mutation_info["length"] = len(mutation.deleted_base)

        try:
            result = analyzer.analyze_mutation_impact(
                reference,
                mutated,
                mutation_info
            )
            impact = result["mutation_impact"]
            if impact == "Silent Mutation":
                impact = "Synonymous"
        except TranslationAnalyzerError:
            impact = "Unavailable"

        return {
            "position": mutation.position,
            "type": mutation_type,
            "change": change,
            "impact": impact,
        }

    @staticmethod
    def build_analysis_report(reference, mutated):
        mutations = detect_mutations(reference, mutated)
        statistics_section = GeneGuardApp.build_statistics_section(
            reference,
            mutated
        )

        if reference != mutated and not mutations:
            return (
                "========== GeneGuard Report ==========\n"
                f"Reference DNA: {reference}\n"
                f"Mutated DNA:   {mutated}\n\n"
                "Mutation detected, but this change pattern is not "
                "supported by the current simple mutation detector.\n"
                "Supported patterns: substitutions and simple "
                "single-region insertions/deletions.\n"
                "======================================"
                + statistics_section
            )

        basic_report = generate_report(
            reference,
            mutated,
            mutations
        )

        if not mutations:
            return basic_report + statistics_section

        translation_section = GeneGuardApp.build_translation_section(
            reference,
            mutated,
            mutations
        )

        return basic_report + statistics_section + translation_section

    def show_results(self):
        data = self.check_inputs()

        if not data:
            return

        reference, mutated = data

        try:
            mutations = detect_mutations(reference, mutated)
            result = self.build_analysis_report(
                reference,
                mutated
            )
        except TranslationAnalyzerError as error:
            messagebox.showerror(
                "Translation Error",
                str(error)
            )
            return
        except Exception as error:
            messagebox.showerror(
                "Analysis Error",
                str(error)
            )
            return

        self.show_result_window(
            reference,
            mutated,
            mutations,
            result
        )

    def create_summary_card(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )
        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 12),
            text_color=self.GRAY
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 2)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            text_color=self.WHITE
        ).pack(
            anchor="w",
            padx=14,
            pady=(0, 12)
        )

    def add_table_cell(
        self,
        parent,
        text,
        row,
        column,
        bold=False,
        color=None
    ):
        ctk.CTkLabel(
            parent,
            text=str(text),
            font=(
                "Segoe UI",
                12,
                "bold" if bold else "normal"
            ),
            text_color=color or self.WHITE,
            anchor="w"
        ).grid(
            row=row,
            column=column,
            padx=12,
            pady=8,
            sticky="ew"
        )

    def show_result_window(
        self,
        reference,
        mutated,
        mutations,
        result
    ):

        result_window = ctk.CTkToplevel(self)
        result_window.title("GeneGuard - Analysis Dashboard")
        result_window.geometry("1000x760")
        result_window.minsize(850, 650)
        result_window.configure(fg_color=self.BG)
        result_window.transient(self)
        result_window.grab_set()
        result_window.grid_columnconfigure(0, weight=1)
        result_window.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            result_window,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            padx=30,
            pady=(24, 12),
            sticky="ew"
        )
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Analysis Dashboard",
            font=("Segoe UI", 28, "bold"),
            text_color=self.WHITE
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Mutation summary, DNA statistics and impact",
            font=("Segoe UI", 13),
            text_color=self.GRAY
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="Close",
            width=100,
            height=38,
            corner_radius=14,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            text_color="#081008",
            font=("Segoe UI", 13, "bold"),
            command=result_window.destroy
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(16, 0),
            sticky="e"
        )

        content = ctk.CTkScrollableFrame(
            result_window,
            fg_color="transparent"
        )
        content.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew"
        )
        content.grid_columnconfigure(0, weight=1)

        reference_stats = calculate_dna_statistics(reference)
        mutated_stats = calculate_dna_statistics(mutated)

        summary = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        summary.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        self.create_summary_card(
            summary,
            0,
            "Mutations",
            str(len(mutations))
        )
        self.create_summary_card(
            summary,
            1,
            "Reference Length",
            f"{reference_stats['length']} bp"
        )
        self.create_summary_card(
            summary,
            2,
            "Mutated Length",
            f"{mutated_stats['length']} bp"
        )
        self.create_summary_card(
            summary,
            3,
            "Reference GC",
            f"{reference_stats['gc_content']:.2f}%"
        )
        self.create_summary_card(
            summary,
            4,
            "Mutated GC",
            f"{mutated_stats['gc_content']:.2f}%"
        )

        mutation_counts = {
            "Substitution": 0,
            "Insertion": 0,
            "Deletion": 0,
        }
        for mutation in mutations:
            mutation_counts[mutation.get_type()] += 1

        status_text = (
            f"Substitution: {mutation_counts['Substitution']}    "
            f"Insertion: {mutation_counts['Insertion']}    "
            f"Deletion: {mutation_counts['Deletion']}"
        )

        ctk.CTkLabel(
            content,
            text="Mutation Summary",
            font=("Segoe UI", 18, "bold"),
            text_color=self.WHITE
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        ctk.CTkLabel(
            content,
            text=status_text,
            font=("Segoe UI", 13),
            text_color=self.GRAY
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 12)
        )

        if reference != mutated and not mutations:
            ctk.CTkLabel(
                content,
                text=(
                    "A difference was detected, but the pattern is outside "
                    "the current simple mutation detector scope."
                ),
                font=("Segoe UI", 12),
                text_color=self.GREEN
            ).grid(
                row=3,
                column=0,
                sticky="w",
                pady=(0, 12)
            )

        ctk.CTkLabel(
            content,
            text="Mutation Details",
            font=("Segoe UI", 18, "bold"),
            text_color=self.WHITE
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(6, 8)
        )

        table = ctk.CTkFrame(
            content,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        table.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        for column in range(4):
            table.grid_columnconfigure(column, weight=1)

        headers = ["Position", "Type", "Change", "Impact"]
        for column, header_text in enumerate(headers):
            self.add_table_cell(
                table,
                header_text,
                0,
                column,
                bold=True,
                color=self.GREEN
            )

        if mutations:
            for row, mutation in enumerate(mutations, start=1):
                item = self.get_mutation_display_data(
                    reference,
                    mutated,
                    mutation
                )
                self.add_table_cell(
                    table,
                    item["position"],
                    row,
                    0
                )
                self.add_table_cell(
                    table,
                    item["type"],
                    row,
                    1
                )
                self.add_table_cell(
                    table,
                    item["change"],
                    row,
                    2
                )
                self.add_table_cell(
                    table,
                    item["impact"],
                    row,
                    3
                )
        else:
            no_mutation_text = (
                "No mutations detected"
                if reference == mutated
                else "Unsupported change pattern"
            )
            self.add_table_cell(
                table,
                no_mutation_text,
                1,
                0
            )

        ctk.CTkLabel(
            content,
            text="Sequence Difference",
            font=("Segoe UI", 18, "bold"),
            text_color=self.WHITE
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(0, 8)
        )

        difference_frame = ctk.CTkFrame(
            content,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        difference_frame.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )
        difference_frame.grid_columnconfigure(1, weight=1)

        reference_line, mutated_line = self.build_difference_lines(
            reference,
            mutated,
            mutations
        )

        ctk.CTkLabel(
            difference_frame,
            text="Reference:",
            font=("Consolas", 13),
            text_color=self.WHITE,
            anchor="e"
        ).grid(
            row=0,
            column=0,
            padx=(16, 8),
            pady=(14, 2),
            sticky="e"
        )

        ctk.CTkLabel(
            difference_frame,
            text=reference_line,
            font=("Consolas", 13),
            text_color=self.WHITE,
            anchor="w",
            justify="left"
        ).grid(
            row=0,
            column=1,
            padx=(0, 16),
            pady=(14, 2),
            sticky="w"
        )

        ctk.CTkLabel(
            difference_frame,
            text="Mutated:",
            font=("Consolas", 13),
            text_color=self.WHITE,
            anchor="e"
        ).grid(
            row=1,
            column=0,
            padx=(16, 8),
            pady=(2, 14),
            sticky="e"
        )

        ctk.CTkLabel(
            difference_frame,
            text=mutated_line,
            font=("Consolas", 13),
            text_color=self.WHITE,
            anchor="w",
            justify="left"
        ).grid(
            row=1,
            column=1,
            padx=(0, 16),
            pady=(2, 14),
            sticky="w"
        )

        ctk.CTkLabel(
            content,
            text="Full Analysis Report",
            font=("Segoe UI", 18, "bold"),
            text_color=self.WHITE
        ).grid(
            row=8,
            column=0,
            sticky="w",
            pady=(0, 8)
        )

        report_frame = ctk.CTkFrame(
            content,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        report_frame.grid(
            row=9,
            column=0,
            sticky="ew",
            pady=(0, 8)
        )
        report_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            report_frame,
            text=result,
            font=("Consolas", 12),
            text_color=self.WHITE,
            anchor="nw",
            justify="left",
            wraplength=760
        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=16,
            sticky="ew"
        )

    def import_txt(self, target):
        file_path = filedialog.askopenfilename(
            title="Import DNA TXT File",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if not file_path:
            return

        try:
            sequence = read_dna_from_file(file_path)

            if target == "reference":
                text_box = self.reference_text
                label = "Reference DNA"
            else:
                text_box = self.mutated_text
                label = "Mutated DNA"

            text_box.delete(
                "1.0",
                "end"
            )

            text_box.insert(
                "1.0",
                sequence
            )

            messagebox.showinfo(
                "Import Complete",
                f"{label} imported successfully."
            )

        except DNAFileError as error:
            messagebox.showerror(
                "Import Error",
                str(error)
            )

    def export_report(self):
        if self.export_options_visible:
            self.export_options_frame.grid_remove()
            self.export_options_visible = False
            return

        data = self.check_inputs()
        if not data:
            return

        self.export_options_frame.grid()
        self.export_options_visible = True

    def save_export(self, export_type):
        data = self.check_inputs()
        if not data:
            return

        reference, mutated = data

        try:
            report_data = self.collect_report_data(reference, mutated)

            if export_type == "summary":
                report = generate_summary_report(
                    reference,
                    mutated,
                    report_data["mutations"],
                    report_data["reference_stats"],
                    report_data["mutated_stats"],
                    report_data["impacts"],
                    report_data["supported"],
                )
                initial_file = "GeneGuard_Summary.txt"
                title = "Export GeneGuard Summary"
            else:
                report = generate_professional_report(
                    reference,
                    mutated,
                    report_data["mutations"],
                    report_data["reference_stats"],
                    report_data["mutated_stats"],
                    report_data["translation"],
                    report_data["impacts"],
                    report_data["supported"],
                )
                initial_file = "GeneGuard_Full_Report.txt"
                title = "Export GeneGuard Full Report"

        except Exception as error:
            messagebox.showerror(
                "Analysis Error",
                str(error)
            )
            return

        file_path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=".txt",
            initialfile=initial_file,
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(report)

            self.export_options_frame.grid_remove()
            self.export_options_visible = False

            messagebox.showinfo(
                "Export Complete",
                "Analysis exported successfully."
            )

        except PermissionError:
            messagebox.showerror(
                "Export Error",
                "You do not have permission to save in this location."
            )
        except OSError as error:
            messagebox.showerror(
                "Export Error",
                str(error)
            )

if __name__ == "__main__":
    app = GeneGuardApp()
    app.mainloop()