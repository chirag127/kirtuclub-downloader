"""``kirtuclub`` — unified CLI for the download → PDF → OCR → merge pipeline.

Subcommands:
  download   fetch page images for an episode range
  topdf      assemble downloaded images into per-episode PDFs
  ocr        add a searchable text layer to scanned PDFs
  merge      combine per-episode PDFs into one file
  pipeline   run download → topdf → ocr → merge end to end
"""

from __future__ import annotations

import os

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import __version__, pipeline
from .config import Config
from .http import Downloader

console = Console()


def _config(**overrides: object) -> Config:
    base = Config()
    fields = {k: v for k, v in overrides.items() if v is not None}
    return Config(**{**base.__dict__, **fields})


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="kirtuclub")
def cli() -> None:
    """Download, convert, OCR, and merge comic PDFs — one pipeline."""


series_opt = click.option("--series", default=None, help="Series slug.")
range_opt = click.option(
    "--episodes", nargs=2, type=int, default=None,
    metavar="START END", help="Inclusive episode range.",
)
content_opt = click.option(
    "--content-dir", default=None, help="Base output directory."
)


@cli.command()
@series_opt
@range_opt
@content_opt
@click.option("--base-url", default=None, help="Image base URL.")
def download(series, episodes, content_dir, base_url):  # noqa: ANN001
    """Fetch page images for an episode range."""
    cfg = _config(series=series, content_dir=content_dir, base_url=base_url)
    start, end = episodes or (1, 200)
    total = 0
    with Downloader(cfg) as dl, Progress(
        SpinnerColumn(), TextColumn("{task.description}"), console=console
    ) as prog:
        task = prog.add_task("Downloading…", total=None)
        for ep in range(start, end + 1):
            saved = pipeline.download_episode(dl, cfg, ep)
            if not saved:
                continue
            total += len(saved)
            prog.update(task, description=f"ep {ep}: {len(saved)} pages")
    console.print(f"[green]Downloaded {total} page images.[/green]")


@cli.command()
@series_opt
@content_opt
def topdf(series, content_dir):  # noqa: ANN001
    """Assemble downloaded images into per-episode PDFs."""
    cfg = _config(series=series, content_dir=content_dir)
    images_root = os.path.join(cfg.content_dir, cfg.series, "images")
    made = 0
    if not os.path.isdir(images_root):
        console.print(f"[yellow]No images at {images_root}[/yellow]")
        return
    for ep_dir in sorted(
        d.path for d in os.scandir(images_root) if d.is_dir()
    ):
        images = sorted(
            os.path.join(ep_dir, f)
            for f in os.listdir(ep_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        )
        out = os.path.join(
            cfg.content_dir, cfg.series, os.path.basename(ep_dir) + ".pdf"
        )
        if pipeline.images_to_pdf(images, out):
            made += 1
    console.print(f"[green]Built {made} episode PDFs.[/green]")


@cli.command()
@content_opt
@click.option("--root", default=None, help="Root dir to scan for PDFs.")
@click.option("--force", is_flag=True, help="OCR even if text is present.")
def ocr(content_dir, root, force):  # noqa: ANN001
    """Add a searchable text layer to scanned PDFs."""
    cfg = _config(content_dir=content_dir)
    scan_root = root or cfg.content_dir
    done = 0
    for pdf in pipeline.find_pdfs(scan_root):
        if force or pipeline.needs_ocr(pdf, cfg):
            if pipeline.run_ocr(pdf, cfg):
                done += 1
    console.print(f"[green]OCR complete on {done} PDFs.[/green]")


@cli.command()
@content_opt
@click.option("--root", default=None, help="Root dir of per-episode PDFs.")
@click.option("--out", "out_path", default=None, help="Merged output path.")
def merge(content_dir, root, out_path):  # noqa: ANN001
    """Combine per-episode PDFs into one file."""
    cfg = _config(content_dir=content_dir)
    scan_root = root or os.path.join(cfg.content_dir, cfg.series)
    pdfs = [
        p for p in pipeline.find_pdfs(scan_root)
        if "all_in_one" not in p
    ]
    dest = out_path or os.path.join(scan_root, "all_in_one.pdf")
    if pipeline.merge_pdfs(pdfs, dest, cfg):
        console.print(f"[green]Merged {len(pdfs)} PDFs → {dest}[/green]")
    else:
        console.print("[yellow]Merge skipped (empty or over size cap).[/yellow]")


@cli.command()
@series_opt
@range_opt
@content_opt
@click.option("--skip-ocr", is_flag=True, help="Skip the OCR stage.")
@click.pass_context
def pipeline_cmd(ctx, series, episodes, content_dir, skip_ocr):  # noqa: ANN001
    """Run download → topdf → ocr → merge end to end."""
    ctx.invoke(download, series=series, episodes=episodes,
               content_dir=content_dir, base_url=None)
    ctx.invoke(topdf, series=series, content_dir=content_dir)
    if not skip_ocr:
        ctx.invoke(ocr, content_dir=content_dir, root=None, force=False)
    ctx.invoke(merge, content_dir=content_dir, root=None, out_path=None)


cli.add_command(pipeline_cmd, name="pipeline")


if __name__ == "__main__":
    cli()
