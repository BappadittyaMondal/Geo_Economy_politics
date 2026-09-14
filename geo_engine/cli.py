"""
CLI Interface for the Geo-Engine.
Renders 5-tier summit intelligence reports with rich formatting, tables,
and epistemic audit logs for strategic decision-makers.
"""

import sys
import re
import argparse
from typing import Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .core.models import SummitEvent, StrategicEvent, TemporalMode
from .core.query_parser import QueryParser, StrategicQuery
from .ingestion import GDELTClient, SovereignRSSClient, IngestionNormalizer
from .forecasting import ForecastingEngine, BrierScorer
from .arbitration import SummitSynthesizer, PersonaNarrator
from .storage.event_store import EventStore
from .lenses import (
    LENS_REGISTRY,
    DeepTechLens,
    HistoryLens,
    CivilizationalLens,
    GeoEconomistLens,
    GeopoliticalLens,
    KinesicsLens,
    CashFlowLens,
    PropagandaLens,
    PetroLogisticsLens,
    BureaucraticInertiaLens,
    DigitalSovereigntyLens,
    HybridCovertLens,
    IndiaTimelineLens,
    DemographicInfiltrationLens,
    CriticalMineralsLens,
    InstitutionalLawfareLens,
)


if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(safe_box=True)


def render_full_report(
    summit_name: str = "BRICS 2026 Summit",
    year: int = 2026,
    persona: str = "neutral",
    target_event: Optional[Union[SummitEvent, StrategicEvent]] = None
):
    """Generates and renders the complete 5-tier report using rich terminal formatting."""
    if target_event is not None:
        summit = target_event
    else:
        summit = SummitEvent(
            summit_name=summit_name,
            year=year,
            host_country="India",
            location="New Delhi",
            member_countries=[
                "India", "China", "Russia", "Brazil", "South Africa",
                "Iran", "Saudi Arabia", "UAE", "Egypt", "Ethiopia"
            ]
        )

    report = SummitSynthesizer.synthesize_report(summit)

    # Header Panel
    event_title = getattr(report.event, "summit_name", "") or getattr(report.event, "title", "Strategic Event")
    host_info = getattr(report.event, "host_country", getattr(report.event, "primary_region", "Multilateral"))
    loc_info = getattr(report.event, "location", "N/A")
    console.print(Panel(
        f"[bold cyan]{event_title} ({report.event.year})[/bold cyan]\n"
        f"[yellow]Host / Region:[/yellow] {host_info} ({loc_info}) | "
        f"[yellow]Temporal Mode:[/yellow] [bold red]{report.event.temporal_mode.value.upper()}[/bold red] | "
        f"[yellow]Epistemic Confidence:[/yellow] [bold green]{report.overall_confidence_score * 100:.1f}%[/bold green]\n"
        f"[dim]De-sanitized analysis produced by {len(LENS_REGISTRY)}-Lens Matrix & Epistemic Truth Hierarchy[/dim]",
        title="[bold white on blue] GEO-ECONOMIC & GEOPOLITICAL INTELLIGENCE REPORT [/bold white on blue]",
        border_style="cyan"
    ))

    # TIER 1: Negative Space & Communique Diff
    console.print("\n[bold yellow]=== TIER 1: COMMUNIQUE DECONSTRUCTION & NEGATIVE SPACE (WHAT WAS DROPPED) ===[/bold yellow]")
    for item in report.negative_space_synopsis:
        if "[CRITICAL OMISSION]" in item:
            console.print(f" [bold red][X][/bold red] [red]{item}[/red]")
        elif "[DILUTION DETECTED]" in item:
            console.print(f" [bold yellow][!][/bold yellow] [yellow]{item}[/yellow]")
        else:
            console.print(f" [bold green][+][/bold green] [green]{item}[/green]")

    # TIER 2: Country-by-Country Ledger Table
    console.print("\n[bold yellow]=== TIER 2: COUNTRY-BY-COUNTRY LEDGER (OPTICS VS REAL YIELD) ===[/bold yellow]")
    country_table = Table(title="Member State Forensic Audit", border_style="bright_blue", show_lines=True)
    country_table.add_column("Country", style="bold white", width=16)
    country_table.add_column("Domestic Optics Narrative", style="cyan", width=26)
    country_table.add_column("Hard Geopolitical Yield", style="green", width=28)
    country_table.add_column("Effective CapEx", style="bold green", width=14)
    country_table.add_column("Vulnerabilities / Concessions", style="red", width=28)
    country_table.add_column("Autonomy", style="magenta", width=10)

    for c in report.country_ledgers:
        country_table.add_row(
            c.country_name,
            c.public_domestic_narrative,
            c.geopolitical_yield,
            f"${c.hard_cash_yield_usd/1e9:.1f}B",
            c.concessions_or_vulnerabilities,
            f"{c.strategic_autonomy_score*100:.0f}%"
        )
    console.print(country_table)

    # TIER 3: Kinesics & Body Language Forensics
    console.print("\n[bold yellow]=== TIER 3: DIPLOMATIC KINESICS & PHOTOCALL FORENSICS (PROTOCOL SUBTRACTED) ===[/bold yellow]")
    kinesic_table = Table(title="Leader Proxemics & Micro-Signals", border_style="magenta", show_lines=True)
    kinesic_table.add_column("Actors", style="bold white", width=22)
    kinesic_table.add_column("Setting", style="yellow", width=18)
    kinesic_table.add_column("Protocol Discount", style="cyan", width=18)
    kinesic_table.add_column("Handshake Vector", style="blue", width=18)
    kinesic_table.add_column("Tension Score", style="red", width=14)
    kinesic_table.add_column("Residual Warmth", style="bold green", width=16)
    kinesic_table.add_column("Forensic Notes", style="dim white", width=30)

    for k in report.kinesic_forensics:
        kinesic_table.add_row(
            f"{k.actor_primary} <-> {k.actor_secondary}",
            k.setting,
            "YES (Mandated)" if k.protocol_mandated else "NO (Spontaneous)",
            k.handshake_torque_vector,
            f"{k.residual_tension_score:.2f}",
            f"{k.genuine_warmth_index:.2f}",
            k.notes or ""
        )
    console.print(kinesic_table)

    # TIER 4: Hard Money & Petro-Logistics Reality Check
    console.print("\n[bold yellow]=== TIER 4: HARD-MONEY & PETRO-LOGISTICS AUDIT (CASH REALITY) ===[/bold yellow]")
    m = report.hard_money_audit
    cash_text = (
        f"[bold cyan]Total Announced Nominal Commitments:[/bold cyan] ${m['total_nominal_announced_usd']/1e9:.1f} Billion USD\n"
        f"[bold green]Effective Verified CapEx (Post-Haircut):[/bold green] ${m['total_effective_capex_usd']/1e9:.1f} Billion USD\n"
        f"[bold red]Haircut Discount Rate:[/bold red] {m['aggregate_haircut_pct']}% (85% haircut on unfinanced MOUs enforced)\n"
        f"[bold yellow]Common Reserve Currency Feasibility:[/bold yellow] [bold red]{m['common_reserve_currency_status']}[/bold red]\n"
        f"[bold cyan]Bilateral Local Currency Settlement Share:[/bold cyan] {m['bilateral_local_currency_clearing_share_pct']}%\n"
        f"[bold green]Physical Crude Diverted to Asia:[/bold green] {m['physical_crude_re_routed_bpd']}\n"
        f"[bold magenta]Shadow Tanker Fleet Dependency:[/bold magenta] {m['shadow_tanker_fleet_pct']}%\n"
        f"[bold red]Western P&I Maritime Reinsurance Bottleneck:[/bold red] {m['western_pi_maritime_insurance_chokepoint_pct']}%"
    )
    console.print(Panel(cash_text, title="Financial Ground Truth vs. Rhetoric", border_style="green"))

    # TIER 5: Strategic Inner Meaning (Civilizational & Geopolitical Synthesis)
    console.print("\n[bold yellow]=== TIER 5: STRATEGIC 'INNER MEANING' (CIVILIZATIONAL SYNTHESIS) ===[/bold yellow]")
    s = report.civilizational_synthesis
    syn_text = (
        f"[bold yellow]The Civilizational Core:[/bold yellow]\n{s['civilizational_core']}\n\n"
        f"[bold yellow]Sanatan Dharmic Statecraft & Rajdharma (Bharat):[/bold yellow]\n{s['sanatan_dharmic_statecraft']}\n\n"
        f"[bold yellow]The Polycentric Strategic Endgame:[/bold yellow]\n{s['strategic_endgame']}"
    )
    console.print(Panel(syn_text, title="The Civilizational & Kautilyan Matrix", border_style="yellow"))

    # Epistemic Arbitration Audit Log
    console.print("\n[bold dim cyan]--- EPISTEMIC TRUTH ARBITRATION AUDIT LOG ---[/bold dim cyan]")
    for entry in report.epistemic_arbitration_log:
        console.print(f"[dim]* {entry}[/dim]")
    console.print()

    # Strategic Persona Archetype Projection
    if persona and persona.lower() != "neutral":
        p_data = PersonaNarrator.apply_persona(report, persona)
        p_recs = "\n".join([f"  [bold green]*[/bold green] {r}" for r in p_data["strategic_recommendations"]])
        p_box = (
            f"[bold cyan]Intellectual Tradition:[/bold cyan] {p_data['archetype_name']}\n"
            f"[bold yellow]Doctrinal Axis:[/bold yellow] {p_data['doctrinal_axis']}\n\n"
            f"[bold white]Executive Takeaway:[/bold white]\n{p_data['executive_takeaway']}\n\n"
            f"[bold green]Key Strategic Recommendations:[/bold green]\n{p_recs}"
        )
        console.print(Panel(p_box, title=f"[bold white on red] STRATEGIC PERSONA PROJECTION: {p_data['archetype_key'].upper()} [/bold white on red]", border_style="red"))
        console.print()


