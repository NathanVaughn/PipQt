import re


def center_widget(parent, widget):
    """Moves a widget to be centered with respect to the parent"""
    x = parent.pos().x() + (0.5 * parent.width()) - (0.5 * widget.width())
    y = parent.pos().y() + (0.5 * parent.height()) - (0.5 * widget.height())

    widget.move(x, y)

def sanitize_text(text):
    """Attempts to sanitize package text from common attack vectors"""
    return re.sub("[|]*[&]*[;]*[\\s]*", "", text)
