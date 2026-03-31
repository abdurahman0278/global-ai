import easyocr
import torch
from PIL import Image
import re
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.device = self._get_device()
        logger.info(f"Initializing EasyOCR with device: {self.device}")
        self.reader = easyocr.Reader(["en"], gpu=self.device != "cpu")
        logger.info("EasyOCR initialized successfully")

    def _get_device(self) -> str:
        """Detect and return the best available device for OCR processing."""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using EasyOCR with GPU acceleration if available."""
        try:
            result = self.reader.readtext(image_path)
            # Combine all detected text with spaces
            text = " ".join([detection[1] for detection in result])
            logger.info(f"Extracted text from {image_path}: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            return ""

    def parse_handwritten_data(self, text: str) -> Dict[str, str]:
        text = text.lower()

        first_name = self._extract_field(text, ['first name', 'firstname', 'name'])
        last_name = self._extract_field(text, ['last name', 'lastname', 'surname'])
        nationality = self._extract_field(text, ['nationality', 'country', 'nation'])
        dob = self._extract_date(text)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'nationality': nationality,
            'date_of_birth': dob
        }

    def _extract_field(self, text: str, keywords: list) -> str:
        """Extract field value using multiple keyword patterns."""
        for keyword in keywords:
            # Try pattern with colon/space separator
            pattern = rf"{keyword}[:\s]+([a-zA-Z\s]+?)(?:\s+(?:last|first|nationality|date|dob|birth|\d|$))"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Clean up common OCR artifacts
                value = re.sub(r"[^a-zA-Z\s]", "", value)
                return value.strip().title()
        return ''

    def _extract_date(self, text: str) -> str:
        """Extract date of birth using various date patterns."""
        date_patterns = [
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",  # DD/MM/YYYY or MM/DD/YYYY
            r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",  # YYYY-MM-DD
            r"\b(\d{1,2}\s+[a-zA-Z]{3,9}\s+\d{4})\b",  # DD Month YYYY
            r"\b(\d{2}\s*[.]\s*\d{2}\s*[.]\s*\d{4})\b",  # DD.MM.YYYY
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Normalize the date format
                date_str = match.group(1).strip()
                # Remove extra spaces
                date_str = re.sub(r"\s+", " ", date_str)
                return date_str
        return ''
