"""
Online LaTeX to PDF converter with multiple fallback services
"""
import requests
import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Conversion services in priority order
CONVERSION_SERVICES = [
    {
        "name": "YtoTech LaTeX",
        "url": "https://latex.ytotech.com/builds/sync",
        "method": "multipart",
    },
    {
        "name": "LaTeX.Online",
        "url": "https://latexonline.cc/compile",
        "method": "query_text",
    },
]


def _try_ytotech(latex_content: str, timeout: int) -> bytes | None:
    """Try YtoTech LaTeX build service"""
    payload = {
        "compiler": "pdflatex",
        "resources": [
            {
                "main": True,
                "content": latex_content,
            }
        ],
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        CONVERSION_SERVICES[0]["url"],
        data=json.dumps(payload),
        headers=headers,
        timeout=timeout,
    )
    if resp.status_code in (200, 201) and resp.headers.get("Content-Type", "").startswith("application/pdf"):
        return resp.content
    # Also try multipart form
    files = {"file": ("document.tex", latex_content, "text/plain")}
    resp = requests.post(CONVERSION_SERVICES[0]["url"], files=files, timeout=timeout)
    if resp.status_code in (200, 201) and len(resp.content) > 100:
        return resp.content
    return None


def _try_latexonline(latex_content: str, timeout: int) -> bytes | None:
    """Try LaTeX.Online compile service"""
    resp = requests.post(
        CONVERSION_SERVICES[1]["url"],
        data={"text": latex_content},
        timeout=timeout,
    )
    if resp.status_code == 200 and len(resp.content) > 100:
        return resp.content
    return None


def convert_latex_to_pdf_online(latex_file_path, output_dir="./output"):
    """
    Convert LaTeX file to PDF using online services with fallback
    """
    try:
        with open(latex_file_path, "r", encoding="utf-8") as f:
            latex_content = f.read()

        os.makedirs(output_dir, exist_ok=True)
        pdf_filename = Path(latex_file_path).stem + ".pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)

        timeout = 60  # generous timeout

        # Try each service in order
        converters = [
            ("YtoTech LaTeX", _try_ytotech),
            ("LaTeX.Online", _try_latexonline),
        ]

        for name, converter_fn in converters:
            try:
                logger.info(f"Trying PDF conversion with {name}...")
                pdf_bytes = converter_fn(latex_content, timeout)
                if pdf_bytes and len(pdf_bytes) > 100:
                    with open(pdf_path, "wb") as f:
                        f.write(pdf_bytes)
                    logger.info(f"PDF generated via {name}: {pdf_path}")
                    print(f"PDF generated via {name}: {pdf_path}")
                    return pdf_path
                else:
                    logger.warning(f"{name} returned empty or invalid response")
            except requests.Timeout:
                logger.warning(f"{name} timed out after {timeout}s")
            except Exception as e:
                logger.warning(f"{name} failed: {e}")

        logger.error("All online PDF conversion services failed")
        print("PDF conversion failed: all services unavailable. The .tex file was saved successfully.")
        return None

    except Exception as e:
        logger.error(f"Error converting to PDF: {e}")
        print(f"Error converting to PDF: {str(e)}")
        return None


def batch_convert_latex_files(output_dir="./output"):
    """
    Convert all LaTeX files in output directory to PDF
    """
    latex_files = list(Path(output_dir).glob("*.tex"))

    if not latex_files:
        print("No LaTeX files found in output directory")
        return

    print(f"Found {len(latex_files)} LaTeX files to convert...")

    for latex_file in latex_files:
        print(f"Converting {latex_file.name}...")
        convert_latex_to_pdf_online(str(latex_file), output_dir)


if __name__ == "__main__":
    batch_convert_latex_files()
