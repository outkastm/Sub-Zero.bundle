# coding=utf-8
import re
import logging

from subzero.modification.processors.re_processor import ReProcessor, NReProcessor

logger = logging.getLogger(__name__)


class SubtitleModification(object):
    identifier = None
    description = None
    long_description = None
    exclusive = False
    advanced = False  # has parameters
    modifies_whole_file = False  # operates on the whole file, not individual entries
    pre_processors = []
    processors = []
    post_processors = []

    def __init__(self, parent):
        return

    def _process(self, content, processors, debug=False, parent=None, **kwargs):
        if not content:
            return

        # processors may be a list or a callable
        #if callable(processors):
        #    _processors = processors()
        #else:
        #    _processors = processors
        _processors = processors

        new_content = content
        for processor in _processors:
            old_content = new_content
            new_content = processor.process(new_content, debug=debug)
            if not new_content:
                if debug:
                    logger.debug("Processor returned empty line: %s", processor)
                break
            if debug:
                if old_content == new_content:
                    continue
                logger.debug("%s: %s -> %s", processor, old_content, new_content)
        return new_content

    def pre_process(self, content, debug=False, parent=None, **kwargs):
        return self._process(content, self.pre_processors, debug=debug, parent=parent, **kwargs)

    def process(self, content, debug=False, parent=None, **kwargs):
        return self._process(content, self.processors, debug=debug, parent=parent, **kwargs)

    def post_process(self, content, debug=False, parent=None, **kwargs):
        return self._process(content, self.post_processors, debug=debug, parent=parent, **kwargs)

    def modify(self, content, debug=False, parent=None, **kwargs):
        new_content = content
        for method in ("pre_process", "process", "post_process"):
            new_content = getattr(self, method)(new_content, debug=debug, parent=parent, **kwargs)

        return new_content

    @classmethod
    def get_signature(cls, **kwargs):
        string_args = ",".join(["%s=%s" % (key, value) for key, value in kwargs.iteritems()])
        return "%s(%s)" % (cls.identifier, string_args)


class SubtitleTextModification(SubtitleModification):
    post_processors = [
        # empty tag
        ReProcessor(re.compile(r'({\\\w+1})[\s.,-_!?]+({\\\w+0})'), "", name="empty_tag"),

        # empty line (needed?)
        NReProcessor(re.compile(r'^\s+$'), "", name="empty_line"),

        # empty dash line (needed?)
        NReProcessor(re.compile(r'(^[\s]*[\-]+[\s]*)$'), "", name="empty_dash_line"),

        # clean whitespace at start and end
        ReProcessor(re.compile(r'^\s*([^\s]+)\s*$'), r"\1", name="surrounding_whitespace"),
    ]
