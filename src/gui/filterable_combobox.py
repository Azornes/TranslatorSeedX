"""
Custom Filterable ComboBox for PyQt6 with live filtering popup, no auto-completion
"""

from PyQt6.QtWidgets import QComboBox, QCompleter
from PyQt6.QtCore import Qt, QStringListModel


class FilterableComboBox(QComboBox):
    """
    A QComboBox with live filtering popup. No auto-completion in the line edit.
    Suggestions appear in a popup as you type, but text is not auto-completed.
    Select by clicking or pressing Enter on the desired item.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        # Model z wszystkimi opcjami
        self.source_model = QStringListModel()

        # Ustawienie QCompleter w trybie popup
        self.completer_ = QCompleter(self.source_model, self)
        self.completer_.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer_.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer_.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.setCompleter(self.completer_)

        # Połączenie sygnałów
        self.lineEdit().textEdited.connect(self.on_text_edited)
        self.completer_.activated.connect(self.on_completer_activated)

    def on_text_edited(self, text):
        # Filtruje listę podpowiedzi "na żywo"
        filtered = [item for item in self.source_model.stringList() if text.lower() in item.lower()]
        self.completer_.model().setStringList(filtered)
        if text:
            self.completer_.complete()
        else:
            self.hidePopup()

    def on_completer_activated(self, text):
        # Ustawienie wybranej wartości
        self.setCurrentText(text)
        self.hidePopup()

    def addItems(self, texts):
        """Add items to the source model"""
        self.source_model.setStringList(texts)
        self.completer_.model().setStringList(texts)  # Initial full list

    def setCurrentText(self, text):
        """Set current text"""
        index = self.findText(text)
        if index >= 0:
            self.setCurrentIndex(index)
        else:
            self.lineEdit().setText(text)

    def text(self):
        """Get current text"""
        return self.lineEdit().text()

    def setText(self, text):
        """Set text"""
        self.setCurrentText(text)
