"""
Main PyQt6 GUI application for Seed-X Translation
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QSplitter,
    QListWidget,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QProgressBar,
    QStatusBar,
    QToolBar,
    QDockWidget,
    QListWidgetItem,
    QComboBox,
)
from PyQt6.QtCore import Qt, QSettings, QTimer
from PyQt6.QtGui import QAction

from src.utils.config import LANGUAGES, UI_CONFIG, GENERATION_CONFIG, DEFAULT_MODEL_PATH
from src.gui.filterable_combobox import FilterableComboBox
from src.backend.translation_backend import TranslationManager


class TranslatorMainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.manager = TranslationManager()
        self.settings = QSettings("SeedX", "Translator")
        self.init_ui()
        self.load_settings()
        self.try_autoload_model()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Seed-X Translation - PyQt6")
        self.setGeometry(100, 100, UI_CONFIG["window_width"], UI_CONFIG["window_height"])

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create menu bar
        self.create_menu_bar()

        # Create toolbar
        self.create_toolbar()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Model controls
        model_group = self.create_model_controls()
        main_layout.addWidget(model_group)

        # Language selection
        lang_group = self.create_language_controls()
        main_layout.addWidget(lang_group)

        # Translation area
        translation_widget = self.create_translation_area()
        main_layout.addWidget(translation_widget, stretch=1)

        # Settings dock
        self.create_settings_dock()

        # History dock
        self.create_history_dock()

    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        load_model_action = QAction("Load Model", self)
        load_model_action.setShortcut("Ctrl+O")
        load_model_action.triggered.connect(self.browse_model)
        file_menu.addAction(load_model_action)

        file_menu.addSeparator()

        save_history_action = QAction("Save History", self)
        save_history_action.setShortcut("Ctrl+S")
        save_history_action.triggered.connect(self.save_history)
        file_menu.addAction(save_history_action)

        load_history_action = QAction("Load History", self)
        load_history_action.triggered.connect(self.load_history)
        file_menu.addAction(load_history_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        clear_input_action = QAction("Clear Input", self)
        clear_input_action.triggered.connect(lambda: self.input_text.clear())
        edit_menu.addAction(clear_input_action)

        clear_output_action = QAction("Clear Output", self)
        clear_output_action.triggered.connect(lambda: self.output_text.clear())
        edit_menu.addAction(clear_output_action)

        edit_menu.addSeparator()

        copy_output_action = QAction("Copy Output", self)
        copy_output_action.setShortcut("Ctrl+Shift+C")
        copy_output_action.triggered.connect(self.copy_output)
        edit_menu.addAction(copy_output_action)

        # View menu
        view_menu = menubar.addMenu("View")

        self.show_settings_action = QAction("Settings Panel", self, checkable=True)
        self.show_settings_action.setChecked(True)
        self.show_settings_action.triggered.connect(self.toggle_settings_dock)
        view_menu.addAction(self.show_settings_action)

        self.show_history_action = QAction("History Panel", self, checkable=True)
        self.show_history_action.setChecked(True)
        self.show_history_action.triggered.connect(self.toggle_history_dock)
        view_menu.addAction(self.show_history_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Load model button
        load_action = QAction("Load Model", self)
        load_action.triggered.connect(self.browse_model)
        toolbar.addAction(load_action)

        toolbar.addSeparator()

        # Translate button
        translate_action = QAction("Translate", self)
        translate_action.triggered.connect(self.translate)
        toolbar.addAction(translate_action)

        # Clear button
        clear_action = QAction("Clear All", self)
        clear_action.triggered.connect(self.clear_all)
        toolbar.addAction(clear_action)

        toolbar.addSeparator()

        # Swap languages button
        swap_action = QAction("Swap Languages", self)
        swap_action.triggered.connect(self.swap_languages)
        toolbar.addAction(swap_action)

    def create_model_controls(self) -> QGroupBox:
        """Create model loading controls"""
        group = QGroupBox("Model")
        layout = QHBoxLayout()

        # Backend selection
        backend_label = QLabel("Backend:")
        self.backend_combo = QComboBox()
        backends = ["GGUF (llama.cpp)", "Original (Transformers)"]
        self.backend_combo.addItems(backends)
        self.backend_combo.setCurrentIndex(0)
        self.backend_combo.currentIndexChanged.connect(self.on_backend_changed)
        layout.addWidget(backend_label)
        layout.addWidget(self.backend_combo)

        self.model_path_label = QLabel("No model loaded")
        self.model_path_label.setStyleSheet("QLabel { color: #666; }")
        layout.addWidget(self.model_path_label, stretch=1)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_model)
        layout.addWidget(self.browse_button)

        self.load_button = QPushButton("Load Model")
        self.load_button.clicked.connect(self.load_model)
        self.load_button.setEnabled(False)
        layout.addWidget(self.load_button)

        self.download_button = QPushButton("Download Model")
        self.download_button.clicked.connect(self.download_model)
        layout.addWidget(self.download_button)

        self.model_progress = QProgressBar()
        self.model_progress.setMaximum(0)
        self.model_progress.hide()
        layout.addWidget(self.model_progress)

        group.setLayout(layout)
        return group

    def create_language_controls(self) -> QGroupBox:
        """Create language selection controls"""
        group = QGroupBox("Language Settings")
        layout = QHBoxLayout()

        # Source language
        layout.addWidget(QLabel("From:"))
        self.source_lang = FilterableComboBox()
        self.source_lang.addItems(list(LANGUAGES.keys()))
        self.source_lang.setCurrentText("English")
        layout.addWidget(self.source_lang, stretch=1)

        # Swap button
        self.swap_button = QPushButton("⇄")
        self.swap_button.setMaximumWidth(40)
        self.swap_button.clicked.connect(self.swap_languages)
        layout.addWidget(self.swap_button)

        # Target language
        layout.addWidget(QLabel("To:"))
        self.target_lang = FilterableComboBox()
        self.target_lang.addItems(list(LANGUAGES.keys()))
        self.target_lang.setCurrentText("Polish")
        layout.addWidget(self.target_lang, stretch=1)

        # Chain-of-Thought checkbox
        self.cot_checkbox = QCheckBox("Chain-of-Thought (Detailed)")
        self.cot_checkbox.setToolTip("Enable detailed translation with explanations")
        layout.addWidget(self.cot_checkbox)

        group.setLayout(layout)
        return group

    def create_translation_area(self) -> QWidget:
        """Create the main translation input/output area"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Create splitter for input and output
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Input area
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.addWidget(QLabel("Input Text:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to translate...")
        input_layout.addWidget(self.input_text)
        splitter.addWidget(input_widget)

        # Output area
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.addWidget(QLabel("Translation:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translation will appear here...")
        output_layout.addWidget(self.output_text)
        splitter.addWidget(output_widget)

        # Set equal sizes
        splitter.setSizes([600, 600])
        layout.addWidget(splitter)

        # Translation button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.translate_button = QPushButton("Translate")
        self.translate_button.setMinimumHeight(40)
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #0084ff;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #0066cc;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.translate_button.clicked.connect(self.translate)
        self.translate_button.setEnabled(False)
        button_layout.addWidget(self.translate_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        return widget

    def create_settings_dock(self):
        """Create the settings dock widget"""
        self.settings_dock = QDockWidget("Generation Settings", self)
        self.settings_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Temperature
        settings_layout.addWidget(QLabel("Temperature:"))
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(GENERATION_CONFIG["temperature"])
        settings_layout.addWidget(self.temperature_spin)

        # Max tokens
        settings_layout.addWidget(QLabel("Max Tokens:"))
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(1, 2048)
        self.max_tokens_spin.setValue(GENERATION_CONFIG["max_tokens"])
        settings_layout.addWidget(self.max_tokens_spin)

        # Top-p
        settings_layout.addWidget(QLabel("Top-p:"))
        self.top_p_spin = QDoubleSpinBox()
        self.top_p_spin.setRange(0.0, 1.0)
        self.top_p_spin.setSingleStep(0.05)
        self.top_p_spin.setValue(GENERATION_CONFIG["top_p"])
        settings_layout.addWidget(self.top_p_spin)

        # Top-k
        settings_layout.addWidget(QLabel("Top-k:"))
        self.top_k_spin = QSpinBox()
        self.top_k_spin.setRange(1, 100)
        self.top_k_spin.setValue(GENERATION_CONFIG["top_k"])
        settings_layout.addWidget(self.top_k_spin)

        # Repeat penalty
        settings_layout.addWidget(QLabel("Repeat Penalty:"))
        self.repeat_penalty_spin = QDoubleSpinBox()
        self.repeat_penalty_spin.setRange(0.0, 2.0)
        self.repeat_penalty_spin.setSingleStep(0.1)
        self.repeat_penalty_spin.setValue(GENERATION_CONFIG["repeat_penalty"])
        settings_layout.addWidget(self.repeat_penalty_spin)

        # Apply button
        apply_button = QPushButton("Apply Settings")
        apply_button.clicked.connect(self.apply_settings)
        settings_layout.addWidget(apply_button)

        # Reset button
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_settings)
        settings_layout.addWidget(reset_button)

        settings_layout.addStretch()

        self.settings_dock.setWidget(settings_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.settings_dock)

    def create_history_dock(self):
        """Create the history dock widget"""
        self.history_dock = QDockWidget("Translation History", self)
        self.history_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.load_from_history)
        history_layout.addWidget(self.history_list)

        # History controls
        history_controls = QHBoxLayout()

        clear_history_button = QPushButton("Clear")
        clear_history_button.clicked.connect(self.clear_history)
        history_controls.addWidget(clear_history_button)

        export_history_button = QPushButton("Export")
        export_history_button.clicked.connect(self.save_history)
        history_controls.addWidget(export_history_button)

        history_layout.addLayout(history_controls)

        self.history_dock.setWidget(history_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.history_dock)

    def on_backend_changed(self):
        """Switch backend"""
        backend_text = self.backend_combo.currentText()
        self.manager.switch_backend(backend_text)

        # Reset UI state
        self.model_path_label.setText("No model loaded")
        self.translate_button.setEnabled(False)
        self.load_button.setEnabled(False)

    def browse_model(self):
        """Browse for a model path depending on backend"""
        backend_text = self.backend_combo.currentText()

        if "GGUF" in backend_text:
            # llama.cpp backend: select GGUF file
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select GGUF Model", DEFAULT_MODEL_PATH, "GGUF Models (*.gguf);;All Files (*.*)"
            )
            if file_path:
                # Block BF16 GGUF on llama.cpp backend (known to crash on Windows)
                if "bf16" in os.path.basename(file_path).lower():
                    QMessageBox.critical(
                        self,
                        "Unsupported GGUF format",
                        "BF16 GGUF models are unstable on Windows with llama.cpp and may crash.\n\n"
                        "Recommended:\n"
                        "  1) Download a quantized GGUF like Q4_K_M, OR\n"
                        "  2) Switch Backend to 'Original (Transformers)' and use the HF model",
                    )
                    return
                self.model_path_label.setText(file_path)
                self.load_button.setEnabled(True)
        else:
            # Transformers backend: select model directory (HuggingFace format)
            dir_path = QFileDialog.getExistingDirectory(self, "Select HF Model Directory", DEFAULT_MODEL_PATH)
            if dir_path:
                self.model_path_label.setText(dir_path)
                self.load_button.setEnabled(True)

    def load_model(self):
        """Load the selected model using manager"""
        model_path = self.model_path_label.text()
        if model_path == "No model loaded":
            QMessageBox.warning(self, "Warning", "Please select a model file first.")
            return

        # Disable controls during loading
        self.load_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.translate_button.setEnabled(False)
        self.model_progress.show()

        self.load_thread = self.manager.load_model(model_path, self.update_status, self.on_model_loaded)

    def on_model_loaded(self, success: bool):
        """Handle model loading completion"""
        self.model_progress.hide()
        self.browse_button.setEnabled(True)
        self.load_button.setEnabled(True)

        if success:
            self.translate_button.setEnabled(True)
            self.status_bar.showMessage("Model loaded successfully!")
            self.model_path_label.setStyleSheet("QLabel { color: green; }")

            # Show model info
            info = self.manager.get_model_info()
            details = []
            path_display = Path(info.get("path", "")).name if info.get("path") else "N/A"
            details.append(f"Model: {path_display}")
            if "backend" in info:
                details.append(f"Backend: {info.get('backend')}")
            if "context_size" in info:
                details.append(f"Context Size: {info.get('context_size')}")
            if "gpu_layers" in info:
                details.append(f"GPU Layers: {info.get('gpu_layers')}")
            if "threads" in info:
                details.append(f"Threads: {info.get('threads')}")
            QMessageBox.information(self, "Model Loaded", "\n".join(details))
        else:
            self.status_bar.showMessage("Failed to load model")
            self.model_path_label.setStyleSheet("QLabel { color: red; }")
            err = "Failed to load the model. Please check the file and try again."
            if hasattr(self.manager.model, "last_error") and getattr(self.manager.model, "last_error"):
                err += f"\n\nDetails:\n{self.manager.model.last_error}"
            QMessageBox.critical(self, "Error", err)

    def translate(self):
        """Perform translation using manager"""
        if not self.manager.is_model_loaded():
            QMessageBox.warning(self, "Warning", "Please load a model first.")
            return

        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to translate.")
            return

        # Get settings
        settings = {
            "temperature": self.temperature_spin.value(),
            "max_tokens": self.max_tokens_spin.value(),
            "top_p": self.top_p_spin.value(),
            "top_k": self.top_k_spin.value(),
            "repeat_penalty": self.repeat_penalty_spin.value(),
        }

        # Disable translate button during translation
        self.translate_button.setEnabled(False)
        self.output_text.clear()
        self.output_text.setPlainText("Translating...")

        self.translation_thread = self.manager.translate(
            text,
            self.source_lang.text(),
            self.target_lang.text(),
            self.cot_checkbox.isChecked(),
            settings,
            self.on_translation_complete,
            self.on_translation_error,
            self.update_status,
        )

    def on_translation_complete(self, translation: str):
        """Handle translation completion"""
        self.output_text.setPlainText(translation)
        self.translate_button.setEnabled(True)
        self.status_bar.showMessage("Translation complete!")

        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = {
            "timestamp": timestamp,
            "source_lang": self.source_lang.text(),
            "target_lang": self.target_lang.text(),
            "input": self.input_text.toPlainText()[:50] + "...",
            "output": translation[:50] + "...",
            "full_input": self.input_text.toPlainText(),
            "full_output": translation,
        }
        self.manager.add_to_history(history_entry)
        self.update_history_list()

    def on_translation_error(self, error: str):
        """Handle translation error"""
        self.output_text.setPlainText(f"Error: {error}")
        self.translate_button.setEnabled(True)
        self.status_bar.showMessage("Translation failed")
        QMessageBox.critical(self, "Translation Error", f"An error occurred: {error}")

    def update_history_list(self):
        """Update the history list widget from manager's history"""
        self.history_list.clear()
        for entry in self.manager.get_history():
            item_text = f"[{entry['timestamp']}] {entry['source_lang']} → {entry['target_lang']}: {entry['input']}"
            item = QListWidgetItem(item_text)
            self.history_list.addItem(item)

    def load_from_history(self, item: QListWidgetItem):
        """Load a translation from history"""
        index = self.history_list.row(item)
        history = self.manager.get_history()
        if 0 <= index < len(history):
            entry = history[index]
            self.input_text.setPlainText(entry["full_input"])
            self.output_text.setPlainText(entry["full_output"])

            # Set languages
            self.source_lang.setText(entry["source_lang"])
            self.target_lang.setText(entry["target_lang"])

    def clear_history(self):
        """Clear translation history"""
        self.manager.clear_history()
        self.history_list.clear()

    def save_history(self):
        """Save translation history to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save History", "translation_history.json", "JSON Files (*.json);;All Files (*.*)"
        )

        if file_path:
            if self.manager.save_history(file_path):
                QMessageBox.information(self, "Success", "History saved successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save history")

    def load_history(self):
        """Load translation history from file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load History", "", "JSON Files (*.json);;All Files (*.*)")

        if file_path:
            if self.manager.load_history(file_path):
                self.update_history_list()
                QMessageBox.information(self, "Success", "History loaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to load history")

    def swap_languages(self):
        """Swap source and target languages"""
        source_text = self.source_lang.text()
        target_text = self.target_lang.text()
        self.source_lang.setText(target_text)
        self.target_lang.setText(source_text)

        # Also swap the text if there's a translation
        if self.output_text.toPlainText():
            input_text = self.input_text.toPlainText()
            output_text = self.output_text.toPlainText()
            self.input_text.setPlainText(output_text)
            self.output_text.setPlainText(input_text)

    def clear_all(self):
        """Clear input and output text"""
        self.input_text.clear()
        self.output_text.clear()

    def copy_output(self):
        """Copy output text to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        self.status_bar.showMessage("Translation copied to clipboard", 2000)

    def apply_settings(self):
        """Apply generation settings"""
        settings = {
            "temperature": self.temperature_spin.value(),
            "max_tokens": self.max_tokens_spin.value(),
            "top_p": self.top_p_spin.value(),
            "top_k": self.top_k_spin.value(),
            "repeat_penalty": self.repeat_penalty_spin.value(),
        }
        self.manager.update_settings(settings)
        self.status_bar.showMessage("Settings applied", 2000)

    def reset_settings(self):
        """Reset settings to defaults"""
        self.temperature_spin.setValue(GENERATION_CONFIG["temperature"])
        self.max_tokens_spin.setValue(GENERATION_CONFIG["max_tokens"])
        self.top_p_spin.setValue(GENERATION_CONFIG["top_p"])
        self.top_k_spin.setValue(GENERATION_CONFIG["top_k"])
        self.repeat_penalty_spin.setValue(GENERATION_CONFIG["repeat_penalty"])
        self.apply_settings()

    def toggle_settings_dock(self):
        """Toggle settings dock visibility"""
        self.settings_dock.setVisible(self.show_settings_action.isChecked())

    def toggle_history_dock(self):
        """Toggle history dock visibility"""
        self.history_dock.setVisible(self.show_history_action.isChecked())

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.showMessage(message)

    def download_model(self):
        """Download model automatically"""
        from PyQt6.QtWidgets import QDialog, QRadioButton, QButtonGroup

        dialog = QDialog(self)
        dialog.setWindowTitle("Download Model")
        dialog.setModal(True)
        dialog.resize(500, 300)

        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel("Choose model to download:"))

        # Radio buttons for model selection
        self.model_group = QButtonGroup()

        # GGUF models
        layout.addWidget(QLabel("\nGGUF Models (for llama.cpp backend):"))

        q4_radio = QRadioButton("Q4_K_M (4.6GB) - Recommended balance of quality/speed")
        q4_radio.setChecked(True)
        self.model_group.addButton(q4_radio, 0)
        layout.addWidget(q4_radio)

        q5_radio = QRadioButton("Q5_K_M (5.4GB) - Better quality, slower")
        self.model_group.addButton(q5_radio, 1)
        layout.addWidget(q5_radio)

        q8_radio = QRadioButton("Q8_0 (8.0GB) - Best quality, requires more RAM")
        self.model_group.addButton(q8_radio, 2)
        layout.addWidget(q8_radio)

        # Original model
        layout.addWidget(QLabel("\nOriginal Model for Transformers backend:"))

        original_radio = QRadioButton("Original Seed-X-PPO-7B (15GB) - Full precision")
        self.model_group.addButton(original_radio, 3)
        layout.addWidget(original_radio)

        # Buttons
        button_layout = QHBoxLayout()

        download_btn = QPushButton("Download")
        download_btn.clicked.connect(lambda: self.start_download(dialog))
        button_layout.addWidget(download_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        dialog.exec()

    def start_download(self, dialog):
        """Start the model download"""
        dialog.accept()

        selected_id = self.model_group.checkedId()

        models = {
            0: ("Q4_K_M", "Mungert/Seed-X-PPO-7B-GGUF", "Seed-X-PPO-7B-q4_k_m.gguf"),
            1: ("Q5_K_M", "Mungert/Seed-X-PPO-7B-GGUF", "Seed-X-PPO-7B-q5_k_m.gguf"),
            2: ("Q8_0", "Mungert/Seed-X-PPO-7B-GGUF", "Seed-X-PPO-7B-q8_0.gguf"),
            3: ("Original", "ByteDance-Seed/Seed-X-PPO-7B", None),
        }

        if selected_id in models:
            model_name, repo_id, filename = models[selected_id]

            # Show progress dialog
            from PyQt6.QtWidgets import QProgressDialog

            progress = QProgressDialog(f"Downloading {model_name}...", "Cancel", 0, 0, self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.show()

            # Use manager's download_model method
            self.download_thread = self.manager.download_model(
                repo_id,
                filename,
                progress.setLabelText,
                lambda success, path: self.on_download_complete(success, path, progress),
            )

    def on_download_complete(self, success, model_path, progress_dialog):
        """Handle download completion"""
        progress_dialog.close()

        if success:
            QMessageBox.information(self, "Download Complete", f"Model downloaded successfully!\n\nPath: {model_path}")
            self.model_path_label.setText(model_path)
            self.load_button.setEnabled(True)

            # Auto-switch backend if needed
            if model_path.endswith(".gguf"):
                self.backend_combo.setCurrentIndex(0)  # GGUF backend
            else:
                # Find the Transformers backend index
                for i in range(self.backend_combo.count()):
                    if "Transformers" in self.backend_combo.itemText(i):
                        self.backend_combo.setCurrentIndex(i)
                        break
        else:
            QMessageBox.critical(
                self, "Download Failed", "Failed to download the model. Please check your internet connection and try again."
            )

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Seed-X Translator",
            "Seed-X Translation GUI\n\n"
            "A PyQt6 application for using the Seed-X-PPO-7B GGUF translation model.\n\n"
            "Supports translation between 28 languages with state-of-the-art quality.\n\n"
            "Version 1.0.0",
        )

    def load_settings(self):
        """Load saved application settings"""
        # Window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Window state
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)

        # Last model path
        last_model = self.settings.value("lastModel", "")
        if last_model and os.path.exists(last_model):
            # If current backend is llama.cpp and saved path is BF16 GGUF, do not auto-enable load
            if (
                self.backend_combo.currentIndex() == 0
                and last_model.lower().endswith(".gguf")
                and "bf16" in os.path.basename(last_model).lower()
            ):
                self.model_path_label.setText("No model loaded")
                self.load_button.setEnabled(False)
            else:
                self.model_path_label.setText(last_model)
                self.load_button.setEnabled(True)

        # Language preferences
        source_lang = self.settings.value("sourceLang", "English")
        target_lang = self.settings.value("targetLang", "Polish")
        self.source_lang.setText(source_lang)
        self.target_lang.setText(target_lang)

        # Load history if exists (optional, can be added)

    def find_preferred_model_path(self) -> Optional[str]:
        """Find a preferred GGUF model path under models/"""
        try:
            preferred = os.path.abspath(os.path.join("models", "Seed-X-PPO-7B-q4_k_m.gguf"))
            if os.path.exists(preferred) and os.path.getsize(preferred) > 1024:
                return preferred
            candidates = []
            for root, _, files in os.walk("models"):
                for f in files:
                    if f.lower().endswith(".gguf") and "bf16" not in f.lower():
                        full = os.path.abspath(os.path.join(root, f))
                        try:
                            size = os.path.getsize(full)
                        except Exception:
                            size = 0
                        candidates.append((size, full))
            if candidates:
                candidates.sort(reverse=True)  # largest first
                return candidates[0][1]
        except Exception:
            pass
        return None

    def try_autoload_model(self):
        """Auto-detect and load a model on startup"""
        if self.model_path_label.text() == "No model loaded":
            path = self.find_preferred_model_path()
            if path:
                self.model_path_label.setText(path)
                self.load_button.setEnabled(True)
                QTimer.singleShot(200, self.load_model)

    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        if self.model_path_label.text() != "No model loaded":
            self.settings.setValue("lastModel", self.model_path_label.text())

        self.settings.setValue("sourceLang", self.source_lang.text())
        self.settings.setValue("targetLang", self.target_lang.text())

    def closeEvent(self, event):
        """Handle application close event"""
        self.save_settings()

        if self.manager.is_model_loaded():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "The model is still loaded. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.manager.unload_model()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Seed-X Translator")
    app.setOrganizationName("SeedX")

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = TranslatorMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
