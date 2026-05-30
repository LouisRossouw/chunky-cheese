from fastapi import APIRouter, BackgroundTasks, Request, Depends
from pydantic import BaseModel
from typing import List, Tuple
from core.config import Config

from core.dot_squad import DotSquad

router = APIRouter()


class Frame(BaseModel):
    colors: List[Tuple[int, int, int]]
    duration: float


class Animation(BaseModel):
    name: str
    loop: bool = False
    frames: List[Frame]


def get_ds(request: Request) -> DotSquad:
    return request.app.state.ds


def get_config(request: Request) -> Config:
    return request.app.state.config


@router.get("/")
def root():
    return {"info": "Dot-Squad led service"}


@router.post("/run/{notification}")
def run_led(notification: str, background_tasks: BackgroundTasks, DS=Depends(get_ds), config=Depends(get_config)):
    background_tasks.add_task(DS.run, config.anims.get(notification))

    return {"ok": True}


@router.post("/run-sequence")
def run_led_sequence(anim: Animation, background_tasks: BackgroundTasks, DS=Depends(get_ds)):
    background_tasks.add_task(DS.run, anim.frames)

    return {"ok": True}