def render_lenses_summary(summit_name: str = "BRICS 2026 Summit"):
    """Displays alignment scores and key findings from all registered lenses."""
    summit = SummitEvent(summit_name=summit_name, year=2026, host_country="India", location="New Delhi")
    table = Table(title=f"The {len(LENS_REGISTRY)}-Lens Analytical Matrix Evaluation", border_style="cyan")
    table.add_column("Lens #", style="bold white", width=6)
    table.add_column("Lens Name", style="bold cyan", width=34)
    table.add_column("Epistemic Tier", style="magenta", width=18)
    table.add_column("Alignment Score", style="green", width=16)
    table.add_column("Confidence", style="yellow", width=12)
    table.add_column("Primary Analytical Finding", style="white", width=45)

    for i, lens in enumerate(LENS_REGISTRY, 1):
        ev = lens.evaluate(summit)
        score_color = "green" if ev.alignment_score > 0.5 else "yellow" if ev.alignment_score > 0.3 else "red"
        table.add_row(
            str(i),
            ev.lens_name,
            ev.primary_epistemic_tier.name,
            f"[{score_color}]{ev.alignment_score:+.2f}[/{score_color}]",
            f"{ev.confidence*100:.0f}%",
            ev.key_findings[0] if ev.key_findings else "N/A"
        )
    console.print(table)


