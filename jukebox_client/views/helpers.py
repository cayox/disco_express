import os

from PyQt6 import QtCore, QtGui, QtSvg

from jukebox_client.config import APP_CONFIG_ROOT


def load_colored_svg(
    relative_svg_path: str, color: str, icon_size: int = 32
) -> QtGui.QPixmap:
    """Load and color an SVG, returning a QPixmap."""
    # Read SVG data
    path = os.path.join(APP_CONFIG_ROOT, relative_svg_path)
    with open(path, "rb") as file:
        svg_data = file.read()

    # Replace color in SVG
    svg_data = svg_data.replace(b'fill="#000000"', f'fill="{color}"'.encode())
    svg_data = svg_data.replace(b'stroke="#000000"', f'stroke="{color}"'.encode())

    # Render the modified SVG
    svg_renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data))
    image = QtGui.QPixmap(QtCore.QSize(icon_size, icon_size))  # Set the size as needed
    image.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(image)
    svg_renderer.render(painter)
    painter.end()

    return image
