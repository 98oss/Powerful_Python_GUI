import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import math


class SpeedometerGauge(QtWidgets.QWidget):
    """Custom circular speedometer gauge widget"""
    
    def __init__(self, max_value=500, label="SPEED", parent=None):
        super().__init__(parent)
        self.max_value = max_value
        self.current_value = 0
        self.label = label
        self.setMinimumSize(250, 250)
        
    def setValue(self, value):
        """Set the current value of the gauge"""
        self.current_value = max(0, min(value, self.max_value))
        self.update()
    
    def value(self):
        """Get the current value"""
        return self.current_value
    
    def paintEvent(self, event):
        """Custom paint event to draw the speedometer"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Get widget dimensions
        width = self.width()
        height = self.height()
        size = min(width, height)
        
        # Center point
        center_x = width / 2
        center_y = height / 2
        radius = size * 0.4
        
        # Draw outer circle (gauge background)
        painter.setPen(QtGui.QPen(QtGui.QColor("#3a3a3a"), 3))
        painter.setBrush(QtGui.QColor("#252525"))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)
        
        # Draw tick marks and value labels
        painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff"), 2))
        for i in range(0, 11):  # 0 to max_value in 10 steps
            angle = -45 + (270 * i / 10)  # Start at -45° (top-right), sweep 270° to 225° (top-left)
            rad = math.radians(angle)
            
            # Draw tick marks
            inner_radius = radius * 0.85
            outer_radius = radius * 0.95
            x1 = center_x + inner_radius * math.cos(rad)
            y1 = center_y + inner_radius * math.sin(rad)
            x2 = center_x + outer_radius * math.cos(rad)
            y2 = center_y + outer_radius * math.sin(rad)
            painter.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))
            
            # Draw value labels
            label_value = int(self.max_value * i / 10)
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(rad)
            label_y = center_y + label_radius * math.sin(rad)
            painter.drawText(QtCore.QRectF(label_x - 20, label_y - 10, 40, 20),
                           QtCore.Qt.AlignCenter, str(label_value))
        
        # Draw colored arc (speed range indicator)
        # Arc spans from 135° to 405° (270° total)
        painter.setPen(QtCore.Qt.NoPen)
        
        # Draw arc in segments with gradient colors
        num_segments = 100
        for i in range(num_segments):
            # Calculate color based on position
            ratio = i / num_segments
            if ratio < 0.33:
                # Green to Yellow
                local_ratio = ratio / 0.33
                color = QtGui.QColor(
                    int(0 + (255 * local_ratio)),
                    255,
                    0
                )
            elif ratio < 0.66:
                # Yellow to Orange
                local_ratio = (ratio - 0.33) / 0.33
                color = QtGui.QColor(
                    255,
                    int(255 - (112 * local_ratio)),
                    0
                )
            else:
                # Orange to Red
                local_ratio = (ratio - 0.66) / 0.34
                color = QtGui.QColor(
                    255,
                    int(143 - (143 * local_ratio)),
                    0
                )
            
            painter.setPen(QtGui.QPen(color, 8))
            start_angle = (-45 + (270 * i / num_segments)) * 16
            span_angle = (270 / num_segments) * 16
            arc_rect = QtCore.QRectF(center_x - radius * 0.9, center_y - radius * 0.9,
                                      radius * 1.8, radius * 1.8)
            painter.drawArc(arc_rect, int(start_angle), int(span_angle))
        
        # Draw needle
        value_angle = -45 + (270 * self.current_value / self.max_value)
        needle_rad = math.radians(value_angle)
        needle_length = radius * 0.8
        needle_x = center_x + needle_length * math.cos(needle_rad)
        needle_y = center_y + needle_length * math.sin(needle_rad)
        
        painter.setPen(QtGui.QPen(QtGui.QColor("#ff0000"), 3))
        painter.drawLine(QtCore.QPointF(center_x, center_y),
                        QtCore.QPointF(needle_x, needle_y))
        
        # Draw center circle (needle pivot)
        painter.setBrush(QtGui.QColor("#ff0000"))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), 8, 8)
        
        # Draw gauge label
        painter.setPen(QtGui.QColor("#ffffff"))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QtCore.QRectF(0, center_y - radius * 0.7, width, 30),
                        QtCore.Qt.AlignCenter, self.label)
        
        # Draw current value text
        font.setPointSize(16)
        painter.setFont(font)
        painter.drawText(QtCore.QRectF(0, center_y - 20, width, 40),
                        QtCore.Qt.AlignCenter, f"{self.current_value:.1f}")
