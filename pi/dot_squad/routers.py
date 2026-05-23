from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Tuple

from led_map import led_animations
from led import run

router = APIRouter()


class Frame(BaseModel):
    colors: List[Tuple[int, int, int]]
    duration: float


class Animation(BaseModel):
    name: str
    loop: bool = False
    frames: List[Frame]


@router.get("/")
def root():
    return {"info": "Dot-Squad led service"}


@router.post("/run/{notification}")
def run_led(notification: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run, led_animations.get(notification))
    return {"ok": True}


@router.post("/run-sequence")
def run_led_sequence(anim: Animation, background_tasks: BackgroundTasks):
    background_tasks.add_task(run, anim.frames)

    return {"ok": True}
