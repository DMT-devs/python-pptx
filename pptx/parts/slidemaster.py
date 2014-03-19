# encoding: utf-8

"""
Objects related to the slide master part
"""

from __future__ import absolute_import, print_function

from warnings import warn

from pptx.parts.slide import BaseSlide
from pptx.util import lazyproperty


class SlideMaster(BaseSlide):
    """
    Slide master part. Corresponds to package files
    ppt/slideMasters/slideMaster[1-9][0-9]*.xml.
    """
    @property
    def sldLayoutIdLst(self):
        """
        The ``<p:sldLayoutIdLst>`` child element specifying the slide layouts
        of this slide master in the XML.
        """
        return self._element.get_or_add_sldLayoutIdLst()

    @lazyproperty
    def slide_layouts(self):
        """
        Sequence of |SlideLayout| objects belonging to this slide master
        """
        return _SlideLayouts(self)

    @property
    def slidelayouts(self):
        """
        Deprecated. Use ``.slide_layouts`` property instead.
        """
        msg = (
            'SlideMaster.slidelayouts property is deprecated. Use .slide_lay'
            'outs instead.'
        )
        warn(msg, UserWarning, stacklevel=2)
        return self.slide_layouts


class _SlideLayouts(object):
    """
    Collection of slide layouts belonging to an instance of |SlideMaster|,
    having list access semantics. Supports indexed access, len(), and
    iteration.
    """
    def __init__(self, slide_master):
        super(_SlideLayouts, self).__init__()
        self._slide_master = slide_master

    def __getitem__(self, idx):
        """
        Provide indexed access, (e.g. ``slide_layouts[2]``).
        """
        if idx >= len(self._sldLayoutIdLst):
            raise IndexError('slide layout index out of range')
        rId = self._sldLayoutIdLst.sldLayoutId_lst[idx].rId
        return self._slide_master.related_parts[rId]

    def __iter__(self):
        """
        Generate a reference to each of the |SlideLayout| instances in the
        collection, in sequence.
        """
        for rId in self._iter_rIds():
            yield self._slide_master.related_parts[rId]

    def __len__(self):
        """
        Support len() built-in function (e.g. 'len(slides) == 4').
        """
        return len(self._sldLayoutIdLst)

    def _iter_rIds(self):
        """
        Generate the rId for each slide layout in the collection, in
        sequence.
        """
        sldLayoutId_lst = self._sldLayoutIdLst.sldLayoutId_lst
        for sldLayoutId in sldLayoutId_lst:
            yield sldLayoutId.rId

    @property
    def _sldLayoutIdLst(self):
        """
        The ``<p:sldLayoutIdLst>`` element specifying the slide layouts in
        this collection. This element is a child of the ``<p:sldMaster>``
        element, the root element of a slide master part.
        """
        return self._slide_master.sldLayoutIdLst
