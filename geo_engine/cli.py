"""
CLI Interface for the Geo-Engine.
Renders 5-tier summit intelligence reports with rich formatting, tables,
and epistemic audit logs for strategic decision-makers.
"""

import sys
import re
import argparse
from typing import Any, List, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

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
    target_event: Optional[Union[SummitEvent, StrategicEvent]] = None,
    claims: Optional[List[Any]] = None,
    evidence_items: Optional[List[Any]] = None,
    prioritized_lenses: Optional[List[str]] = None
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

    report = SummitSynthesizer.synthesize_report(
        summit,
        claims=claims,
        evidence_items=evidence_items,
        prioritized_lenses=prioritized_lenses
    )

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
    if "vostro_capital_recycling_velocity" in m:
        cash_text += (
            f"\n[bold cyan]SRVA Capital Recycling Velocity:[/bold cyan] {m['vostro_capital_recycling_velocity']}x "
            f"(Trapped Balances: ${m.get('vostro_balance_trapped_usd_b', 42.0):.1f}B USD, Reinvestment: {m.get('sovereign_debt_reinvestment_ratio', 0.65)*100:.0f}%)"
        )
    console.print(Panel(cash_text, title="Financial Ground Truth vs. Rhetoric", border_style="green"))

    # Strategic Resilience & Escalation Readiness Matrix (Lenses 13-20)
    if getattr(report, "strategic_resilience_matrix", None):
        res = report.strategic_resilience_matrix
        res_text = (
            f"[bold green]Strategic Grain Buffer Ratio (FCI):[/bold green] {res.get('strategic_grain_buffer_ratio', 0.0):.2f}x statutory norm  |  "
            f"[bold yellow]Potash (MOP) Import Dependency:[/bold yellow] {res.get('potash_mop_dependency_pct', 0.0):.1f}%\n"
            f"[bold cyan]Two-Front Deterrence Posture Score:[/bold cyan] {res.get('two_front_deterrence_posture', 0.0):.2f}  |  "
            f"[bold magenta]WWR Ammunition Reserve Depth:[/bold magenta] {res.get('wwr_ammunition_reserve_days', 0.0):.1f} Days\n"
            f"[bold green]IADS Integrated Air Defense Coverage:[/bold green] {res.get('iads_air_defense_coverage', 0.0):.2f}  |  "
            f"[bold red]HREE Refining Monopoly Exposure:[/bold red] {res.get('hree_refining_monopoly_pct', 0.0):.1f}%\n"
            f"[bold red]Demographic Border Transit Vulnerability:[/bold red] {res.get('demographic_border_vulnerability', 0.0):.2f}  |  "
            f"[bold yellow]Institutional Lawfare & OFAC Risk:[/bold yellow] {res.get('institutional_lawfare_ofac_risk', 0.0):.2f}\n"
            f"[bold cyan]Subsea Bandwidth Dependency:[/bold cyan] {res.get('subsea_bandwidth_dependency_pct', 0.0):.1f}%  |  "
            f"[bold green]Hydro-Spatial Seabed Sovereignty:[/bold green] {res.get('hydro_spatial_sovereignty_score', 0.0):.2f}\n"
            f"[bold magenta]SatCom Sovereignty Coverage (NavIC):[/bold magenta] {res.get('satcom_sovereignty_coverage_pct', 0.0):.1f}%  |  "
            f"[bold green]Orbital Anti-ASAT Sovereignty Index:[/bold green] {res.get('orbital_sovereignty_index', 0.0):.2f}"
        )
        console.print("\n[bold yellow]=== STRATEGIC RESILIENCE & ESCALATION READINESS (LENSES 13-20) ===[/bold yellow]")
        console.print(Panel(res_text, title="Physical Caloric, Military, Subsea & Orbital Sovereignty Matrix", border_style="cyan"))

    # Analysis of Competing Hypotheses (ACH) Deep Reasoning Matrix
    if getattr(report, "ach_evaluation", None):
        ach = report.ach_evaluation
        console.print("\n[bold yellow]=== ANALYSIS OF COMPETING HYPOTHESES (ACH) DEEP REASONING MATRIX ===[/bold yellow]")
        ach_table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
        ach_table.add_column("Causal Hypothesis", style="bold white", width=38)
        ach_table.add_column("Prior", style="dim", justify="right", width=8)
        ach_table.add_column("Likelihood", style="yellow", justify="right", width=12)
        ach_table.add_column("Posterior", style="bold green", justify="right", width=11)
        ach_table.add_column("Evidence Grounding", style="dim white", width=36)

        for h in ach.get("hypotheses", []):
            is_dom = (h.get("id") == ach.get("dominant_hypothesis_id"))
            p_style = "[bold green]" if is_dom else ""
            p_end = "[/bold green]" if is_dom else ""
            label_str = f"[bold yellow]* {h.get('label')}[/bold yellow]" if is_dom else h.get("label")
            ev_summary = f"{h.get('supporting_count', 0)} supporting, {h.get('contradicting_count', 0)} contradicting"
            ach_table.add_row(
                label_str,
                f"{h.get('prior', 0.25):.2f}",
                f"{h.get('likelihood', 0.50):.2f}",
                f"{p_style}{h.get('posterior', 0.25):.1%}{p_end}",
                ev_summary
            )
        console.print(ach_table)
        if ach.get("epistemic_warning"):
            console.print(Panel(
                f"[bold red]ACH CAUTION / TRUTH GUARD:[/bold red]\n{ach['epistemic_warning']}",
                border_style="red"
            ))

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
        weights_str = ", ".join([f"{k} ({v}x)" for k, v in p_data.get("lens_weights", {}).items()])
        disclaimer_str = p_data.get("disclaimer", "")
        p_box = (
            f"[dim italic]{disclaimer_str}[/dim italic]\n\n"
            f"[bold cyan]Intellectual Tradition:[/bold cyan] {p_data['archetype_name']}\n"
            f"[bold yellow]Doctrinal Axis:[/bold yellow] {p_data['doctrinal_axis']}\n"
            f"[bold magenta]Prioritized Lens Weights:[/bold magenta] {weights_str}\n\n"
            f"[bold white]Executive Takeaway:[/bold white]\n{p_data['executive_takeaway']}\n\n"
            f"[bold green]Key Strategic Recommendations:[/bold green]\n{p_recs}"
        )
        console.print(Panel(p_box, title=f"[bold white on red] STRATEGIC PERSONA PROJECTION: {p_data['archetype_key'].upper()} [/bold white on red]", border_style="red"))
        console.print()


