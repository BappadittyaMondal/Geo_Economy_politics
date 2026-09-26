"""
Headless PDF Compiler (Phase 72).
Compiles HTML dashboards and executive reports into publication-grade PDFs
via local headless Chromium / Microsoft Edge instances without heavy external libraries.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple


class PDFCompiler:
    """Invokes local headless browser to compile HTML documents to vector PDF."""

    WINDOWS_BROWSER_PATHS = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]

    LINUX_BROWSER_NAMES = [
        "chromium-browser",
        "chromium",
        "google-chrome-stable",
        "google-chrome",
        "edge",
        "microsoft-edge"
    ]

    @classmethod
    def find_browser_executable(cls) -> Optional[str]:
        """Discovers headless-capable browser binary on local operating system."""
        # 1. Check known Windows paths if on Windows
        if sys.platform == "win32":
            for p in cls.WINDOWS_BROWSER_PATHS:
                if os.path.isfile(p):
                    return p

        # 2. Check PATH environment variable
        search_names = ["msedge", "chrome", "google-chrome", "chromium"] + cls.LINUX_BROWSER_NAMES
        for name in search_names:
            found = shutil.which(name)
            if found:
                return found

        return None

    @classmethod
    def compile_pdf(
        cls,
        html_content: str,
        output_pdf_path: str,
        timeout_seconds: int = 30
    ) -> Tuple[bool, str]:
        """
        Renders HTML string into a PDF file at output_pdf_path.
        Returns: (success: bool, output_path_or_error_message: str)
        """
        browser_exe = cls.find_browser_executable()
        if not browser_exe:
            return False, "Headless browser (Edge/Chrome/Chromium) not detected on host system."

        out_path = Path(output_pdf_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Write HTML to temporary file
        temp_dir = tempfile.mkdtemp(prefix="geo_pdf_")
        temp_html = Path(temp_dir) / "source.html"
        try:
            temp_html.write_text(html_content, encoding="utf-8")

            cmd = [
                browser_exe,
                "--headless=new",
                "--no-pdf-header-footer",
                "--run-all-compositor-stages-before-draw",
                f"--print-to-pdf={str(out_path)}",
                str(temp_html)
            ]

            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False
            )

            if out_path.is_file() and out_path.stat().st_size > 1000:
                return True, str(out_path)
            else:
                err_msg = res.stderr or res.stdout or f"Process exited with code {res.returncode}"
                return False, f"PDF compilation failed: {err_msg}"
        except Exception as ex:
            return False, f"PDF compilation exception: {str(ex)}"
        finally:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
