"""
JSON-RPC 2.0 Model Context Protocol (MCP) Server for Geo-Engine.
Implements stdio protocol for tools/list and tools/call, bridging external LLMs
(Claude Desktop, Cursor, Gemini CLI, NotebookLM sidecars) directly to the live engine.
"""

import sys
import json
from typing import Any, Dict, List, Optional

from ..core.models import SummitEvent
from ..core.query_parser import QueryParser
from ..arbitration.synthesizer import SummitSynthesizer
from ..arbitration.persona_narrator import PersonaNarrator
from ..simulation.cascading_engine import CascadingSimulationEngine
from ..simulation.game_theoretic import GameTheoreticEngine
from ..storage.event_store import EventStore
from ..lenses import LENS_REGISTRY
from ..lenses.geo_economist import GeoEconomistLens
from ..ingestion.telemetry_adapter import MacroTelemetryAdapter


class GeoEngineMCPServer:
    """Zero-dependency JSON-RPC 2.0 MCP server executing live geo_engine tools."""

    PROTOCOL_VERSION = "2024-11-05"
    SERVER_NAME = "geo-engine-mcp"
    SERVER_VERSION = "0.1.0"

    TOOLS_MANIFEST = [
        {
            "name": "geo_query",
            "description": "Run full 20-lens forensic geopolitical and geoeconomic analysis on an event or prompt.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The strategic query or event description to analyze."
                    },
                    "persona": {
                        "type": "string",
                        "enum": ["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"],
                        "default": "neutral",
                        "description": "Strategic persona projection tradition to apply."
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "geo_simulate",
            "description": "Simulate multi-order cascading shock propagation across 20 analytical lenses with non-linear tipping points.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Domain of the initial shock (e.g., petro_logistics, critical_minerals, subsea_cables)."
                    },
                    "severity": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "description": "Shock severity magnitude between 0.0 and 1.0."
                    },
                    "description": {
                        "type": "string",
                        "description": "Textual context and parameters of the shock."
                    }
                },
                "required": ["domain", "severity", "description"]
            }
        },
        {
            "name": "geo_red_team",
            "description": "Run 3-turn sequential game-theoretic strategic interaction (Action, Asymmetric Reaction, Domestic Backlash).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "initiator": {"type": "string", "description": "Initiating state actor (e.g., China, USA)."},
                    "target": {"type": "string", "description": "Target state actor (e.g., India)."},
                    "domain": {"type": "string", "description": "Strategic domain of confrontation."},
                    "severity": {"type": "number", "minimum": 0.0, "maximum": 1.0, "description": "Severity of opening move."},
                    "action": {"type": "string", "description": "Description of initiating move."},
                    "intent": {"type": "string", "default": "", "description": "Declared intent."}
                },
                "required": ["initiator", "target", "domain", "severity", "action"]
            }
        },
        {
            "name": "geo_forecasts",
            "description": "Query calibrated forecasts and Brier score validation records from the SQLite ledger.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["ALL", "ACTIVE", "RESOLVED"],
                        "default": "ALL",
                        "description": "Filter forecasts by status."
                    }
                }
            }
        },
        {
            "name": "geo_lenses",
            "description": "Inspect the 20 analytical lenses, their primary epistemic tiers, and persona weights.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "persona": {
                        "type": "string",
                        "enum": ["neutral", "sanyal", "doval", "jaishankar", "ranganathan", "ankit_shah"],
                        "default": "neutral",
                        "description": "Persona tradition to retrieve weight multipliers for."
                    }
                }
            }
        },
        {
            "name": "geo_ingest_audit",
            "description": "Ingest structured macroeconomic and geopolitical audit findings into SQLite EventStore.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "default": "FORENSIC_AUDIT_INDIA_1991_2026.md",
                        "description": "File path to the markdown audit document."
                    }
                }
            }
        },
        {
            "name": "geo_recalculate_deflation",
            "description": "Compute double-deflated vs single-deflated manufacturing GVA and calculate the statistical distortion divergence percentage.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "nominal_output": {"type": "number", "description": "Nominal value of gross manufacturing output."},
                    "output_deflator": {"type": "number", "description": "Deflator index for gross output (e.g., 1.02 for 2% inflation)."},
                    "nominal_input": {"type": "number", "description": "Nominal value of intermediate inputs consumed."},
                    "input_deflator": {"type": "number", "description": "Deflator index for inputs (e.g., 0.95 for 5% input deflation)."}
                },
                "required": ["nominal_output", "output_deflator", "nominal_input", "input_deflator"]
            }
        },
        {
            "name": "geo_ingest_media",
            "description": "Extract captions/transcript and ingest verified claims from a YouTube or media URL.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube or media stream URL to ingest."
                    },
                    "target_lenses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of lenses to tag the extracted claims with."
                    }
                },
                "required": ["url"]
            }
        }
    ]

    def __init__(self, store: Optional[EventStore] = None):
        self.store = store or EventStore()

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processes a single JSON-RPC 2.0 request dict and returns the response dict."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        # Handle notifications (no id)
        if req_id is None and method == "notifications/initialized":
            return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": self.SERVER_NAME,
                        "version": self.SERVER_VERSION
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": self.TOOLS_MANIFEST
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_content = self.execute_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_content, indent=2, default=str)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": f"Tool execution failed: {str(e)}"
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Executes the specified tool with arguments and returns structured Python objects."""
        if tool_name == "geo_query":
            prompt = arguments.get("prompt", "")
            persona = arguments.get("persona", "neutral")
            parsed_query = QueryParser.parse(prompt)
            target_countries = parsed_query.target_countries if parsed_query.target_countries else [
                "India", "China", "Russia"
            ]
            host_c = parsed_query.target_countries[0] if parsed_query.target_countries else "India"
            target_event = SummitEvent(
                summit_name=parsed_query.target_summit,
                year=parsed_query.year,
                event_type=parsed_query.event_type,
                host_country=host_c,
                location=host_c,
                member_countries=target_countries,
                focal_date=parsed_query.focal_date
            )
            report = SummitSynthesizer.synthesize_report(
                summit=target_event,
                prioritized_lenses=parsed_query.prioritized_lenses,
                fixture_mode=True
            )
            persona_view = PersonaNarrator.apply_persona(report, persona_key=persona)
            return {
                "query": prompt,
                "event_type": str(target_event.event_type),
                "prioritized_lenses": parsed_query.prioritized_lenses,
                "overall_confidence": report.overall_confidence_score,
                "persona": persona,
                "country_ledgers_count": len(report.country_ledgers),
                "negative_space_omissions": report.negative_space_synopsis,
                "civilizational_synthesis": persona_view.get("synthesized_text", ""),
                "key_findings": [f for l in report.lens_evaluations[:2] for f in l.key_findings[:2]]
            }

        elif tool_name == "geo_simulate":
            domain = arguments["domain"]
            severity = float(arguments["severity"])
            description = arguments["description"]
            engine = CascadingSimulationEngine()
            result = engine.simulate_shock(domain=domain, severity=severity, description=description)
            return {
                "domain": result.initial_shock.domain,
                "severity": result.initial_shock.severity,
                "systemic_vulnerability_index": result.systemic_vulnerability_index,
                "is_tipping_point": result.is_tipping_point,
                "critical_resilience_deficit": result.critical_resilience_deficit,
                "order_1_impacts": [i.model_dump() for i in result.order_1_impacts],
                "order_2_impacts": [i.model_dump() for i in result.order_2_impacts],
                "order_3_impacts": [i.model_dump() for i in result.order_3_impacts],
                "strategic_hedges": result.strategic_hedges
            }

        elif tool_name == "geo_red_team":
            initiator = arguments["initiator"]
            target = arguments["target"]
            domain = arguments["domain"]
            severity = float(arguments["severity"])
            action = arguments["action"]
            intent = arguments.get("intent", "")
            engine = GameTheoreticEngine()
            interaction = engine.simulate_interaction(
                initiator=initiator,
                target=target,
                domain=domain,
                severity=severity,
                action=action,
                intent=intent
            )
            return interaction.model_dump()

        elif tool_name == "geo_forecasts":
            status_filter = arguments.get("status", "ALL")
            status = None if status_filter == "ALL" else status_filter
            records = self.store.get_forecast_ledger(status=status)
            return {
                "status_filter": status_filter,
                "count": len(records),
                "forecasts": records
            }

        elif tool_name == "geo_lenses":
            persona = arguments.get("persona", "neutral")
            archetype = PersonaNarrator.ARCHETYPES.get(persona, PersonaNarrator.ARCHETYPES["neutral"])
            lenses_meta = []
            for name, lens_cls in LENS_REGISTRY.items():
                lenses_meta.append({
                    "registry_key": name,
                    "lens_name": getattr(lens_cls, "LENS_NAME", name),
                    "primary_tier": getattr(lens_cls, "PRIMARY_TIER", 1).name,
                    "persona_weight": archetype.get("lens_weights", {}).get(name, 1.0)
                })
            return {
                "persona": persona,
                "persona_description": archetype.get("description", ""),
                "lens_count": len(lenses_meta),
                "lenses": lenses_meta
            }

        elif tool_name == "geo_ingest_audit":
            path = arguments.get("path", "FORENSIC_AUDIT_INDIA_1991_2026.md")
            claims = MacroTelemetryAdapter.extract_claims_from_audit_markdown(path)
            for claim in claims:
                self.store.record_claim(claim)
            return {
                "status": "SUCCESS",
                "source_file": path,
                "claims_ingested": len(claims),
                "message": f"Successfully ingested {len(claims)} verified claims into SQLite events.db"
            }

        elif tool_name == "geo_recalculate_deflation":
            output_nom = float(arguments["nominal_output"])
            output_def = float(arguments["output_deflator"])
            input_nom = float(arguments["nominal_input"])
            input_def = float(arguments["input_deflator"])
            res = GeoEconomistLens.calculate_double_deflated_gva(
                nominal_output=output_nom,
                output_deflator=output_def,
                nominal_input=input_nom,
                input_deflator=input_def
            )
            return res

        elif tool_name == "geo_ingest_media":
            from ..video import AudioStreamConnector
            url = str(arguments["url"])
            target_lenses = arguments.get("target_lenses")
            res = AudioStreamConnector.ingest_media_url(
                url_or_id=url,
                store=self.store,
                target_lenses=target_lenses
            )
            return res

        else:
            raise ValueError(f"Unknown tool: {tool_name}")


def run_stdio_server():
    """Runs the MCP server over standard input and standard output."""
    server = GeoEngineMCPServer()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = server.handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
