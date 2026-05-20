"""Open Shop Quote (OSQ) — main desktop launcher window."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

_ORANGE = "#E87722"
_INNER_BG = "#1c1c1c"
_SUBTITLE_GRAY = "#b8b8b8"
_MUTED_GRAY = "#888888"
_BORDER_SUBTLE = "#3d3d3d"
_DISABLED_BTN = "#4a4a4a"

_STEP_FILTER = "STEP files (*.step *.stp);;All files (*.*)"


def pick_step_file_qt() -> str | None:
    """Native Windows file dialog via Qt (reliable with CustomTkinter)."""
    from PySide6.QtWidgets import QApplication, QFileDialog

    app = QApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QApplication([])

    path, _selected = QFileDialog.getOpenFileName(
        None,
        "Select STEP file",
        str(Path.home()),
        _STEP_FILTER,
    )
    if owns_app:
        app.quit()

    return path if path else None


class LauncherApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Open Shop Quote")
        self.geometry("700x480")
        self.resizable(False, False)
        self.configure(fg_color=_ORANGE)

        self._selected_path: str | None = None
        self._busy = False

        inner = ctk.CTkFrame(self, fg_color=_INNER_BG, corner_radius=0)
        inner.pack(fill="both", expand=True, padx=6, pady=6)

        self._build_header(inner)
        self._build_welcome(inner)
        self._build_step_load_area(inner)
        self._build_bottom_bar(inner)

    def _build_header(self, parent: ctk.CTkFrame) -> None:
        header = ctk.CTkFrame(parent, fg_color=_ORANGE, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Open Shop Quote",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff",
        ).pack(pady=(16, 0))

        ctk.CTkLabel(
            header,
            text="Precision Quoting for the American Machine Shop",
            font=ctk.CTkFont(size=13),
            text_color=_SUBTITLE_GRAY,
        ).pack(pady=(2, 0))

    def _build_welcome(self, parent: ctk.CTkFrame) -> None:
        welcome = ctk.CTkFrame(parent, fg_color="transparent")
        welcome.pack(fill="x", pady=(18, 8), padx=24)

        ctk.CTkLabel(
            welcome,
            text="Welcome Back, Logan",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        ).pack()

        ctk.CTkFrame(welcome, fg_color=_BORDER_SUBTLE, height=1, corner_radius=0).pack(
            fill="x", pady=(14, 0)
        )

    def _build_step_load_area(self, parent: ctk.CTkFrame) -> None:
        center = ctk.CTkFrame(parent, fg_color="transparent")
        center.pack(fill="both", expand=True, padx=24, pady=8)

        load_box = ctk.CTkFrame(
            center,
            fg_color="#252525",
            corner_radius=12,
            border_width=2,
            border_color=_BORDER_SUBTLE,
        )
        load_box.pack(expand=True, pady=16)

        ctk.CTkLabel(
            load_box,
            text="📂 Load a STEP File to Begin",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
        ).pack(pady=(28, 16), padx=32)

        self.browse_btn = ctk.CTkButton(
            load_box,
            text="Browse for STEP File",
            width=360,
            height=56,
            corner_radius=10,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=_ORANGE,
            hover_color="#cf6619",
            command=self._browse_step_file,
        )
        self.browse_btn.pack(pady=(0, 14))

        self.file_label = ctk.CTkLabel(
            load_box,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color=_MUTED_GRAY,
            wraplength=400,
        )
        self.file_label.pack(pady=(0, 28))

    def _build_bottom_bar(self, parent: ctk.CTkFrame) -> None:
        bottom = ctk.CTkFrame(parent, fg_color="transparent", height=64)
        bottom.pack(side="bottom", fill="x", padx=20, pady=(0, 14))
        bottom.pack_propagate(False)

        self.analyze_btn = ctk.CTkButton(
            bottom,
            text="Analyze Part →",
            width=200,
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=_DISABLED_BTN,
            hover_color=_DISABLED_BTN,
            text_color="#aaaaaa",
            state="disabled",
            command=self._on_analyze,
        )
        self.analyze_btn.pack(side="right", pady=8)

    def _set_selected_file(self, path: str) -> None:
        self._selected_path = path
        self.file_label.configure(text=Path(path).name, text_color="#ffffff")
        self.analyze_btn.configure(
            state="normal",
            fg_color=_ORANGE,
            hover_color="#cf6619",
            text_color="#ffffff",
        )

    def _browse_step_file(self) -> None:
        if self._busy:
            return
        self._busy = True
        self.browse_btn.configure(state="disabled", text="Choose a file…")
        self.update_idletasks()

        try:
            path = pick_step_file_qt()
        except Exception as exc:
            messagebox.showerror(
                "Open Shop Quote",
                f"Could not open file chooser:\n{exc}\n\n"
                "Ensure conda env quotetool is active and PySide6 is installed.",
                parent=self,
            )
            return
        finally:
            self._busy = False
            self.browse_btn.configure(state="normal", text="Browse for STEP File")

        if not path:
            return

        if not Path(path).is_file():
            messagebox.showerror(
                "Open Shop Quote",
                f"File not found:\n{path}",
                parent=self,
            )
            return

        self._set_selected_file(path)
        self._open_viewer(path)

    def _on_analyze(self) -> None:
        if self._selected_path:
            self._open_viewer(self._selected_path)

    def _open_viewer(self, path: str) -> None:
        step = Path(path)
        if not step.is_file():
            messagebox.showerror("Open Shop Quote", f"File not found:\n{path}", parent=self)
            return

        self.file_label.configure(text=f"{step.name} — opening 3D view…")
        self.update_idletasks()

        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            subprocess.Popen(
                [sys.executable, "-m", "src.viewer_app", str(step)],
                cwd=str(_ROOT),
                creationflags=creationflags,
            )
        except Exception as exc:
            messagebox.showerror(
                "Open Shop Quote",
                f"Could not start 3D viewer:\n{exc}",
                parent=self,
            )
            return

        self.destroy()


if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
