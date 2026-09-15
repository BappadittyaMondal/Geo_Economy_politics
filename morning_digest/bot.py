"""
Stage B: Telegram Digest Formatter & Publisher.
Formats ranked strategic news into Telegram-compliant Markdown chunks (under 4096 chars)
and publishes to a configured Telegram channel or chat via the Telegram Bot API.
Supports offline/dry-run mode for local verification without API credentials.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from typing import Any, Dict, List, Optional
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
try:
    from .ranker import StrategicNewsRanker
except (ImportError, ValueError):
    from morning_digest.ranker import StrategicNewsRanker
from geo_engine.lenses import LENS_REGISTRY

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class TelegramDigestPublisher:
    """Formats and dispatches morning strategic news briefings to Telegram."""

    TELEGRAM_API_BASE = "https://api.telegram.org/bot"

    @classmethod
    def format_telegram_digest(
        cls,
        ranked_items: List[Dict[str, Any]],
        date_str: Optional[str] = None
    ) -> List[str]:
        """
        Formats ranked items into Telegram Markdown messages.
        Partitions output into message chunks conforming to Telegram's 4096 character limit.
        """
        today = date_str or datetime.now().strftime("%d %b %Y")
        header = (
            f"🌐 *BHARAT STRATEGIC MORNING BRIEFING* | {today}\n"
            f"_Curated via {len(LENS_REGISTRY)}-Lens Matrix & Epistemic Truth Hierarchy_\n"
            f"{'═'*38}\n\n"
        )

        chunks = []
        current_chunk = header
        item_counter = 1

        for item in ranked_items:
            priority_tag = "🔴 [HIGH-SIGNAL]" if item["requires_deep_dive"] else "🔹"
            category = item["category"]
            score = int(item["strategic_score"] * 100)
            headline = item["headline"]
            if len(headline) > 2000:
                headline = headline[:1997] + "..."
            source = item["source"]

            entry = (
                f"{item_counter}. {priority_tag} *[{category}]* (Score: {score}%)\n"
                f"   {headline}\n"
                f"   _Source: {source}_\n\n"
            )

            # Check chunk size limit (leave buffer for footer)
            if len(current_chunk) + len(entry) > 3900:
                current_chunk += f"*(Continued in Part {len(chunks)+2}...)*"
                chunks.append(current_chunk)
                current_chunk = f"🌐 *STRATEGIC BRIEFING (Part {len(chunks)+1})* | {today}\n{'═'*38}\n\n" + entry
            else:
                current_chunk += entry

            item_counter += 1

        if current_chunk:
            current_chunk += f"{'═'*38}\n_End of Strategic Briefing. Total Items: {len(ranked_items)}._"
            chunks.append(current_chunk)

        return chunks

    @classmethod
    def send_to_telegram(
        cls,
        message: str,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None
    ) -> bool:
        """Sends an atomic text chunk to Telegram using the HTTP API."""
        token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID")

        if not token or not chat:
            print("[DRY-RUN / NOTICE] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured in environment.")
            return False

        url = f"{cls.TELEGRAM_API_BASE}{token}/sendMessage"
        payload = {
            "chat_id": chat,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except urllib.error.HTTPError as e:
            print(f"[ERROR] Failed to publish message chunk to Telegram: HTTP {e.code} {e.reason}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[ERROR] Failed to publish message chunk to Telegram: {type(e).__name__}", file=sys.stderr)
            return False

    @classmethod
    def publish_morning_digest(
        cls,
        top_n: int = 50,
        dry_run: bool = False
    ) -> List[str]:
        """
        Full automated pipeline: Ranks live news, formats Telegram chunks, and sends (or prints in dry-run).
        """
        ranked = StrategicNewsRanker.rank_headlines(top_n=top_n)
        chunks = cls.format_telegram_digest(ranked)

        if dry_run or not os.environ.get("TELEGRAM_BOT_TOKEN"):
            print(f"\n[DRY-RUN] Generated {len(chunks)} message chunk(s) for {len(ranked)} ranked stories:\n")
            for i, chunk in enumerate(chunks, 1):
                print(f"--- TELEGRAM MESSAGE CHUNK {i} ({len(chunk)} chars) ---")
                print(chunk)
                print()
            return chunks

        all_delivered = True
        for chunk in chunks:
            ok = cls.send_to_telegram(chunk)
            if not ok:
                all_delivered = False

        cls.last_delivery_success = all_delivered
        if not all_delivered:
            print("[ERROR] Failed to deliver one or more Telegram message chunks.", file=sys.stderr)
        return chunks


def build_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Morning Strategic News Digest & Telegram Publisher")
    parser.add_argument("--top", type=int, default=50, help="Number of ranked headlines to include (default: 50)")
    parser.add_argument("--live", action="store_true", default=False, help="Execute live dispatch to configured Telegram API channel")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Force dry-run inspection mode without sending to Telegram")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    dry_run_mode = not args.live or args.dry_run
    if not dry_run_mode and not os.environ.get("TELEGRAM_BOT_TOKEN"):
        print("[ERROR] TELEGRAM_BOT_TOKEN environment variable is missing for live dispatch.", file=sys.stderr)
        sys.exit(1)

    chunks = TelegramDigestPublisher.publish_morning_digest(top_n=args.top, dry_run=dry_run_mode)
    if not dry_run_mode and not getattr(TelegramDigestPublisher, "last_delivery_success", True):
        sys.exit(1)



if __name__ == "__main__":
    main()
