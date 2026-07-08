"""
Moonraker LED – Test API
========================
Exposes HTTP endpoints so you can control LED segments and animations
from another computer, independent of live Moonraker events.

Endpoints
---------
GET  /api/segments                         – list all segments and their config
GET  /api/state                            – return simulated printer state
POST /api/state                            – update simulated printer state values
GET  /api/mode                             – return current control mode
POST /api/mode                             – switch between "auto" / "manual"
POST /api/segments/{segment}/animation    – assign an animation to a segment
DELETE /api/segments/{segment}/animation  – turn a segment off
POST /api/segments/{segment}/enable       – enable a segment
POST /api/segments/{segment}/disable      – disable a segment
POST /api/clear                            – clear all active animations
POST /api/state/simulate/{state_name}     – simulate a named printer state (idle/heating/printing)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────────────────────────────────────
# Pydantic schemas
# ──────────────────────────────────────────────────────────────────────────────

Color = Tuple[int, int, int]


class AnimationRequest(BaseModel):
    type: str = Field(
        description=(
            "Animation type: solid | breathe | pulse | flash | "
            "heartbeat | z_tracker | heating_progress | temperature"
        )
    )
    color: Optional[Color] = None
    period: Optional[float] = None
    mode: Optional[str] = None          # for heating_progress: "bed" | "extruder"
    sensor: Optional[str] = None        # for temperature: "bed" | "extruder"


class ModeRequest(BaseModel):
    mode: str = Field(description='"auto" or "manual"')


class StateUpdate(BaseModel):
    progress: Optional[float] = None
    print_state: Optional[str] = None
    extruder_temperature: Optional[float] = None
    target_extruder_temperature: Optional[float] = None
    heater_bed_temperature: Optional[float] = None
    target_heater_bed_temperature: Optional[float] = None
    z_position: Optional[float] = None
    max_z: Optional[float] = None


# ──────────────────────────────────────────────────────────────────────────────
# App factory
# ──────────────────────────────────────────────────────────────────────────────

def build_api(renderer, led_manager, printer_state) -> FastAPI:
    """
    Returns a configured FastAPI app that shares the live renderer,
    led_manager, and printer_state objects with the main event loop.
    """

    app = FastAPI(
        title="Moonraker LED Test API",
        description="Remote control interface for Ender 3 LED segments",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store shared objects in app state so route handlers can access them
    app.state.renderer = renderer
    app.state.led_manager = led_manager
    app.state.printer_state = printer_state
    app.state.mode = "auto"   # "auto" | "manual"

    # ── helpers ────────────────────────────────────────────────────────────────

    def _renderer(request: Request):
        return request.app.state.renderer

    def _led_manager(request: Request):
        return request.app.state.led_manager

    def _printer_state(request: Request):
        return request.app.state.printer_state

    def _mode(request: Request) -> str:
        return request.app.state.mode

    def _make_animation(req: AnimationRequest, segment=None):
        """Instantiate an animation object from an AnimationRequest payload."""
        anim_type = req.type.lower()
        color = tuple(req.color) if req.color else (255, 255, 255)

        if anim_type == "solid":
            from animations.solid import Solid
            return Solid(color)

        elif anim_type == "breathe":
            from animations.breathe import Breathe
            return Breathe(color, period=req.period or 4.0)

        elif anim_type == "pulse":
            from animations.pulse import Pulse
            return Pulse(color, period=req.period or 2.0)

        elif anim_type == "flash":
            from animations.flash import Flash
            return Flash(color, period=req.period or 1.0)

        elif anim_type == "heartbeat":
            from animations.heartbeat import Heartbeat
            return Heartbeat(color=color)

        elif anim_type == "z_tracker":
            from animations.z_tracker import ZTracker
            return ZTracker()

        elif anim_type == "heating_progress":
            from animations.heating_progress import HeatingProgress
            return HeatingProgress(mode=req.mode or "bed")

        elif anim_type == "temperature":
            from animations.temperature import Temperature
            return Temperature(sensor=req.sensor)

        else:
            raise HTTPException(status_code=400, detail=f"Unknown animation type: '{anim_type}'")

    # ── routes ────────────────────────────────────────────────────────────────

    @app.get("/")
    def root():
        return {"info": "Moonraker LED Test API", "docs": "/docs"}

    # --- segments -------------------------------------------------------------

    @app.get("/api/segments")
    def list_segments(request: Request):
        renderer = _renderer(request)
        result = {}
        for name, seg in renderer.segments.items():
            anim = seg.animation
            result[name] = {
                "name": name,
                "start": seg.start,
                "end": seg.end,
                "length": seg.length,
                "enabled": seg.enabled,
                "animation": type(anim).__name__ if anim else None,
            }
        return result

    @app.post("/api/segments/{segment_name}/animation")
    def set_animation(segment_name: str, req: AnimationRequest, request: Request):
        renderer = _renderer(request)
        seg = renderer.segments.get(segment_name)
        if not seg:
            raise HTTPException(status_code=404, detail=f"Segment '{segment_name}' not found")

        # Switch to manual so Moonraker events don't overwrite our change
        request.app.state.mode = "manual"

        seg.animation = _make_animation(req, segment=seg)
        return {"ok": True, "segment": segment_name, "animation": req.type}

    @app.delete("/api/segments/{segment_name}/animation")
    def clear_segment_animation(segment_name: str, request: Request):
        renderer = _renderer(request)
        seg = renderer.segments.get(segment_name)
        if not seg:
            raise HTTPException(status_code=404, detail=f"Segment '{segment_name}' not found")
        request.app.state.mode = "manual"
        seg.animation = None
        return {"ok": True, "segment": segment_name, "animation": None}

    @app.post("/api/segments/{segment_name}/enable")
    def enable_segment(segment_name: str, request: Request):
        renderer = _renderer(request)
        seg = renderer.segments.get(segment_name)
        if not seg:
            raise HTTPException(status_code=404, detail=f"Segment '{segment_name}' not found")
        seg.enabled = True
        return {"ok": True, "segment": segment_name, "enabled": True}

    @app.post("/api/segments/{segment_name}/disable")
    def disable_segment(segment_name: str, request: Request):
        renderer = _renderer(request)
        seg = renderer.segments.get(segment_name)
        if not seg:
            raise HTTPException(status_code=404, detail=f"Segment '{segment_name}' not found")
        seg.enabled = False
        return {"ok": True, "segment": segment_name, "enabled": False}

    # --- clear ----------------------------------------------------------------

    @app.post("/api/clear")
    def clear_all(request: Request):
        renderer = _renderer(request)
        request.app.state.mode = "manual"
        for seg in renderer.segments.values():
            seg.animation = None
        return {"ok": True, "message": "All animations cleared"}

    # --- mode -----------------------------------------------------------------

    @app.get("/api/mode")
    def get_mode(request: Request):
        return {"mode": request.app.state.mode}

    @app.post("/api/mode")
    def set_mode(req: ModeRequest, request: Request):
        if req.mode not in ("auto", "manual"):
            raise HTTPException(status_code=400, detail="mode must be 'auto' or 'manual'")
        request.app.state.mode = req.mode

        # When switching back to auto, re-apply the current printer state
        if req.mode == "auto":
            led_manager = _led_manager(request)
            printer_state = _printer_state(request)
            led_manager.update(printer_state)

        return {"ok": True, "mode": req.mode}

    # --- printer state --------------------------------------------------------

    @app.get("/api/state")
    def get_state(request: Request):
        s = _printer_state(request)
        return {
            "print_state": s.print_state,
            "progress": s.progress,
            "extruder_temperature": s.extruder_temperature,
            "target_extruder_temperature": s.target_extruder_temperature,
            "extruder_target_progress": s.extruder_target_progress,
            "heater_bed_temperature": s.heater_bed_temperature,
            "target_heater_bed_temperature": s.target_heater_bed_temperature,
            "heater_bed_target_progress": s.heater_bed_target_progress,
            "z_position": s.z_position,
            "max_z": s.max_z,
        }

    @app.post("/api/state")
    def update_state(body: StateUpdate, request: Request):
        s = _printer_state(request)
        if body.progress is not None:
            s.progress = body.progress
        if body.print_state is not None:
            s.print_state = body.print_state
        if body.extruder_temperature is not None:
            s.extruder_temperature = body.extruder_temperature
            s.extruder_target_progress = (
                (s.extruder_temperature / s.target_extruder_temperature) * 100
                if s.target_extruder_temperature > 0 else 0
            )
        if body.target_extruder_temperature is not None:
            s.target_extruder_temperature = body.target_extruder_temperature
        if body.heater_bed_temperature is not None:
            s.heater_bed_temperature = body.heater_bed_temperature
            s.heater_bed_target_progress = (
                (s.heater_bed_temperature / s.target_heater_bed_temperature) * 100
                if s.target_heater_bed_temperature > 0 else 0
            )
        if body.target_heater_bed_temperature is not None:
            s.target_heater_bed_temperature = body.target_heater_bed_temperature
        if body.z_position is not None:
            s.z_position = body.z_position
        if body.max_z is not None:
            s.max_z = body.max_z

        # Auto-trigger led_manager if in auto mode
        if request.app.state.mode == "auto":
            led_manager = _led_manager(request)
            led_manager.update(s)

        return {"ok": True}

    @app.post("/api/state/simulate/{state_name}")
    def simulate_state(state_name: str, request: Request):
        """
        Apply a named preset to the simulated printer state and trigger
        the LedManager just like a live Moonraker event would.
        Supported: idle, heating, printing, error
        """
        s = _printer_state(request)
        led_manager = _led_manager(request)

        presets: Dict[str, dict] = {
            "idle": {
                "print_state": "idle",
                "progress": 0,
                "extruder_temperature": 25,
                "target_extruder_temperature": 0,
                "heater_bed_temperature": 25,
                "target_heater_bed_temperature": 0,
            },
            "heating": {
                "print_state": "printing",
                "progress": 0,
                "extruder_temperature": 80,
                "target_extruder_temperature": 210,
                "heater_bed_temperature": 30,
                "target_heater_bed_temperature": 60,
            },
            "printing": {
                "print_state": "printing",
                "progress": 0.45,
                "extruder_temperature": 210,
                "target_extruder_temperature": 210,
                "heater_bed_temperature": 60,
                "target_heater_bed_temperature": 60,
                "z_position": 12.4,
            },
            "error": {
                "print_state": "error",
                "progress": 0,
            },
        }

        preset = presets.get(state_name.lower())
        if not preset:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown state '{state_name}'. Choose from: {list(presets.keys())}",
            )

        for key, value in preset.items():
            setattr(s, key, value)

        # Recalculate derived progress fields
        if s.target_extruder_temperature > 0:
            s.extruder_target_progress = (s.extruder_temperature / s.target_extruder_temperature) * 100
        if s.target_heater_bed_temperature > 0:
            s.heater_bed_target_progress = (s.heater_bed_temperature / s.target_heater_bed_temperature) * 100

        # Switch to auto so the led_manager drives segments from the preset state
        request.app.state.mode = "auto"
        led_manager.update(s)

        return {"ok": True, "simulated_state": state_name, "mode": "auto"}

    return app