def render_query_pipeline(prompt: str, persona: str = "neutral"):
    """Dynamically parses arbitrary user prompts, ingests open evidence, and executes calibrated forecasting."""
    # 1. Dynamic Query Deconstruction
    query = QueryParser.parse(prompt)

    
    console.print(Panel(
        f"[bold yellow]Prompt Analyzed:[/bold yellow] \"{query.raw_prompt}\"\n\n"
        f"[bold cyan]Target Event:[/bold cyan] {query.target_summit} (Horizon: {query.year}) | "
        f"[bold cyan]Countries Detected:[/bold cyan] {', '.join(query.target_countries) if query.target_countries else 'All 10 Core Member States'}\n"
        f"[bold cyan]Prioritized Lenses:[/bold cyan] {', '.join(query.prioritized_lenses) if query.prioritized_lenses else f'All {len(LENS_REGISTRY)} Lenses Activated'}\n"
        f"[bold cyan]Forensic Modules Required:[/bold cyan] Kinesics: {query.requires_kinesics} | Cash Audit: {query.requires_cash_audit} | Negative Space: {query.requires_negative_space}",
        title="[bold white on green] 1. DYNAMIC STRATEGIC QUERY DECONSTRUCTION [/bold white on green]",
        border_style="green"
    ))

    # 1B. Historical Calendar Mirrors & Anniversary Matching
    month_num = None
    day_num = None
    if query.focal_date:
        m_match = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", query.focal_date.lower())
        d_match = re.search(r"(\d{1,2})", query.focal_date)
        if m_match:
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            month_num = months.index(m_match.group(1)[:3]) + 1
        if d_match:
            day_num = int(d_match.group(1))

    if month_num:
        try:
            store = EventStore()
            annivs = store.match_anniversaries(month_num, day_num)
            if annivs:
                console.print("\n[bold yellow]=== HISTORICAL CALENDAR MIRRORS & CIVILIZATIONAL TURNING POINTS (SQLite) ===[/bold yellow]")
                for a in annivs:
                    console.print(Panel(
                        f"[bold cyan]Historical Event:[/bold cyan] {a['event_title']} ({a['year']} AD) | [yellow]Region:[/yellow] {a['region']}\n"
                        f"[bold white]Summary:[/bold white] {a['historical_summary']}\n"
                        f"[bold green]Strategic Mirror Significance:[/bold green] {a['strategic_mirror_significance']}",
                        title=f"[bold white on magenta] HISTORICAL ANNIVERSARY MATCH: {a['month']}/{a['day']} [/bold white on magenta]",
                        border_style="magenta"
                    ))
        except Exception:
            pass

    # 2. Ingest Sovereign Evidence & GDELT Telemetry
    console.print("\n[bold yellow]=== 2. INGESTING OPEN SOVEREIGN EVIDENCE & GLOBAL TELEMETRY ===[/bold yellow]")
    evidence_items = GDELTClient.query_events(query.target_summit, max_records=2) + SovereignRSSClient.fetch_primary_statements()
    for ev in evidence_items:
        console.print(f" [bold green][+][/bold green] [cyan]{ev.source_name}[/cyan] ({ev.source_type} - {ev.timestamp[:10]}): [dim]{ev.raw_text[:120]}...[/dim]")

    # Normalize into structured claims for Bayesian updating
    all_claims = []
    for ev in evidence_items:
        all_claims.extend(IngestionNormalizer.normalize_evidence_item(ev))

    # 3. Calibrated Forecasting & Scenario Engine (Bayesian Evidence Updated)
    strata = ForecastingEngine.generate_strata(
        query.target_summit,
        query.year,
        evidence_claims=all_claims,
        event_type=query.event_type,
        include_unmodeled=True
    )
    console.print("\n[bold yellow]=== 3. CALIBRATED FORECASTING & SCENARIO DECOMPOSITION (BAYESIAN UPDATED) ===[/bold yellow]")
    
    scenario_table = Table(title="Probabilistic Scenario Tree (Brier Calibrated)", border_style="yellow", show_lines=True)
    scenario_table.add_column("Scenario Branch", style="bold white", width=34)
    scenario_table.add_column("Probability", style="bold green", width=14)
    scenario_table.add_column("Key Drivers", style="cyan", width=38)
    scenario_table.add_column("Early Warning Indicators", style="magenta", width=36)

    for sc in strata.scenario_branches:
        prob_color = "green" if sc.probability > 0.5 else "yellow" if sc.probability > 0.2 else "red"
        scenario_table.add_row(
            sc.scenario_name,
            f"[{prob_color}]{sc.probability*100:.0f}%[/{prob_color}]",
            "; ".join(sc.key_drivers),
            "; ".join(sc.early_indicators)
        )
    console.print(scenario_table)

    forecast_box = "\n".join([
        f"[bold cyan]* Hypothesis:[/bold cyan] {f.target_hypothesis}\n"
        f"  [bold green]Calibrated Probability:[/bold green] {f.forecast_probability*100:.0f}% (90% CI: {f.confidence_interval_low*100:.0f}% - {f.confidence_interval_high*100:.0f}% | Horizon: {f.time_horizon_months}m)\n"
        f"  [dim]Epistemic Basis: {f.epistemic_basis}[/dim]"
        for f in strata.calibrated_forecasts
    ])
    console.print(Panel(forecast_box, title="Calibrated Probabilistic Forecasts (Persistent Ledger)", border_style="cyan"))

    # 4. Render 5-Tier Report
    console.print("\n[bold yellow]=== 4. EXECUTING 5-TIER MULTI-LENS TRUTH ARBITRATION ===[/bold yellow]")
    target_countries = query.target_countries if query.target_countries else [
        "India", "China", "Russia", "Brazil", "South Africa",
        "Iran", "Saudi Arabia", "UAE", "Egypt", "Ethiopia"
    ]
    host_c = query.target_countries[0] if query.target_countries else "India"
    event_obj = SummitEvent(
        summit_name=query.target_summit,
        year=query.year,
        event_type=query.event_type,
        host_country=host_c,
        location=host_c,
        member_countries=target_countries,
        focal_date=query.focal_date
    )
    render_full_report(query.target_summit, query.year, persona=persona, target_event=event_obj)


