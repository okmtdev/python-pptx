"""pptx → pdf 変換のヘルパー.

LibreOffice の headless モード (`soffice --headless --convert-to pdf`) を呼び出して
pptx を pdf に変換する。LibreOffice は別途インストールが必要:

    # macOS
    brew install --cask libreoffice
    # Ubuntu / Debian
    sudo apt-get install libreoffice
    # Windows
    https://www.libreoffice.org/download/ から導入

Microsoft PowerPoint をインストール済みなら、PowerPoint 経由でも変換できるが、
クロスプラットフォームで一番楽なのは LibreOffice 経由なのでこれを採用する。
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def convert_to_pdf(pptx_path: str | Path, *, out_dir: str | Path | None = None) -> Path:
    """指定された .pptx を .pdf に変換し、生成された pdf のパスを返す.

    Args:
        pptx_path: 変換元の .pptx ファイル。
        out_dir: pdf の出力先ディレクトリ。省略時は pptx と同じ場所。

    Returns:
        生成された .pdf のパス。
    """
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        raise FileNotFoundError(pptx_path)

    out_dir = Path(out_dir).resolve() if out_dir else pptx_path.parent

    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError(
            "LibreOffice (soffice) が見つからない。インストールして PATH を通すこと。"
        )

    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(pptx_path)],
        check=True,
        capture_output=True,
    )
    pdf_path = out_dir / f"{pptx_path.stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"PDF generation failed: expected {pdf_path}")
    return pdf_path
