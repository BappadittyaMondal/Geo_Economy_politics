"""
geo_engine.verification.sanitizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Security hardening: Prompt injection defense, control sequence stripping,
and untrusted evidence encapsulation for external feeds and content.
"""

import re
from typing import Tuple


class EvidenceSanitizer:
    """Hardened sanitizer for external, untrusted evidence streams and text."""

    MAX_EVIDENCE_LENGTH = 8000  # Prevent memory denial-of-service

    # Patterns commonly used in prompt-injection attacks
    INJECTION_PATTERNS = [
        re.compile(r"(?i)\bignore\s+(?:all\s+)?previous\s+(?:instructions|directions|prompts)\b"),
        re.compile(r"(?i)\bsystem\s+prompt\s+override\b"),
        re.compile(r"(?i)\byou\s+are\s+now\s+in\s+developer\s+mode\b"),
        re.compile(r"(?i)\bprint\s+(?:all\s+)?(?:api\s+keys?|secrets?|passwords?|tokens?)\b"),
        re.compile(r"(?i)\bexecute\s+(?:arbitrary\s+)?code\s+as\s+root\b"),
        re.compile(r"(?i)<\s*script[^>]*>.*?</\s*script\s*>"),
    ]

    @classmethod
    def sanitize_untrusted_text(cls, raw_text: str, source_identifier: str = "EXTERNAL_FEED") -> Tuple[str, bool]:
        """
        Sanitizes untrusted text and wraps it in explicit security delimiters.
        Returns: (sanitized_and_wrapped_text, was_injection_detected)
        """
        if not raw_text:
            return "", False

        # 1. Truncate oversized payload
        truncated = raw_text[:cls.MAX_EVIDENCE_LENGTH]

        # 2. Scan for prompt injection directives
        injection_detected = False
        clean_text = truncated
        for pattern in cls.INJECTION_PATTERNS:
            if pattern.search(clean_text):
                injection_detected = True
                clean_text = pattern.sub("[REDACTED_ADVERSARIAL_INJECTION_DIRECTIVE]", clean_text)

        # 3. Strip null bytes and non-printable control characters
        clean_text = "".join(ch for ch in clean_text if ch == "\n" or ch == "\t" or (ch >= " " and ch != "\x7f"))

        # 4. Encapsulate in strict untrusted evidence boundary
        encapsulated = f'<UNTRUSTED_EXTERNAL_EVIDENCE source="{source_identifier}">\n{clean_text.strip()}\n</UNTRUSTED_EXTERNAL_EVIDENCE>'

        return encapsulated, injection_detected
