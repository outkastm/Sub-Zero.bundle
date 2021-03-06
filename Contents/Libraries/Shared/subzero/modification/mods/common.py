# coding=utf-8

import re

from subzero.modification.mods import SubtitleTextModification, empty_line_post_processors
from subzero.modification.processors.string_processor import StringProcessor
from subzero.modification.processors.re_processor import NReProcessor
from subzero.modification import registry


class CommonFixes(SubtitleTextModification):
    identifier = "common"
    description = "Basic common fixes"
    exclusive = True
    order = 40

    long_description = """\
    Fix common whitespace/punctuation issues in subtitles
    """

    processors = [
        # -- = ...
        StringProcessor("-- ", '... ', name="CM_doubledash"),

        # '' = "
        StringProcessor("''", '"', name="CM_double_apostrophe"),

        # remove leading ...
        NReProcessor(re.compile(r'(?u)^\.\.\.[\s]*'), "", name="CM_leading_ellipsis"),

        # no space after ellipsis
        NReProcessor(re.compile(r'(?u)\.\.\.(?![\s.,!?\'"])(?!$)'), "... ", name="CM_ellipsis_no_space"),

        # multiple spaces
        NReProcessor(re.compile(r'(?u)[\s]{2,}'), " ", name="CM_multiple_spaces"),

        # no space after starting dash
        NReProcessor(re.compile(r'(?u)^-(?![\s-])'), "- ", name="CM_dash_space"),

        # remove starting spaced dots (not matching ellipses
        NReProcessor(re.compile(r'(?u)^(?!\s?(\.\s\.\s\.)|(\s?\.{3}))[\s.]*'), "", name="CM_starting_spacedots"),

        # space missing before doublequote
        # ReProcessor(re.compile(r'(?u)(?<!^)(?<![\s(\["])("[^"]+")'), r' \1', name="CM_space_before_dblquote"),

        # space missing after doublequote
        # ReProcessor(re.compile(r'(?u)("[^"\s][^"]+")([^\s.,!?)\]]+)'), r"\1 \2", name="CM_space_after_dblquote"),

        # space before ending doublequote?

        # remove >>
        NReProcessor(re.compile(r'(?u)^\s?>>\s*'), "", name="CM_leading_crocodiles"),

        # replace uppercase I with lowercase L in words
        NReProcessor(re.compile(ur'(?u)([A-zÀ-ž][a-zà-ž]+)(I+)'),
                     lambda match: ur'%s%s' % (match.group(1), "l" * len(match.group(2))),
                     name="CM_uppercase_i_in_word"),

        # fix spaces in numbers (allows for punctuation: ,.:' (comma/dot only fixed if after space, those may be
        # countdowns otherwise); don't break up ellipses
        # fixme: maybe check whether it's a countdown (second part smaller than the first), otherwise handle default?
        NReProcessor(
            re.compile(r'(?u)([0-9]+[0-9:\']*(?<!\.\.)\s+(?!\.\.)[0-9,.:\']*(?=[0-9]+)[0-9,.:\'\s]+)(?=\s|$)'),
            lambda match: match.group(1).replace(" ", ""),
            name="CM_spaces_in_numbers"),

        # uppercase after dot
        NReProcessor(re.compile(ur'(?u)((?:[^.\s])+\.\s+)([a-zà-ž])'),
                     lambda match: ur'%s%s' % (match.group(1), match.group(2).upper()), name="CM_uppercase_after_dot"),

        # remove spaces before punctuation
        NReProcessor(re.compile(r'(?u)(?:(?<=^)|(?<=\w)) +([!?.,](?![!?.,]))'), r"\1", name="CM_punctuation_space"),
    ]

    post_processors = empty_line_post_processors


registry.register(CommonFixes)
