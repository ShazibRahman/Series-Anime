import io
import os
import pickle
import pathlib
import logging

from decorator_utils import singleton_with_no_parameters

from .pickle_utility import (
    get_picked_series_data,
)
from .general_util import clean_not_existing_series_data_from_image_mapping

logger = logging.getLogger(__name__)


@singleton_with_no_parameters
class SeriesToImageMapping:
    """
    Fully encapsulates the series-to-image mapping pickle.
    Handles internal file path, cache, load, save, and cleaning.
    """

    def __init__(self):
        print("Initializing SeriesToImageMapping...")
        self._data_dir = pathlib.Path(__file__).parent.parent / "data"
        self._data_dir.mkdir(exist_ok=True)  # create if missing
        self._file = self._data_dir / "series_to_image_mapping.pickle"
        if not self._file.exists():
            self._file.touch()

        self._data: dict[str, str] | None = None  # lazy load

    def get_mapping(self) -> dict:
        """
        Retrieve the series-to-image mapping (cached in memory).
        Automatically cleans entries that no longer exist in series data.
        """
        if self._data is not None:
            return self._data

        try:
            with io.open(self._file, "rb") as f:
                self._data = pickle.load(f)
                # Clean any stale entries
                keys_to_be_deleted = clean_not_existing_series_data_from_image_mapping(
                    self._data, get_picked_series_data()
                )
                self.__delete_removed_image_mapping(keys_to_be_deleted)
        except Exception as e:
            logger.error("Failed to load series-to-image mapping: %s" % e)
            self._data = {}

        logger.debug("loaded mapping with %s entries", len(self._data))
        return self._data

    def save_mapping(self):
        """
        Save the series-to-image mapping to disk.
        Persists whatever is currently in self._data.
        """

        logger.debug(
            "Saving series-to-image mapping with %d entries",
            len(self._data) if self._data else 0,
        )
        if self._data is None or len(self._data) == 0:
            logger.warning("No data to save, skipping.")
            return

        try:
            with io.open(self._file, "wb") as f:
                pickle.dump(self._data, f)
        except Exception as e:
            logger.error("Failed to save series-to-image mapping: %s" % e)

    def __delete_removed_image_mapping(self, keys_to_be_deleted: list[str]):
        """Delete removed image mappings from the internal data."""
        if self._data is None:
            return

        for key in keys_to_be_deleted:
            if key in self._data:
                image_path = self._data[key]
                logger.debug("deleting", key, "->", image_path)

                # Only delete if image_path is a valid str or Path
                if isinstance(image_path, (str, bytes, os.PathLike)):
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    except Exception as e:
                        logger.debug(f"Failed to delete {image_path}: {e}")

                del self._data[key]