def main():
    parser = argparse.ArgumentParser(description="Geo-Economic & Geopolitical Intelligence Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: audit
    audit_parser = subparsers.add_parser("audit", help="Run full 5-tier audit on a summit")
    audit_parser.add_argument("--summit", default="BRICS 2026 Summit", help="Summit title")
    audit_parser.add_argument("--year", type=int, default=2026, help="Summit year")
    audit_parser.add_argument("--persona", default="neutral", choices=["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"], help="Strategic analytical archetype projection")

    # Command: lenses
    lens_parser = subparsers.add_parser("lenses", help="Display evaluation across all registered lenses")
    lens_parser.add_argument("--summit", default="BRICS 2026 Summit", help="Summit title")

    # Command: query
    query_parser = subparsers.add_parser("query", help="Answer a complex user strategic prompt")
    query_parser.add_argument("prompt", type=str, help="The user question string")
    query_parser.add_argument("--persona", default="neutral", choices=["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"], help="Strategic analytical archetype projection")


    args = parser.parse_args()

    if args.command == "lenses":
        render_lenses_summary(args.summit)
    elif args.command == "query":
        persona = getattr(args, "persona", "neutral")
        render_query_pipeline(args.prompt, persona=persona)
    elif args.command == "audit" or args.command is None:
        summit_title = getattr(args, "summit", "BRICS 2026 Summit")
        year = getattr(args, "year", 2026)
        persona = getattr(args, "persona", "neutral")
        render_full_report(summit_title, year, persona=persona)


if __name__ == "__main__":
    main()
