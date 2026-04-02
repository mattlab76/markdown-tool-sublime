import sublime
import sublime_plugin
import re


class EdiFormatTableCommand(sublime_plugin.TextCommand):
    """Finds the Markdown table under the cursor and aligns all columns."""

    def run(self, edit):
        cursor = self.view.sel()[0].begin()
        table_region = self._find_table_region(cursor)

        if table_region is None:
            sublime.status_message("EDI Markdown: Keine Tabelle unter dem Cursor gefunden")
            return

        original = self.view.substr(table_region)
        formatted = self._format_table(original)

        if formatted != original:
            self.view.replace(edit, table_region, formatted)
            sublime.status_message("EDI Markdown: Tabelle formatiert")
        else:
            sublime.status_message("EDI Markdown: Tabelle bereits ausgerichtet")

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")

    # ------------------------------------------------------------------

    def _find_table_region(self, cursor):
        """Expand from cursor line upward/downward to find contiguous table lines."""
        row, _ = self.view.rowcol(cursor)
        total = self.view.rowcol(self.view.size())[0]

        # Check current line is a table line
        if not self._is_table_line(self._line_text(row)):
            return None

        # Expand upward
        start_row = row
        while start_row > 0 and self._is_table_line(self._line_text(start_row - 1)):
            start_row -= 1

        # Expand downward
        end_row = row
        while end_row < total and self._is_table_line(self._line_text(end_row + 1)):
            end_row += 1

        start_pt = self.view.text_point(start_row, 0)
        end_pt = self.view.line(self.view.text_point(end_row, 0)).end()

        return sublime.Region(start_pt, end_pt)

    def _line_text(self, row):
        point = self.view.text_point(row, 0)
        return self.view.substr(self.view.line(point))

    @staticmethod
    def _is_table_line(line):
        stripped = line.strip()
        return stripped.startswith("|") and stripped.endswith("|")

    @staticmethod
    def _format_table(text):
        lines = text.split("\n")
        parsed = []
        separator_indices = []

        for i, line in enumerate(lines):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            parsed.append(cells)
            # Detect separator lines like |---|---|
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                separator_indices.append(i)

        if not parsed:
            return text

        # Determine max width per column
        num_cols = max(len(row) for row in parsed)
        col_widths = [0] * num_cols
        for row_idx, cells in enumerate(parsed):
            if row_idx in separator_indices:
                continue
            for col_idx, cell in enumerate(cells):
                col_widths[col_idx] = max(col_widths[col_idx], len(cell))

        # Ensure minimum width of 3 for separator dashes
        col_widths = [max(w, 3) for w in col_widths]

        # Rebuild lines
        result = []
        for row_idx, cells in enumerate(parsed):
            # Pad cells to num_cols
            cells = cells + [""] * (num_cols - len(cells))

            if row_idx in separator_indices:
                # Rebuild separator, preserving alignment colons
                sep_cells = []
                for col_idx, cell in enumerate(cells):
                    left = cell.startswith(":")
                    right = cell.endswith(":")
                    inner = col_widths[col_idx] - (1 if left else 0) - (1 if right else 0)
                    sep = (":" if left else "") + "-" * inner + (":" if right else "")
                    sep_cells.append(sep)
                result.append("| " + " | ".join(sep_cells) + " |")
            else:
                padded = [cell.ljust(col_widths[col_idx]) for col_idx, cell in enumerate(cells)]
                result.append("| " + " | ".join(padded) + " |")

        return "\n".join(result)
