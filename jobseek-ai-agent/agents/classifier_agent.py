from __future__ import annotations

from typing import Any, Dict, Tuple

from config.constants import AI_KEYWORDS, NON_TARGET_ROLE_KEYWORDS
from config.settings import Settings


class ClassifierAgent:
    """
    Classifies whether a job posting belongs to the target AI Engineer domain.

    This starter implementation uses rule-based screening.
    Later you can upgrade it to an LLM-based semantic classifier.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def classify(self, job: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Return:
            (is_target_role, reason)
        """
        text = self._compose_text(job)

        if not text.strip():
            return False, "Empty job content."

        non_target_hits = [kw for kw in NON_TARGET_ROLE_KEYWORDS if kw.lower() in text]
        ai_hits = [kw for kw in AI_KEYWORDS if kw.lower() in text]

        if non_target_hits and not ai_hits:
            return False, f"Non-target role keywords detected: {', '.join(non_target_hits[:5])}"

        if ai_hits:
            return True, f"AI-related keywords detected: {', '.join(ai_hits[:8])}"

        return False, "No strong AI-related evidence found."

    @staticmethod
    def _compose_text(job: Dict[str, Any]) -> str:
        """
        Concatenate searchable fields for classification.
        """
        fields = [
            str(job.get("title", "")),
            str(job.get("requirements", "")),
            str(job.get("description", "")),
            " ".join(job.get("tech_tags", [])) if isinstance(job.get("tech_tags"), list) else "",
        ]
        return " ".join(fields).strip().lower()
