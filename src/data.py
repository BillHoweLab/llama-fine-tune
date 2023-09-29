#!/usr/bin/env python

import logging
import shutil
from functools import partial
from pathlib import Path
from uuid import uuid4

import typer
from datasets import load_dataset
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

###############################################################################

log = logging.getLogger(__name__)

###############################################################################

app = typer.Typer()

###############################################################################


def _convert_cdp_transcript_to_text_file(
    transcript_file: str | Path,
    output_dir: Path,
) -> Path:
    """
    Convert a CDP transcript file to a text file.

    Parameters
    ----------
    transcript_file: str | Path
        Path to the transcript file.
    output_dir: Path
        Path to the output directory.

    Returns
    -------
    output_file: Path
        Path to the output text file.
    """
    from cdp_backend.pipeline.transcript_model import Transcript

    # Convert transcript file to text file
    output_file = output_dir / f"{uuid4()}.txt"

    # Load transcript
    with open(transcript_file) as f:
        transcript = Transcript.from_json(f.read())

    # Rewrite as text file
    with open(output_file, "w") as f:
        f.write(" ".join([s.text for s in transcript.sentences]))

    return output_file


@app.command()
def preprocess_councils_in_action(
    sample_from_each_muni: float = 0.1,
) -> None:
    try:
        from cdp_data import CDPInstances
        from cdp_data import datasets as cdp_datasets
        from cdp_data.utils import connect_to_infrastructure
    except ImportError as e:
        raise ImportError(
            "To use this function, you need to install the `cdp-data` Python package."
        ) from e

    # Final dataset storage dir
    final_dataset_storage_dir = "councils-in-action-2023-06-01.huggingdata"

    # Create temp storage dir
    temp_storage_dir = Path(".temp-councils-in-action-dataset/")
    temp_storage_dir.mkdir(exist_ok=True)

    # List of good munis
    munis = [
        CDPInstances.Seattle,
        CDPInstances.KingCounty,
        CDPInstances.Missoula,
        CDPInstances.Denver,
        CDPInstances.Alameda,
        # CDPInstances.Boston,
        # CDPInstances.SanJose,
        # CDPInstances.MountainView,
        # CDPInstances.Milwaukee,
        # CDPInstances.LongBeach,
        # CDPInstances.Richmond,
        # CDPInstances.Louisville,
        # CDPInstances.Atlanta,
        # CDPInstances.Albuquerque,  # Albuquerque is hit or miss on data quality
        # CDPInstances.Oakland,  # Oakland is hit or miss on data quality
        # CDPInstances.Charlotte,  # Charlotte is hit or miss on data quality
        # CDPInstances.Portland,  # Portland is hit or miss on data quality
    ]

    # Create partial function for converting transcripts to text files
    convert_cdp_transcript_to_text_file = partial(
        _convert_cdp_transcript_to_text_file,
        output_dir=temp_storage_dir,
    )

    # Wrap the whole process in a directory cleaning process
    try:
        # For each muni
        # 1. connect to the infrastructure
        # 2. get the dataset
        # 3. store each transcript to single text file in parallel
        all_text_files = []
        for muni in tqdm(munis, desc="Processing each municipality"):
            # Connect to the infrastructure
            connect_to_infrastructure(infrastructure_slug=muni)

            # Get the dataset
            ds = cdp_datasets.get_session_dataset(
                infrastructure_slug=muni,
                start_datetime="2020-01-01",
                end_datetime="2023-06-01",
                sample=sample_from_each_muni,
                store_transcript=True,
                raise_on_error=False,
                tqdm_kws={"leave": False},
            )

            # Process each transcript
            all_text_files.extend(
                process_map(
                    convert_cdp_transcript_to_text_file,
                    ds.transcript_path,
                    desc="Dumping transcripts to text files",
                    leave=False,
                )
            )

        # Create new dataset from text files
        cia_dataset = load_dataset(
            "text",
            data_files=[str(f) for f in all_text_files],
            split="train",
            cache_dir=temp_storage_dir,
        )

        # Store to disk
        cia_dataset.save_to_disk(final_dataset_storage_dir)

    # Clean up temp storage dir
    finally:
        shutil.rmtree(temp_storage_dir)

    print(f"Full dataset stored to '{final_dataset_storage_dir}'.")


@app.command()
def upload(dataset_path: str, storage_uri: str) -> None:
    pass


@app.command()
def download(uri: str) -> None:
    pass


if __name__ == "__main__":
    app()
