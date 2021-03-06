from toga.interface import MultilineTextInput as MultilineTextInputInterface

from ..libs import *
from .base import WidgetMixin


class MultilineTextInput(MultilineTextInputInterface, WidgetMixin):
    def __init__(self, initial=None, style=None):
        super(MultilineTextInput, self).__init__(style=style)
        self._create()

        self.value = initial

    def create(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.hasVerticalScroller = True
        self._impl.hasHorizontalScroller = False
        self._impl.autohidesScrollers = False
        self._impl.borderType = NSBezelBorder

        # Disable all autolayout functionality on the outer widget
        self._impl.translatesAutoresizingMaskIntoConstraints = False
        self._impl.autoresizesSubviews = True

        # Create the actual text widget
        self._text = NSTextView.alloc().init()
        self._text.editable = True
        self._text.enabled = True
        self._text.selectable = True
        self._text.verticallyResizable = True
        self._text.horizontallyResizable = False

        # Disable the autolayout functionality, and replace with
        # constraints controlled by the layout.
        self._text.translatesAutoresizingMaskIntoConstraints = False
        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._text, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._text, NSLayoutAttributeLeft,
            1.0, 0
        )
        self._text.addConstraint(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._text, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._text, NSLayoutAttributeTop,
            1.0, 0
        )
        self._text.addConstraint(self._height_constraint)

        # Put the text view in the scroll window.
        self._impl.documentView = self._text

        # Add the layout constraints
        self._add_constraints()

    @property
    def value(self):
        return self._text.string

    @value.setter
    def value(self, value):
        if value:
            self._text.insertText(value)

    def _update_child_layout(self):
        self._width_constraint.constant = self.layout.width
        self._height_constraint.constant = self.layout.height

    def rehint(self):
        self.style.hint(
            min_height=100,
            min_width=100
        )
