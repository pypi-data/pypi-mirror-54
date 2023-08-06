from __future__ import absolute_import

from .. import defaults
from ..layer import Layer
from .utils import serialize_palette


def color_continuous_layer(
        source, value, title='', palette=None, size=None,
        opacity=None, stroke_color=None, stroke_width=None,
        description='', footer='', legend=True, popup=True,
        widget=False, animate=None):
    """Helper function for quickly creating a continuous color map.

    Args:
        source (:py:class:`Dataset <cartoframes.data.Dataset>` or str): Dataset
          or text representing a table or query associated with user account.
        value (str): Column to symbolize by.
        title (str, optional): Title of legend
        palette (str, optional): Palette that can be a named cartocolor palette
          or other valid CARTO VL palette expression. Default is `bluyl`.
        size (int, optional): Size of point or line features.
        opacity (int, optional): Opacity value for point color and line features.
          Default is '0.8'.
        stroke_width (int, optional): Size of the stroke on point features.
        stroke_color (str, optional): Color of the stroke on point features.
          Default is '#222'.
        description (str, optional): Description text legend placed under legend title.
        footer (str, optional): Footer text placed under legend items.
        legend (bool, optional): Display map legend: "True" or "False".
          Set to "True" by default.
        popup (bool, optional): Display popups on hover and click: "True" or "False".
          Set to "True" by default.
        widget (bool, optional): Display a widget for mapped data.
          Set to "False" by default.
        animate (str, optional): Animate features by date/time or other numeric field.

    Returns:
        cartoframes.viz.Layer: Layer styled by `value`.
        Includes a legend, popup and widget on `value`.
    """
    default_palette = 'bluyl'
    animation_filter = 'animation(linear(${}), 20, fade(1,1))'.format(animate) if animate else '1'

    return Layer(
        source,
        style={
            'point': {
                'color': 'opacity(ramp(linear(${0}), {1}),{2})'.format(
                    value, serialize_palette(palette) or default_palette,
                    opacity or '1'),
                'width': '{0}'.format(
                    size or defaults.STYLE['point']['width']),
                'strokeColor': '{0}'.format(
                    stroke_color or defaults.STYLE['point']['strokeColor']),
                'strokeWidth': '{0}'.format(
                    stroke_width or defaults.STYLE['point']['strokeWidth']),
                'filter': animation_filter
            },
            'line': {
                'color': 'opacity(ramp(linear(${0}), {1}),{2})'.format(
                    value, serialize_palette(palette) or default_palette,
                    opacity or '1'),
                'width': '{0}'.format(
                    size or defaults.STYLE['line']['width']),
                'filter': animation_filter
            },
            'polygon': {
                'color': 'opacity(ramp(linear(${0}), {1}), {2})'.format(
                    value, serialize_palette(palette) or default_palette,
                    opacity or '0.9'),
                'strokeColor': '{0}'.format(
                    stroke_color or defaults.STYLE['polygon']['strokeColor']),
                'strokeWidth': '{0}'.format(
                    stroke_width or defaults.STYLE['polygon']['strokeWidth']),
                'filter': animation_filter
            }
        },
        popup=popup and not animate and {
            'hover': {
                'title': title or value,
                'value': '$' + value
            }
        },
        legend=legend and {
            'type': {
                'point': 'color-continuous-point',
                'line': 'color-continuous-line',
                'polygon': 'color-continuous-polygon'
            },
            'title': title or value,
            'description': description,
            'footer': footer
        },
        widgets=[
            animate and {
                'type': 'time-series',
                'value': animate,
                'title': 'Animation'
            },
            widget and {
                'type': 'histogram',
                'value': value,
                'title': 'Distribution'
            }
        ]
    )
