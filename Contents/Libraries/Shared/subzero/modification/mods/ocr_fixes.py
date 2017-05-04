# coding=utf-8
import logging

from subzero.modification.mods import SubtitleTextModification
from subzero.modification.processors.string_processor import MultipleLineProcessor
from subzero.modification.processors.re_processor import MultipleWordReProcessor
from subzero.modification import registry
from subzero.modification.dictionaries.data import data as OCR_fix_data

logger = logging.getLogger(__name__)


class FixOCR(SubtitleTextModification):
    identifier = "OCR_fixes"
    description = "Fix common OCR issues"
    exclusive = True
    data_dict = None

    def __init__(self, parent):
        super(FixOCR, self).__init__(parent)
        data_dict = OCR_fix_data.get(parent.language.alpha3t)
        if not data_dict:
            logger.debug("No SnR-data available for language %s", parent.language)
            return

        self.data_dict = data_dict
        self.processors = self.get_processors()

    def get_processors(self):
        if not self.data_dict:
            return []

        return [
            MultipleLineProcessor(self.data_dict["WholeLines"], name="SE_replace_line"),
            MultipleWordReProcessor(self.data_dict["WholeWords"], name="SE_replace_word"),
            MultipleWordReProcessor(self.data_dict["BeginLines"], name="SE_replace_beginline"),
            MultipleWordReProcessor(self.data_dict["EndLines"], name="SE_replace_endline"),
            MultipleLineProcessor(self.data_dict["PartialLines"], name="SE_replace_partialline"),
            MultipleLineProcessor(self.data_dict["PartialWordsAlways"], name="SE_replace_partialwordsalways")
        ]


registry.register(FixOCR)