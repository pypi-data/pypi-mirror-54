""" Definitions for Grammar """
import logging

from .segments_base import (BaseSegment, check_still_complete, parse_match_logging)
from .match import MatchResult, join_segments_raw_curtailed
from ..errors import SQLParseError
from ..helpers import get_time


class BaseGrammar(object):
    """ Grammars are a way of composing match statements, any grammar
    must implment the `match` function. Segments can also be passed to
    most grammars. Segments implement `match` as a classmethod. Grammars
    implement it as an instance method """
    v_level = 3

    def __init__(self, *args, **kwargs):
        """ Deal with kwargs common to all grammars """
        # We provide a common interface for any grammar that allows positional elements
        self._elements = args
        # Now we deal with the standard kwargs
        for var, default in [('code_only', True), ('optional', False)]:
            setattr(self, var, kwargs.pop(var, default))
        # optional, only really makes sense in the context of a sequence.
        # If a grammar is optional, then a sequence can continue without it.
        if kwargs:
            raise ValueError("Unconsumed kwargs is creation of grammar: {0}\nExcess: {1}".format(
                self.__class__.__name__,
                kwargs
            ))

    def is_optional(self):
        # The optional attribute is set in the __init__ method
        return self.optional

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        """
            Matching can be done from either the raw or the segments.
            This raw function can be overridden, or a grammar defined
            on the underlying class.
        """
        raise NotImplementedError("{0} has no match function implemented".format(self.__class__.__name__))

    def _match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        """ A wrapper on the match function to do some basic validation """
        t0 = get_time()

        if isinstance(segments, BaseSegment):
            segments = segments,  # Make into a tuple for compatability
        if not isinstance(segments, tuple):
            logging.warning(
                "{0}.match, was passed {1} rather than tuple or segment".format(
                    self.__class__.__name__, type(segments)))
            if isinstance(segments, list):
                # Let's make it a tuple for compatibility
                segments = tuple(segments)

        if len(segments) == 0:
            logging.info("{0}.match, was passed zero length segments list. NB: {0} contains {1!r}".format(
                self.__class__.__name__, self._elements))

        # Work out the raw representation and curtail if long
        parse_match_logging(
            parse_depth, match_depth, match_segment, self.__class__.__name__,
            '_match', 'IN', verbosity=verbosity, v_level=self.v_level,
            le=len(self._elements), ls=len(segments),
            seg=join_segments_raw_curtailed(segments))

        m = self.match(segments, match_depth=match_depth, parse_depth=parse_depth,
                       verbosity=verbosity, dialect=dialect, match_segment=match_segment)

        if not isinstance(m, MatchResult):
            logging.warning(
                "{0}.match, returned {1} rather than MatchResult".format(
                    self.__class__.__name__, type(m)))

        dt = get_time() - t0
        if m.is_complete():
            msg = 'OUT ++'
        elif m:
            msg = 'OUT -'
        else:
            msg = 'OUT'

        parse_match_logging(
            parse_depth, match_depth, match_segment, self.__class__.__name__,
            '_match', msg, verbosity=verbosity, v_level=self.v_level, dt=dt, m=m)

        # Basic Validation
        check_still_complete(segments, m.matched_segments, m.unmatched_segments)
        return m

    def expected_string(self, dialect=None, called_from=None):
        """ Return a String which is helpful to understand what this grammar expects """
        raise NotImplementedError(
            "{0} does not implement expected_string!".format(
                self.__class__.__name__))

    @staticmethod
    def bracket_sensitive_forward_match(segments, start_bracket, end_bracket,
                                        match_depth, parse_depth, verbosity,
                                        terminator=None, target=None, dialect=None,
                                        match_segment=None):
        sub_bracket_count = 0
        unmatched_segs = segments
        matched_segs = tuple()
        current_bracket_segment = None

        while True:
            # Are we at the end of the sequence?
            if len(unmatched_segs) == 0:
                # Yes we're at the end

                # Are we in a bracket counting cycle that hasn't finished yet?
                if sub_bracket_count > 0:
                    # TODO: Format this better
                    raise SQLParseError(
                        "Couldn't find closing bracket for opening bracket.",
                        segment=current_bracket_segment)

                # TODO: Do something more intelligent here...
                # Currently we just behave like we hit a terminator
                return MatchResult(matched_segs, unmatched_segs)

            else:
                # Are we in a bracket cycle?
                if sub_bracket_count > 0:
                    # Yes we're in a bracket cycle. Ignore the other considerations.

                    # Is it another bracket entry?
                    bracket_match = start_bracket._match(
                        segments=unmatched_segs, match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # increment the open bracket counter and proceed
                        sub_bracket_count += 1
                        # Not using indexing here allows the segments to mutate
                        matched_segs += bracket_match.matched_segments
                        unmatched_segs = bracket_match.unmatched_segments
                        continue

                    # Is it a closing bracket?
                    bracket_match = end_bracket._match(
                        segments=unmatched_segs, match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # reduce the bracket count and then advance the counter.
                        sub_bracket_count -= 1
                        # Not using indexing here allows the segments to mutate
                        matched_segs += bracket_match.matched_segments
                        unmatched_segs = bracket_match.unmatched_segments
                        continue

                else:
                    # No we're not in a bracket cycle.
                    # Here we can either start a bracket cycle, find a target or find a terminator.

                    # First look for a target if there is one.
                    if target:
                        target_match = target._match(
                            unmatched_segs, match_depth=match_depth + 1,
                            parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                            match_segment=match_segment)
                        # Doesn't have to match fully, just has to give us a delimiter.
                        if target_match.has_match():
                            raise NotImplementedError("Still need to do this bit - maybe a callback")
                    # Look for a terminator if there is one.
                    if terminator:
                        terminator_match = terminator._match(
                            unmatched_segs, match_depth=match_depth + 1,
                            parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                            match_segment=match_segment)
                        # Doesn't have to match fully, just has to give us a delimiter.
                        if terminator_match.has_match():
                            # we've found a terminator.
                            # TODO: We might need some kind of callback here to deal with the delimiter case
                            return MatchResult(matched_segs, unmatched_segs)
                    # Look for the start of a new bracket sequence
                    bracket_match = start_bracket._match(
                        segments=unmatched_segs, match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # increment the open bracket counter and proceed
                        sub_bracket_count += 1
                        # Keep track of this segment for error reporting
                        current_bracket_segment = bracket_match.matched_segments[0]
                        # Not using indexing here allows the segments to mutate
                        matched_segs += bracket_match.matched_segments
                        unmatched_segs = bracket_match.unmatched_segments
                        continue
                # Move onward. For the moment we're not fussy about what's in between
                # as we're just looking for terminators or targets.
                # TODO: configure this to allow rules around what can be here.
                # For now, just assume if we've not matched it then it's good.
                matched_segs += unmatched_segs[0],  # as tuple
                unmatched_segs = unmatched_segs[1:]


class Ref(BaseGrammar):
    """ A kind of meta-grammar that allows other defined grammars to be referenced
    at runtime from the dialect """
    # Log less for Ref
    v_level = 4

    def _get_ref(self):
        # Unusually for a grammar we expect _elements to be a list of strings.
        # Notable ONE string for now.
        if len(self._elements) == 1:
            # We're good on length. Get the name of the reference
            return self._elements[0]
        else:
            raise ValueError(
                "Ref grammar can only deal with precisely one element for now. Instead found {0!r}".format(
                    self._elements))

    def _get_elem(self, dialect):
        if dialect:
            # Use the dialect to retrieve the grammar it refers to.
            return dialect.ref(self._get_ref())
        else:
            raise ReferenceError("No Dialect has been provided to Ref grammar!")

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        elem = self._get_elem(dialect=dialect)

        if elem:
            # Match against that. NB We're not incrementing the match_depth here.
            # References shouldn't relly count as a depth of match.
            match_segment = self._get_ref()
            return elem._match(
                segments=segments, match_depth=match_depth,
                parse_depth=parse_depth, verbosity=verbosity,
                dialect=dialect, match_segment=match_segment)
        else:
            raise ValueError("Null Element returned! _elements: {0!r}".format(self._elements))

    def expected_string(self, dialect=None, called_from=None):
        """ pass through to the referenced method """
        elem = self._get_elem(dialect=dialect)
        if called_from and self._get_ref() in called_from:
            # This means we're in recursion so we should stop here.
            # At the moment this means we'll just insert in the name
            # of the segment that we're looking for.
            # Otherwise we get an infinite recursion error
            # TODO: Make this more elegant
            return self._get_ref()
        else:
            # Either add to set or make set
            if called_from:
                called_from.add(self._get_ref())
            else:
                called_from = {self._get_ref()}
            return elem.expected_string(dialect=dialect, called_from=called_from)


class OneOf(BaseGrammar):
    """ Match any of the elements given once, if it matches
    multiple, it returns the longest, and if any are the same
    length it returns the first (unless we explicitly just match first)"""

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', 'longest')  # can be 'first' or 'longest'
        super(OneOf, self).__init__(*args, **kwargs)

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        best_match = None
        # Match on each of the options
        for opt in self._elements:
            m = opt._match(segments, match_depth=match_depth + 1, parse_depth=parse_depth,
                           verbosity=verbosity, dialect=dialect, match_segment=match_segment)
            # If we get a complete match, just return it. If it's incomplete, then check to
            # see if it's all non-code if that allowed and match it
            if m.is_complete():
                # this will return on the *first* complete match
                return m
            elif m:
                if self.code_only:
                    # Attempt to consume whitespace if we can
                    matched_segments = m.matched_segments
                    unmatched_segments = m.unmatched_segments
                    while True:
                        if len(unmatched_segments) > 0:
                            if unmatched_segments[0].is_code:
                                break
                            else:
                                # Append as tuple
                                matched_segments += unmatched_segments[0],
                                unmatched_segments = unmatched_segments[1:]
                        else:
                            break
                    m = MatchResult(matched_segments, unmatched_segments)
                if best_match:
                    if len(m) > len(best_match):
                        best_match = m
                    else:
                        continue
                else:
                    best_match = m
                parse_match_logging(
                    parse_depth, match_depth, match_segment, self.__class__.__name__,
                    '_match', "Saving Match of Length {0}:  {1}".format(len(m), m),
                    verbosity=verbosity, v_level=self.v_level)
        else:
            # No full match from the first time round. If we've got a long partial match then return that.
            if best_match:
                return best_match
            # Ok so no match at all from the elements. Small getout if we can match any whitespace
            if self.code_only:
                matched_segs = tuple()
                unmatched_segs = segments
                # Look for non-code up front
                while True:
                    if len(unmatched_segs) == 0:
                        # We can't return a successful match on JUST whitespace
                        return MatchResult.from_unmatched(segments)
                    elif not unmatched_segs[0].is_code:
                        matched_segs += unmatched_segs[0],
                        unmatched_segs = unmatched_segs[1:]
                    else:
                        break
                # Now try and match
                for opt in self._elements:
                    m = opt._match(unmatched_segs, match_depth=match_depth + 1, parse_depth=parse_depth,
                                   verbosity=verbosity, dialect=dialect, match_segment=match_segment)
                    # Once again, if it's complete - return, if not wait to see if we get a more complete one
                    new_match = MatchResult(matched_segs + m.matched_segments, m.unmatched_segments)
                    if m.is_complete():
                        return new_match
                    elif m:
                        if best_match:
                            if len(best_match) > len(m):
                                best_match = m
                            else:
                                continue
                        else:
                            best_match = m
                        parse_match_logging(
                            parse_depth, match_depth, match_segment, self.__class__.__name__,
                            '_match', "Last-Ditch: Saving Match of Length {0}:  {1}".format(len(m), m),
                            verbosity=verbosity, v_level=self.v_level)
                else:
                    if best_match:
                        return MatchResult(matched_segs + best_match.matched_segments, best_match.unmatched_segments)
                    else:
                        return MatchResult.from_unmatched(segments)

    def expected_string(self, dialect=None, called_from=None):
        return " | ".join([opt.expected_string(dialect=dialect, called_from=called_from) for opt in self._elements])


class AnyNumberOf(BaseGrammar):
    """ A more configurable version of OneOf """
    def __init__(self, *args, **kwargs):
        self.max_times = kwargs.pop('max_times', None)
        self.min_times = kwargs.pop('min_times', 0)
        super(AnyNumberOf, self).__init__(*args, **kwargs)

    def is_optional(self):
        # The optional attribute is set in the __init__ method,
        # But also here, if min_times is zero then this is also optional
        return self.optional or self.min_times == 0

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        # Match on each of the options
        matched_segments = MatchResult.from_empty()
        unmatched_segments = segments
        n_matches = 0
        while True:
            if self.max_times and n_matches >= self.max_times:
                # We've matched as many times as we can
                return MatchResult(matched_segments.matched_segments, unmatched_segments)

            # Is there anything left to match?
            if len(unmatched_segments) == 0:
                # No...
                if n_matches >= self.min_times:
                    return MatchResult(matched_segments.matched_segments, unmatched_segments)
                else:
                    # We didn't meet the hurdle
                    return MatchResult.from_unmatched(unmatched_segments)

            # Is the next segment code?
            if self.code_only and not unmatched_segments[0].is_code:
                # We should add this one to the match and carry on
                matched_segments += unmatched_segments[0],
                unmatched_segments = unmatched_segments[1:]
                check_still_complete(segments, matched_segments.matched_segments, unmatched_segments)
                continue

            # Try the possibilities
            for opt in self._elements:
                m = opt._match(unmatched_segments, match_depth=match_depth + 1,
                               parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                               match_segment=match_segment)
                if m.has_match():
                    matched_segments += m.matched_segments
                    unmatched_segments = m.unmatched_segments
                    n_matches += 1
                    # Break out of the for loop which cycles us round
                    break
            else:
                # If we get here, then we've not managed to match. And the next
                # unmatched segments are meaningful, i.e. they're not what we're
                # looking for.
                if n_matches >= self.min_times:
                    return MatchResult(matched_segments.matched_segments, unmatched_segments)
                else:
                    # We didn't meet the hurdle
                    return MatchResult.from_unmatched(unmatched_segments)

    def expected_string(self, dialect=None, called_from=None):
        # TODO: Make something nice here
        return " !!TODO!! "


class GreedyUntil(BaseGrammar):
    """ See the match method desription for the full details """
    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        """
        Matching for GreedyUntil works just how you'd expect.
        """
        for idx, seg in enumerate(segments):
            for opt in self._elements:
                if opt._match(seg, match_depth=match_depth + 1, parse_depth=parse_depth,
                              verbosity=verbosity, dialect=dialect, match_segment=match_segment):
                    # We've matched something. That means we should return everything up to this point
                    return MatchResult(segments[:idx], segments[idx:])
                else:
                    continue
        else:
            # We've got to the end without matching anything, so return.
            # We don't need to keep track of the match results, because
            # if any of them were usable, then we wouldn't be returning
            # anyway.
            return MatchResult.from_matched(segments)

    def expected_string(self, dialect=None, called_from=None):
        return "..., " + " !( " + " | ".join(
            [opt.expected_string(dialect=dialect, called_from=called_from) for opt in self._elements]
        ) + " ) "


class Sequence(BaseGrammar):
    """ Match a specific sequence of elements """

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        # Rewrite of sequence. We should match FORWARD, this reduced duplication.
        # Sub-matchers should be greedy and so we can jsut work forward with each one.
        if isinstance(segments, BaseSegment):
            segments = tuple(segments)
        # NB: We don't use seg_idx here because the submatchers may be mutating the length
        # of the remaining segments
        matched_segments = MatchResult.from_empty()
        unmatched_segments = segments

        for idx, elem in enumerate(self._elements):
            while True:
                if len(unmatched_segments) == 0:
                    # We've run our of sequence without matching everyting.
                    # Do only optional elements remain.
                    if all([e.is_optional() for e in self._elements[idx:]]):
                        # then it's ok, and we can return what we've got so far.
                        # No need to deal with anything left over because we're at the end.
                        return matched_segments
                    else:
                        # we've got to the end of the sequence without matching all
                        # required elements.
                        return MatchResult.from_unmatched(segments)
                else:
                    # We're not at the end, first detect whitespace and then try to match.
                    if self.code_only and not unmatched_segments[0].is_code:
                        # We should add this one to the match and carry on
                        matched_segments += unmatched_segments[0],
                        unmatched_segments = unmatched_segments[1:]
                        check_still_complete(segments, matched_segments.matched_segments, unmatched_segments)
                        continue

                    # It's not whitespace, so carry on to matching
                    elem_match = elem._match(
                        unmatched_segments, match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)

                    if elem_match.has_match():
                        # We're expecting mostly partial matches here, but complete
                        # matches are possible.
                        matched_segments += elem_match.matched_segments
                        unmatched_segments = elem_match.unmatched_segments
                        # Each time we do this, we do a sense check to make sure we haven't
                        # dropped anything. (Because it's happened before!).
                        check_still_complete(segments, matched_segments.matched_segments, unmatched_segments)

                        # Break out of the while loop and move to the next element.
                        break
                    else:
                        # If we can't match an element, we should ascertain whether it's
                        # required. If so then fine, move on, but otherwise we should crash
                        # out without a match. We have not matched the sequence.
                        if elem.is_optional():
                            # This will crash us out of the while loop and move us
                            # onto the next matching element
                            break
                        else:
                            return MatchResult.from_unmatched(segments)
        else:
            # If we get to here, we've matched all of the elements (or skipped them)
            # but still have some segments left (or perhaps have precisely zero left).
            # In either case, we're golden. Return successfully, with any leftovers as
            # the unmatched elements. UNLESS they're whitespace and we should be greedy.
            if self.code_only:
                while True:
                    if len(unmatched_segments) == 0:
                        break
                    elif not unmatched_segments[0].is_code:
                        # We should add this one to the match and carry on
                        matched_segments += unmatched_segments[0],
                        unmatched_segments = unmatched_segments[1:]
                        check_still_complete(segments, matched_segments.matched_segments, unmatched_segments)
                        continue
                    else:
                        break

            return MatchResult(matched_segments.matched_segments, unmatched_segments)

    def expected_string(self, dialect=None, called_from=None):
        return ", ".join([opt.expected_string(dialect=dialect, called_from=called_from) for opt in self._elements])


class Delimited(BaseGrammar):
    """ Match an arbitrary number of elements seperated by a delimiter.
    Note that if there are multiple elements passed in that they will be treated
    as different options of what can be delimited, rather than a sequence. """
    def __init__(self, *args, **kwargs):
        if 'delimiter' not in kwargs:
            raise ValueError("Delimited grammars require a `delimiter`")
        self.delimiter = kwargs.pop('delimiter')
        self.allow_trailing = kwargs.pop('allow_trailing', False)
        self.terminator = kwargs.pop('terminator', None)
        # Setting min delimiters means we have to match at least this number
        self.min_delimiters = kwargs.pop('min_delimiters', None)

        # The details on how to match a bracket are stored in the dialect
        self.start_bracket = Ref('StartBracketSegment')
        self.end_bracket = Ref('EndBracketSegment')
        super(Delimited, self).__init__(*args, **kwargs)

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        if isinstance(segments, BaseSegment):
            segments = [segments]
        seg_idx = 0
        terminal_idx = len(segments)
        sub_bracket_count = 0
        start_bracket_idx = None
        # delimiters is a list of tuples (idx, len), which keeps track of where
        # we found delimiters up to this point.
        delimiters = []
        matched_segments = MatchResult.from_empty()

        # Have we been passed an empty list?
        if len(segments) == 0:
            return MatchResult.from_empty()

        # First iterate through all the segments, looking for the delimiter.
        # Second, split the list on each of the delimiters, and ensure that
        # each sublist in turn matches one of the elements.

        # In more detail, match against delimiter, if we match, put a slice
        # up to that point onto a list of slices. Carry on.
        while True:
            # Are we at the end of the sequence?
            if seg_idx >= terminal_idx:
                # Yes we're at the end

                # We now need to check whether everything from either the start
                # or from the last delimiter up to here matches. We CAN allow
                # a partial match at this stage.

                # Are we in a bracket counting cycle that hasn't finished yet?
                if sub_bracket_count > 0:
                    # TODO: Format this better
                    raise SQLParseError(
                        "Couldn't find closing bracket for opening bracket.",
                        segment=segments[start_bracket_idx])

                # Do we already have any delimiters?
                if delimiters:
                    # Yes, get the last delimiter
                    dm1 = delimiters[-1]
                    # get everything after the last delimiter
                    pre_segment = segments[dm1[0] + dm1[1]:terminal_idx]
                else:
                    # No, no delimiters at all so far.
                    # TODO: Allow this to be configured.
                    # Just get everything up to this point
                    pre_segment = segments[:terminal_idx]

                # Optionally here, we can match some non-code up front.
                if self.code_only:
                    while len(pre_segment) > 0:
                        if not pre_segment[0].is_code:
                            matched_segments += pre_segment[0],  # As tuple
                            pre_segment = pre_segment[1:]
                        else:
                            break

                # Check we actually have something left to match on
                if len(pre_segment) > 0:
                    # See if any of the elements match
                    for elem in self._elements:
                        elem_match = elem._match(
                            pre_segment, match_depth=match_depth + 1,
                            parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                            match_segment=match_segment)

                        if elem_match.has_match():
                            # Successfully matched one of the elements in this spot

                            # Add this match onto any already matched segments and return.
                            # We do this in a slightly odd way here to allow partial matches.

                            # we do a quick check on min_delimiters if present
                            if self.min_delimiters and len(delimiters) < self.min_delimiters:
                                # if we do have a limit and we haven't met it then crash out
                                return MatchResult.from_unmatched(segments)
                            return MatchResult(
                                matched_segments.matched_segments + elem_match.matched_segments,
                                elem_match.unmatched_segments + segments[terminal_idx:])
                        else:
                            # Not matched this element, move on.
                            # NB, a partial match here isn't helpful. We're matching
                            # BETWEEN two delimiters and so it must be a complete match.
                            # Incomplete matches are only possible at the end
                            continue

                # If we're here we haven't matched any of the elements on this last element.
                # BUT, if we allow trailing, and we have matched something, we can end on the last
                # delimiter
                if self.allow_trailing and len(matched_segments) > 0:
                    return MatchResult(matched_segments.matched_segments, pre_segment + segments[terminal_idx:])
                else:
                    return MatchResult.from_unmatched(segments)

            else:
                # We've got some sequence left.
                # Are we in a bracket cycle?
                if sub_bracket_count > 0:
                    # Is it another bracket entry?
                    bracket_match = self.start_bracket._match(
                        segments=segments[seg_idx:], match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # increment the open bracket counter and proceed
                        sub_bracket_count += 1
                        seg_idx += len(bracket_match)
                        continue

                    # Is it a closing bracket?
                    bracket_match = self.end_bracket._match(
                        segments=segments[seg_idx:], match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # reduce the bracket count and then advance the counter.
                        sub_bracket_count -= 1
                        seg_idx += len(bracket_match)
                        continue

                else:
                    # No bracket cycle
                    # Do we have a delimiter at the current index?

                    del_match = self.delimiter._match(
                        segments[seg_idx:], match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)

                    # Doesn't have to match fully, just has to give us a delimiter.
                    if del_match.has_match():
                        # We've got at least a partial match
                        # Record the location of this delimiter
                        d = (seg_idx, len(del_match))
                        # Do we already have any delimiters?
                        if delimiters:
                            # Yes
                            dm1 = delimiters[-1]
                            # slice the segments between this delimiter and the previous
                            pre_segment = segments[dm1[0] + dm1[1]:d[0]]
                        else:
                            # No
                            # Just get everything up to this point
                            pre_segment = segments[:d[0]]
                        # Append the delimiter that we have found.
                        delimiters.append(d)

                        # Optionally here, we can match some non-code up front.
                        if self.code_only:
                            while len(pre_segment) > 0:
                                if not pre_segment[0].is_code:
                                    matched_segments += pre_segment[0],  # As tuple
                                    pre_segment = pre_segment[1:]
                                else:
                                    break

                        # We now check that this chunk matches whatever we're delimiting.
                        # In this case it MUST be a full match, not just a partial match
                        for elem in self._elements:
                            elem_match = elem._match(
                                pre_segment, match_depth=match_depth + 1,
                                parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                                match_segment=match_segment)

                            if elem_match.is_complete():
                                # Successfully matched one of the elements in this spot

                                # First add the segment up to the delimiter to the matched segments
                                matched_segments += elem_match
                                # Then add the delimiter to the matched segments
                                matched_segments += del_match
                                # Break this for loop and move on, looking for the next delimiter
                                seg_idx += len(del_match)
                                break
                            elif elem_match and self.code_only:
                                # Optionally if it's not a complete match but the unmatched bits are
                                # all non code then we'll also take it.
                                if all([not seg.is_code for seg in elem_match.unmatched_segments]):
                                    # Logic as above, just with the unmatched bits too because none are code
                                    matched_segments += elem_match.matched_segments
                                    matched_segments += elem_match.unmatched_segments
                                    matched_segments += del_match
                                    seg_idx += len(del_match)
                                    break
                                else:
                                    continue
                            else:
                                # Not matched this element, move on.
                                # NB, a partial match here isn't helpful. We're matching
                                # BETWEEN two delimiters and so it must be a complete match.
                                # Incomplete matches are only possible at the end
                                continue
                        else:
                            # If we're here we haven't matched any of the elements, then we have a problem
                            return MatchResult.from_unmatched(segments)
                    # This index doesn't have a delimiter, check for brackets and terminators

                    # First is it a terminator (and we're not in a bracket cycle)
                    if self.terminator:
                        term_match = self.terminator._match(
                            segments[seg_idx:], match_depth=match_depth + 1,
                            parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                            match_segment=match_segment)
                        if term_match:
                            # we've found a terminator.
                            # End the cycle here.
                            terminal_idx = seg_idx
                            continue

                    # Last, do we need to enter a bracket cycle
                    bracket_match = self.start_bracket._match(
                        segments=segments[seg_idx:], match_depth=match_depth + 1,
                        parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                        match_segment=match_segment)
                    if bracket_match.has_match():
                        # increment the open bracket counter and proceed
                        sub_bracket_count += 1
                        seg_idx += len(bracket_match)
                        continue

                # Nothing else interesting. Carry On
                # This is the same regardless of whether we're in the bracket cycle
                # or otherwise.
                seg_idx += 1

    def expected_string(self, dialect=None, called_from=None):
        return " {0} ".format(
            self.delimiter.expected_string(dialect=dialect, called_from=called_from)).join(
                [opt.expected_string(dialect=dialect, called_from=called_from) for opt in self._elements])


class ContainsOnly(BaseGrammar):
    """ match a sequence of segments which are only of the types,
    or only match the grammars in the list """
    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        matched_buffer = tuple()
        forward_buffer = segments
        while True:
            if len(forward_buffer) == 0:
                # We're all good
                return MatchResult.from_matched(matched_buffer)
            elif self.code_only and not forward_buffer[0].is_code:
                matched_buffer += forward_buffer[0],
                forward_buffer = forward_buffer[1:]
            else:
                # Try and match it
                for opt in self._elements:
                    if isinstance(opt, str):
                        if forward_buffer[0].type == opt:
                            matched_buffer += forward_buffer[0],
                            forward_buffer = forward_buffer[1:]
                            break
                    else:
                        m = opt._match(
                            forward_buffer, match_depth=match_depth + 1, parse_depth=parse_depth,
                            verbosity=verbosity, dialect=dialect, match_segment=match_segment)
                        if m:
                            matched_buffer += m.matched_segments
                            forward_buffer = m.unmatched_segments
                            break
                else:
                    # Unable to match the forward buffer. We must have found something
                    # which isn't on our element list. Crash out.
                    return MatchResult.from_unmatched(segments)

    def expected_string(self, dialect=None, called_from=None):
        buff = []
        for opt in self._elements:
            if isinstance(opt, str):
                buff.append(opt)
            else:
                buff.append(opt.expected_string(dialect=dialect, called_from=called_from))
        return " ( " + " | ".join(buff) + " | + )"


class StartsWith(BaseGrammar):
    """ Match if the first element is the same, with configurable
    whitespace and comment handling """
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.terminator = kwargs.pop('terminator', None)
        # The details on how to match a bracket are stored in the dialect
        self.start_bracket = Ref('StartBracketSegment')
        self.end_bracket = Ref('EndBracketSegment')
        super(StartsWith, self).__init__(*args, **kwargs)

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        if self.code_only:
            first_code_idx = None
            # Work through to find the first code segment...
            for idx, seg in enumerate(segments):
                if seg.is_code:
                    first_code_idx = idx
                    break
            else:
                # We've trying to match on a sequence of segments which contain no code.
                # That means this isn't a match.
                return MatchResult.from_unmatched(segments)

            match = self.target._match(
                segments=segments[first_code_idx:], match_depth=match_depth + 1,
                parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                match_segment=match_segment)
            if match:
                # The match will probably have returned a mutated version rather
                # that the raw segment sent for matching. We need to reinsert it
                # back into the sequence in place of the raw one, but we can't
                # just assign at the index because it's a tuple and not a list.
                # to get around that we do this slightly more elaborate construction.

                # NB: This match may be partial or full, either is cool. In the case
                # of a partial match, given that we're only interested in what it STARTS
                # with, then we can still used the unmatched parts on the end.
                # We still need to deal with any non-code segments at the start.
                if self.terminator:
                    # We have an optional terminator. We should only match up to when
                    # this matches. This should also respect bracket counting.
                    match_segments = match.matched_segments
                    trailing_segments = match.unmatched_segments

                    # Given a set of segments, iterate through looking for
                    # a terminator.
                    term_match = self.bracket_sensitive_forward_match(
                        segments=trailing_segments,
                        start_bracket=self.start_bracket,
                        end_bracket=self.end_bracket,
                        match_depth=match_depth,
                        parse_depth=parse_depth,
                        verbosity=verbosity,
                        terminator=self.terminator,
                        dialect=dialect,
                        match_segment=match_segment
                    )
                    return MatchResult(
                        segments[:first_code_idx]
                        + match_segments
                        + term_match.matched_segments,
                        term_match.unmatched_segments,
                    )
                else:
                    return MatchResult.from_matched(
                        segments[:first_code_idx]
                        + match.matched_segments
                        + match.unmatched_segments)
            else:
                return MatchResult.from_unmatched(segments)
        else:
            raise NotImplementedError("Not expecting to match StartsWith and also not just code!?")

    def expected_string(self, dialect=None, called_from=None):
        return self.target.expected_string(dialect=dialect, called_from=called_from) + ", ..."


class Bracketed(BaseGrammar):
    """ Bracketed works differently to sequence, although it used to. Note
    that if multiple arguments are passed then the options will be considered
    as options for what can be in the brackets rather than a sequence. """
    def __init__(self, *args, **kwargs):
        # Start and end tokens
        # The details on how to match a bracket are stored in the dialect
        self.start_bracket = Ref('StartBracketSegment')
        self.end_bracket = Ref('EndBracketSegment')
        super(Bracketed, self).__init__(*args, **kwargs)

    def match(self, segments, match_depth=0, parse_depth=0, verbosity=0, dialect=None, match_segment=None):
        """ The match function for `bracketed` implements bracket counting. """

        # 1. work forwards to find the first bracket.
        #    If we find something other that whitespace, then fail out.
        # 2. Once we have the first bracket, we need to bracket count forward to find it's partner.
        # 3. Assuming we find it's partner then we try and match what goes between them.
        #    If we match, great. If not, then we return an empty match.
        #    If we never find it's partner then we return an empty match but should probably
        #    log a parsing warning, or error?

        sub_bracket_count = 0
        pre_content_segments = tuple()
        unmatched_segs = segments
        matched_segs = tuple()
        current_bracket_segment = None

        # Step 1. Find the first useful segment
        # Work through to find the first code segment...
        if self.code_only:
            for idx, seg in enumerate(segments):
                if seg.is_code:
                    break
                else:
                    matched_segs += seg,
                    unmatched_segs = unmatched_segs[1:]
            else:
                # We've trying to match on a sequence of segments which contain no code.
                # That means this isn't a match.
                return MatchResult.from_unmatched(segments)

        # is it a bracket?
        m = self.start_bracket._match(
            segments=unmatched_segs, match_depth=match_depth + 1,
            parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
            match_segment=match_segment)

        if m.has_match():
            # We've got the first bracket.
            # Update the seg_idx by the length of the match
            current_bracket_segment = m.matched_segments[0]
            # No indexing to allow mutation
            matched_segs += m.matched_segments
            unmatched_segs = m.unmatched_segments
        else:
            # Whatever we have, it doesn't start with a bracket.
            return MatchResult.from_unmatched(segments)

        # Step 2: Bracket count forward to find it's pair
        content_segments = tuple()
        pre_content_segments = matched_segs

        while True:
            # Are we at the end of the sequence?
            if len(unmatched_segs) == 0:
                # We've got to the end without finding the closing bracket
                # this isn't just parsing issue this is probably a syntax
                # error.
                # TODO: Format this better
                raise SQLParseError(
                    "Couldn't find closing bracket for opening bracket.",
                    segment=current_bracket_segment)

            # Is it a closing bracket?
            m = self.end_bracket._match(
                segments=unmatched_segs, match_depth=match_depth + 1,
                parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                match_segment=match_segment)
            if m.has_match():
                if sub_bracket_count == 0:
                    # We're back to the bracket pair!
                    matched_segs += m.matched_segments
                    unmatched_segs = m.unmatched_segments
                    closing_bracket_segs = m.matched_segments
                    break
                else:
                    # reduce the bracket count and then advance the counter.
                    sub_bracket_count -= 1
                    matched_segs += m.matched_segments
                    unmatched_segs = m.unmatched_segments
                    continue

            # Is it an opening bracket?
            m = self.start_bracket._match(
                segments=unmatched_segs, match_depth=match_depth + 1,
                parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                match_segment=match_segment)
            if m.has_match():
                # increment the open bracket counter and proceed
                sub_bracket_count += 1
                matched_segs += m.matched_segments
                unmatched_segs = m.unmatched_segments
                continue

            # If we get here it's not an opening bracket or a closing bracket
            # so we should carry on our merry way
            matched_segs += unmatched_segs[0],
            content_segments += unmatched_segs[0],
            unmatched_segs = unmatched_segs[1:]

        # If we get to here then we've found our closing bracket.
        # Let's identify the section to match for our content matchers
        # and then try it against each of them.

        for elem in self._elements:
            elem_match = elem._match(
                content_segments, match_depth=match_depth + 1,
                parse_depth=parse_depth, verbosity=verbosity, dialect=dialect,
                match_segment=match_segment)
            # Matches at this stage must be complete, because we've got nothing
            # to do with any leftovers within the brackets.
            if elem_match.is_complete():
                # We're also returning the *mutated* versions from the sub-matcher
                return MatchResult(
                    pre_content_segments
                    + elem_match.matched_segments
                    + closing_bracket_segs,
                    unmatched_segs)
            else:
                # Not matched this element, move on.
                # NB, a partial match here isn't helpful. We're matching
                # BETWEEN two delimiters and so it must be a complete match.
                # Incomplete matches are only possible at the end
                continue
        else:
            # If we're here we haven't matched any of the elements, then we have a problem
            return MatchResult.from_unmatched(segments)

    def expected_string(self, dialect=None, called_from=None):
        return " ( {0} ) ".format(' | '.join([opt.expected_string(dialect=dialect, called_from=called_from) for opt in self._elements]))
