# Development Log

## 26 September 2026

### Initial GUI prototype

Created the first interface using Python and PySide6.

The first prototype displayed device information and live grip
information on a single dashboard.

### Problem identified

The interface felt cluttered because several types of information
were presented simultaneously.

### Design decision

Changed the proposed interface to a multi-page design.

The home screen will provide large buttons for:

- Live Grip
- Analytics
- Settings
- Device Information

A QStackedWidget will be used to switch between these pages.

### Accessibility

The interface will use large buttons, clear text and minimal
information on each page because the intended users may have
motor-control difficulties.

### Next step

Implement basic page navigation.


# Development Log

## 27 September 2026

### Theme of GUI

Decided on an apple/tesla theme mix, slightly modern, minimalistic and dark mode.

### Next step

Implement it into the GUI and get buttons to work