def render_lenses_summary(summit_name: str = "BRICS 2026 Summit", persona: str = "neutral"):
    """Displays alignment scores and key findings from all registered lenses, optionally weighted by persona."""
    summit = SummitEvent(summit_name=summit_name, year=2026, host_country="India", location="New Delhi")
    
    # Check persona weights
    persona_weights = {}
    p_data = None
    if persona and persona.lower() != "neutral":
        from .arbitration.persona_narrator import PersonaNarrator
        key = persona.lower().strip()
        if key in PersonaNarrator.ARCHETYPES:
            p_data = PersonaNarrator.ARCHETYPES[key]
            persona_weights = p_data.get("lens_weights", {})

    title_suffix = f" (Persona Weighted: {persona.upper()})" if persona_weights else ""
    table = Table(title=f"The {len(LENS_REGISTRY)}-Lens Analytical Matrix Evaluation{title_suffix}", border_style="cyan")
    table.add_column("Lens #", style="bold white", width=6)
    table.add_column("Lens Name", style="bold cyan", width=34)
    table.add_column("Epistemic Tier", style="magenta", width=18)
    table.add_column("Alignment Score", style="green", width=16)
    table.add_column("Confidence", style="yellow", width=12)
    if persona_weights:
        table.add_column("Persona Weight", style="bold yellow", width=14)
    table.add_column("Primary Analytical Finding", style="white", width=45)

    for i, lens in enumerate(LENS_REGISTRY, 1):
        ev = lens.evaluate(summit)
        score_color = "green" if ev.alignment_score > 0.5 else "yellow" if ev.alignment_score > 0.3 else "red"
        row_items = [
            str(i),
            ev.lens_name,
            ev.primary_epistemic_tier.name,
            f"[{score_color}]{ev.alignment_score:+.2f}[/{score_color}]",
            f"{ev.confidence*100:.0f}%",
        ]
        if persona_weights:
            weight = persona_weights.get(lens.__name__, 1.0)
            w_str = f"[bold green]{weight:.1f}x[/bold green]" if weight > 1.0 else f"[dim]{weight:.1f}x[/dim]"
            row_items.append(w_str)
        row_items.append(ev.key_findings[0] if ev.key_findings else "N/A")
        table.add_row(*row_items)
    console.print(table)

    if p_data:
        console.print(Panel(
            f"[bold cyan]Intellectual Tradition:[/bold cyan] {p_data['name']}\n"
            f"[bold yellow]Doctrinal Axis:[/bold yellow] {p_data['doctrinal_axis']}\n\n"
            f"[bold white]Doctrinal Framing:[/bold white]\n{p_data['conceptual_framing']}",
            title=f"[bold white on red] STRATEGIC PERSONA PROFILE: {persona.upper()} [/bold white on red]",
            border_style="red"
        ))


