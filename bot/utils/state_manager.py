# -*- coding: utf-8 -*-

from typing import Any, Optional


class StateManager:
    def __init__(self):
        self._states = {}

    def create_state(
            self,
            state_id: int,
            state_data: Optional[dict] = None):
        self._states[state_id] = state_data or {}

    def get_state_data(
            self,
            state_id: int,
            state_data_name: Optional[str] = None) -> Optional[dict]:
        try:
            state_data = self._states[state_id]
        except KeyError:
            raise StateNotFound(state_id)

        if state_data_name:
            try:
                return state_data[state_data_name]
            except KeyError:
                raise StateDataNotFound(state_id)
        return state_data

    def set_state_data(self, state_id: int, state_name: str, state_data: Any):
        try:
            self._states[state_id][state_name] = state_data
        except KeyError:
            self.create_state(
                state_id=state_id,
                state_data={state_name: state_data}
            )

    def del_state(self, state_id: int):
        try:
            del self._states[state_id]
        except KeyError:
            pass


class StateNotFound(Exception):
    def __init__(self, state_id: int):
        self._state_id = state_id

    def __str__(self) -> str:
        return f"State `{self._state_id}` not found"


class StateDataNotFound(Exception):
    def __init__(self, state_data_name: int):
        self._state_data_name = state_data_name

    def __str__(self) -> str:
        return f"State data `{self._state_data_name}` not found"
