"""
instagram-tiktok-agent-skill: Run an entire Instagram Reels & TikTok channel with 11 AI Agent Skills + CLI Engine.
"""

from .engine import (
    HOOK_FORMULAS_21,
    score_shortform_hook,
    check_cover_and_hook_alignment,
    generate_transcript_cut_list,
    diagnose_retention_dropoff,
)

__version__ = "1.0.0"
__all__ = [
    "HOOK_FORMULAS_21",
    "score_shortform_hook",
    "check_cover_and_hook_alignment",
    "generate_transcript_cut_list",
    "diagnose_retention_dropoff",
]