def render_query_pipeline(prompt: str, persona: str = "neutral"):
    """Dynamically parses arbitrary user prompts, ingests open evidence, and executes calibrated forecasting."""
    # 1. Dynamic Query Deconstruction
    query = QueryParser.parse(prompt)

    
    console.print(Panel(
        f"[bold yellow]Prompt Analyzed:[/bold yellow] \"{query.raw_prompt}\"\n\n"
        f"[bold cyan]Target Event:[/bold cyan] {query.target_summit} (Horizon: {query.year}) | "
        f"[bold cyan]Countries Detected:[/bold cyan] {', '.join(query.target_countries) if query.target_countries else 'All 10 Core Member States'}\n"
        f"[bold cyan]Forensic Modules Required:[/bold cyan] Kinesics: {query.requires_kinesics} | Cash: {query.requires_cash_audit} | Negative Space: {query.requires_negative_space} | Civilizational: {query.requires_civilizational_depth} | India Timeline: {query.requires_india_timeline} | Demographic: {query.requires_demographic_audit} | Critical Minerals: {query.requires_minerals_audit} | Lawfare: {query.requires_lawfare_audit}",
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

    # Normalize into structured claims with batch SHA-256 wire deduplication
    all_claims = IngestionNormalizer.normalize_evidence_batch(evidence_items)

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
    render_full_report(
        query.target_summit,
        query.year,
        persona=persona,
        target_event=event_obj,
        claims=all_claims,
        evidence_items=evidence_items,
        prioritized_lenses=query.prioritized_lenses
    )


def render_forecast_ledger(status: Optional[str] = None, resolve_id: Optional[str] = None, outcome: Optional[int] = None):
    """Displays and resolves persistent calibrated forecasts in SQLite ledger."""
    store = EventStore()
    if resolve_id and outcome is not None:
        brier = store.resolve_forecast(resolve_id, outcome)
        console.print(f"[bold green][+][/bold green] Resolved forecast [cyan]{resolve_id}[/cyan] with outcome [yellow]{outcome}[/yellow]. Brier score: [bold green]{brier:.4f}[/bold green]")
        return

    records = store.get_forecast_ledger(status=status)
    if not records:
        console.print(f"[yellow]No forecast records found matching status={status}.[/yellow]")
        return

    table = Table(title=f"Calibrated Forecast Ledger (SQLite: events.db) [Count: {len(records)}]", border_style="cyan")
    table.add_column("Forecast ID", style="bold cyan", width=22)
    table.add_column("Target Date", style="yellow", width=12)
    table.add_column("Event / Summit", style="white", width=20)
    table.add_column("Hypothesis", style="bold white", width=36)
    table.add_column("Predicted", style="green", width=10)
    table.add_column("Outcome", style="magenta", width=10)
    table.add_column("Brier", style="bold yellow", width=10)
    table.add_column("Status", style="bold green", width=10)

    for r in records:
        out_str = str(r["actual_outcome"]) if r.get("actual_outcome") is not None else "N/A"
        brier_str = f"{r['brier_score']:.4f}" if r.get("brier_score") is not None else "N/A"
        table.add_row(
            r["forecast_id"],
            r.get("target_date", "N/A"),
            r.get("event_name", "N/A"),
            r["hypothesis"][:34] + "..." if len(r["hypothesis"]) > 34 else r["hypothesis"],
            f"{r['predicted_probability']*100:.0f}%",
            out_str,
            brier_str,
            r.get("status", "ACTIVE")
        )
    console.print(table)


def render_video_intelligence(video_url: str, query: str):
    """Executes question-first video intelligence and prints timestamp citations and synthesis."""
    from geo_engine.video import VideoSynthesizer
    report = VideoSynthesizer.synthesize_video_query(video_url=video_url, query=query)

    console.print(Panel(
        f"[bold cyan]Video ID:[/bold cyan] {report.video_id}\n"
        f"[bold cyan]Canonical URL:[/bold cyan] {report.canonical_url}\n"
        f"[bold yellow]Query Question:[/bold yellow] {report.query}\n"
        f"[bold magenta]Transcript Mode:[/bold magenta] {'[Simulated Geopolitical Fallback]' if report.is_simulated_transcript else '[Verified Captions]'}",
        title="Question-First Video Intelligence",
        border_style="cyan"
    ))

    console.print("\n[bold yellow]=== TIMESTAMPED CITATIONS & EVIDENCE JUMP LINKS ===[/bold yellow]")
    for item in report.cited_timestamps:
        console.print(f"* [bold green][{item['timestamp']}][/bold green] ({item['url']}): {item['text_snippet']}")

    console.print("\n[bold yellow]=== PHYSICAL REALITY VS. RHETORIC AUDIT ===[/bold yellow]")
    console.print(Panel(report.rhetoric_vs_reality_check, title="20-Lens Physical Audit", border_style="green"))

    console.print("\n[bold yellow]=== STRATEGIC SYNTHESIS ===[/bold yellow]")
    console.print(Panel(report.synthesis_markdown, title="Verifiable Intelligence Brief", border_style="yellow"))


def render_cascading_simulation(domain: str, severity: float = 0.8, description: str = "Exogenous Geopolitical Shock Event"):
    from .simulation import CascadingSimulationEngine, SimulationShock
    shock = SimulationShock(
        shock_id=f"shock_{domain}_{int(severity*100)}",
        domain=domain,
        description=description,
        severity=severity
    )
    res = CascadingSimulationEngine.simulate_shock(shock)
    console.print(Panel(
        f"[bold red]Cascading Shock Simulation: {shock.shock_id}[/bold red]\n"
        f"Domain: [cyan]{shock.domain}[/cyan] | Severity: [yellow]{shock.severity:.2f}[/yellow]\n"
        f"Systemic Vulnerability Index: [bold magenta]{res.systemic_vulnerability_index:.2f}[/bold magenta]",
        title="[bold yellow]Multi-Order Contagion Simulation[/bold yellow]",
        border_style="red"
    ))

    for order_name, impacts in [("Order 1: Direct Impacts", res.order_1_impacts),
                                ("Order 2: Secondary Contagion", res.order_2_impacts),
                                ("Order 3: Tertiary Realignment", res.order_3_impacts)]:
        tbl = Table(title=order_name, show_lines=True)
        tbl.add_column("Lens", style="bold cyan", width=24)
        tbl.add_column("Impact Score", justify="center", width=14)
        tbl.add_column("Mitigated", justify="center", width=12)
        tbl.add_column("Mechanism & Strategic Impact", style="white")
        for imp in impacts:
            mit_text = "[green]YES[/green]" if imp.mitigated_by_resilience else "[dim]NO[/dim]"
            tbl.add_row(imp.lens, f"{imp.impact_score:.2f}", mit_text, imp.mechanism)
        console.print(tbl)

    if res.recommended_mitigations:
        console.print("\n[bold green]Recommended Systemic Mitigations:[/bold green]")
        for m in res.recommended_mitigations:
            console.print(f" • {m}")


def render_game_theoretic_simulation(
    initiator: str = "China",
    target: str = "India",
    domain: str = "critical_minerals",
    severity: float = 0.85,
    action: str = "Export restrictions on sintered NdFeB permanent magnets",
    intent: str = "",
    persist: bool = False,
    session_id: Optional[str] = None
):
    from .simulation import GameTheoreticEngine

    res = GameTheoreticEngine.simulate_interaction(
        initiator_name=initiator,
        target_name=target,
        domain=domain,
        severity=severity,
        action_description=action,
        intent=intent,
        persist=persist,
        session_id=session_id
    )

    console.print(Panel(
        f"[bold white]{res.simulation_id}: Sequential Game-Theoretic Red-Team[/bold white]\n"
        f"[cyan]Initiator:[/cyan] {res.initiator.name} (Autonomy: {res.initiator.strategic_autonomy_score:.2f}, Risk: {res.initiator.risk_tolerance:.2f})\n"
        f"[cyan]Target:[/cyan] {res.target.name} (Autonomy: {res.target.strategic_autonomy_score:.2f}, Risk: {res.target.risk_tolerance:.2f})\n"
        f"[cyan]Equilibrium Stability Index:[/cyan] [bold yellow]{res.equilibrium_stability_index:.2f}[/bold yellow] | "
        f"[cyan]Spiral Risk:[/cyan] [bold red]{res.turn_3_backlash.escalation_spiral_risk:.2f}[/bold red]",
        title="[bold yellow]STRATEGIC RED-TEAMING & COUNTER-MOVE SIMULATION[/bold yellow]",
        border_style="yellow"
    ))

    tbl = Table(title="3-Turn Game-Theoretic Interaction Sequence", show_lines=True)
    tbl.add_column("Turn", justify="center", width=8, style="bold cyan")
    tbl.add_column("Actor & Direction", style="bold white", width=22)
    tbl.add_column("Domain / Category", justify="center", width=24)
    tbl.add_column("Severity / Metric", justify="center", width=18)
    tbl.add_column("Strategic Maneuver & Impact Rationale", style="white")

    tbl.add_row(
        "Turn 1",
        f"{res.turn_1_action.initiator} -> {res.turn_1_action.target}",
        res.turn_1_action.domain,
        f"{res.turn_1_action.severity:.2f}",
        f"{res.turn_1_action.action_description}\n[dim]Declared Intent: {res.turn_1_action.declared_intent}[/dim]"
    )
    tbl.add_row(
        "Turn 2",
        f"{res.turn_2_reaction.responder} (Counter)",
        f"{res.turn_2_reaction.counter_domain} ({res.turn_2_reaction.response_type})",
        f"{res.turn_2_reaction.severity:.2f}",
        f"{res.turn_2_reaction.action_description}\n[dim]Strategic Rationale: {res.turn_2_reaction.strategic_rationality}[/dim]"
    )
    tbl.add_row(
        "Turn 3",
        "Systemic Equilibrium",
        "Putnam Two-Level Game",
        f"Friction: {res.turn_3_backlash.domestic_political_friction:.2f}\nInflation: {res.turn_3_backlash.inflationary_backlash_score:.2f}",
        f"Alliance Shift: {res.turn_3_backlash.third_party_realignment}\n[green]Off-Ramp: {res.turn_3_backlash.de_escalation_off_ramp}[/green]"
    )
    console.print(tbl)

    console.print("\n[bold green]Strategic Payoff Assessment:[/bold green]")
    for actor_name, payoff in res.net_strategic_payoff.items():
        color = "green" if payoff >= 0 else "red"
        console.print(f" • {actor_name} Net Strategic Payoff: [{color}]{payoff:+.2f}[/{color}]")
    console.print(f"\n[italic]{res.summary}[/italic]")
    if persist:
        console.print(f"\n[bold green]✓ Campaign session persisted to EventStore:[/bold green] [cyan]{res.simulation_id}[/cyan]")


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
    lens_parser.add_argument("--persona", default="neutral", choices=["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"], help="Strategic analytical archetype projection")

    # Command: query
    query_parser = subparsers.add_parser("query", help="Run natural-language query routing through dynamic lens activation")
    query_parser.add_argument("prompt", type=str, help="Analytical question or scenario prompt")
    query_parser.add_argument("--persona", default="neutral", choices=["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"], help="Strategic analytical archetype projection")

    # Command: forecasts
    fc_parser = subparsers.add_parser("forecasts", help="Inspect and resolve calibrated strategic forecasts")
    fc_parser.add_argument("--status", choices=["ACTIVE", "RESOLVED"], default=None, help="Filter by forecast resolution status")
    fc_parser.add_argument("--resolve", type=str, default=None, help="Forecast ID to resolve")
    fc_parser.add_argument("--outcome", type=int, choices=[0, 1], default=None, help="Actual binary outcome (1=occurred, 0=did not occur)")

    # Command: video
    video_parser = subparsers.add_parser("video", help="Run multi-lens open-source video intelligence audit")
    video_parser.add_argument("--url", "-u", type=str, required=True, help="YouTube video or shorts URL")
    video_parser.add_argument("--query", "-q", type=str, required=True, help="Question to answer from video")

    # Command: simulate
    sim_parser = subparsers.add_parser("simulate", help="Run multi-order cascading shock simulation across lenses")
    sim_parser.add_argument("--domain", required=True, help="Originating domain/lens (e.g. petro_logistics, critical_minerals, institutional_lawfare)")
    sim_parser.add_argument("--severity", type=float, default=0.8, help="Shock severity magnitude (0.0 - 1.0)")
    sim_parser.add_argument("--description", default="Exogenous Geopolitical Shock Event", help="Description of shock event")

    # Command: red-team
    rt_parser = subparsers.add_parser("red-team", help="Run sequential 3-turn game-theoretic strategic red-teaming")
    rt_parser.add_argument("--initiator", default="China", help="Initiating sovereign actor")
    rt_parser.add_argument("--target", default="India", help="Target sovereign actor")
    rt_parser.add_argument("--domain", default="critical_minerals", help="Domain of opening move")
    rt_parser.add_argument("--severity", type=float, default=0.85, help="Severity magnitude (0.0 - 1.0)")
    rt_parser.add_argument("--action", default="Export restrictions on sintered NdFeB permanent magnets", help="Description of action")
    rt_parser.add_argument("--intent", default="", help="Declared intent of initiating move")
    rt_parser.add_argument("--persist", action="store_true", help="Persist wargame campaign session and turns into EventStore SQLite")
    rt_parser.add_argument("--session-id", default=None, help="Custom identifier for persistent wargame campaign")

    try:
        args = parser.parse_args()

        if args.command == "lenses":
            persona = getattr(args, "persona", "neutral")
            render_lenses_summary(args.summit, persona=persona)
        elif args.command == "query":
            persona = getattr(args, "persona", "neutral")
            render_query_pipeline(args.prompt, persona=persona)
        elif args.command == "forecasts":
            render_forecast_ledger(status=args.status, resolve_id=args.resolve, outcome=args.outcome)
        elif args.command == "video":
            render_video_intelligence(args.url, args.query)
        elif args.command == "simulate":
            render_cascading_simulation(args.domain, severity=args.severity, description=args.description)
        elif args.command == "red-team":
            render_game_theoretic_simulation(
                initiator=args.initiator,
                target=args.target,
                domain=args.domain,
                severity=args.severity,
                action=args.action,
                intent=args.intent,
                persist=getattr(args, "persist", False),
                session_id=getattr(args, "session_id", None)
            )
        elif args.command == "audit" or args.command is None:
            summit_title = getattr(args, "summit", "BRICS 2026 Summit")
            year = getattr(args, "year", 2026)
            persona = getattr(args, "persona", "neutral")
            render_full_report(summit_title, year, persona=persona)
    except Exception as e:
        console.print(f"[bold red][ERROR][/bold red] CLI Execution Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

