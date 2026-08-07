from __future__ import annotations

import json

from cube.color.color import Color
from cube.cube_state import CubeState
from cube.internal.canonical_pieces import ALL_PIECES
from cube.notation.singmaster import (
    from_position_notation,
    to_position_notation,
)
from cube.orientation.cube_orientation import CubeOrientation
from cube.piece.piece import Piece
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType

FORMAT_VERSION = "1"
"""
Identifies the shape of every format produced by CubeSerializer.

Bumped whenever a format's schema changes in a way that is not
backwards-compatible. Deserializers reject any other value rather than
guessing at how to interpret unrecognized data.
"""

_PIECES_BY_SIGNATURE: dict[PieceSignature, Piece] = {
    piece.signature: piece
    for piece in ALL_PIECES
}

_COLOR_BY_INITIAL: dict[str, Color] = {
    color.name[0]: color
    for color in Color
}


class CubeSerializer:
    """
    Converts a CubeState to and from portable representations.

    Every format embeds an explicit `format_version` so that a future,
    incompatible wire format can be introduced without silently
    misinterpreting data written by an older version. Deserialization
    always reconstructs a CubeState through its normal constructor, so
    every invariant CubeState already enforces (structural validity,
    orientation legality, parity) applies equally to deserialized data.
    """

    # ------------------------------------------------------------------
    # dict
    # ------------------------------------------------------------------

    @staticmethod
    def to_dict(cube: CubeState) -> dict:
        """
        Returns a JSON-serializable dict representing the given CubeState.
        """
        return {
            "format_version": FORMAT_VERSION,
            "orientation": {
                "up": cube.orientation.up.name,
                "front": cube.orientation.front.name,
            },
            "pieces": [
                {
                    "position": to_position_notation(piece_state.position),
                    "colors": [
                        color.name
                        for color in piece_state.piece.signature.ordered_colors
                    ],
                    "orientation": piece_state.orientation.value,
                }
                for piece_state in cube
            ],
        }

    @staticmethod
    def from_dict(data: dict) -> CubeState:
        """
        Returns the CubeState represented by the given dict.

        Raises:
            ValueError: If the dict is malformed, has an unsupported
                format_version, or describes an invalid CubeState.
        """
        if not isinstance(data, dict):
            raise ValueError("Serialized CubeState must be an object.")

        version = data.get("format_version")

        if version != FORMAT_VERSION:
            raise ValueError(
                f"Unsupported CubeState format_version: {version!r}. "
                f"Expected {FORMAT_VERSION!r}."
            )

        try:
            orientation_data = data["orientation"]
            orientation = CubeOrientation.from_top_front(
                Color[orientation_data["up"]],
                Color[orientation_data["front"]],
            )

            piece_states = tuple(
                CubeSerializer._piece_state_from_dict(entry)
                for entry in data["pieces"]
            )
        except (KeyError, TypeError) as ex:
            raise ValueError(
                f"Malformed serialized CubeState: {ex}"
            ) from ex

        return CubeState(orientation, *piece_states)

    @staticmethod
    def _piece_state_from_dict(entry: dict) -> PieceState:
        position = from_position_notation(entry["position"])
        piece_type = PieceType(position.position_type.value)
        colors = tuple(Color[name] for name in entry["colors"])
        piece = _piece_for(piece_type, colors)

        return PieceState(
            piece,
            position,
            PieceOrientation(piece_type, entry["orientation"]),
        )

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    @staticmethod
    def to_json(cube: CubeState) -> str:
        """
        Returns a JSON string representing the given CubeState.
        """
        return json.dumps(CubeSerializer.to_dict(cube), sort_keys=True)

    @staticmethod
    def from_json(text: str) -> CubeState:
        """
        Returns the CubeState represented by the given JSON string.

        Raises:
            ValueError: If the text is not valid JSON, or describes an
                invalid CubeState.
        """
        try:
            data = json.loads(text)
        except json.JSONDecodeError as ex:
            raise ValueError(f"Invalid JSON: {ex}") from ex

        return CubeSerializer.from_dict(data)

    # ------------------------------------------------------------------
    # Compact string
    # ------------------------------------------------------------------
    #
    # Grammar:
    #
    #   <compact-string> ::= <version> ":" <up-initial> <front-initial>
    #                        "|" <piece> (";" <piece>)*
    #   <piece>          ::= <position-notation> "=" <color-initials>
    #                        <orientation-digit>
    #
    # Example (canonical solved cube):
    #
    #   1:WG|U=W0;D=Y0;F=G0;...;UF=WG0;...;UFR=WGR0;...
    #

    @staticmethod
    def to_compact_string(cube: CubeState) -> str:
        """
        Returns a compact single-line string representing the given
        CubeState.
        """
        header = (
            f"{FORMAT_VERSION}:"
            f"{cube.orientation.up.name[0]}{cube.orientation.front.name[0]}"
        )

        pieces = ";".join(
            CubeSerializer._piece_token(piece_state)
            for piece_state in cube
        )

        return f"{header}|{pieces}"

    @staticmethod
    def _piece_token(piece_state: PieceState) -> str:
        colors = "".join(
            color.name[0]
            for color in piece_state.piece.signature.ordered_colors
        )

        return (
            f"{to_position_notation(piece_state.position)}="
            f"{colors}{piece_state.orientation.value}"
        )

    @staticmethod
    def from_compact_string(text: str) -> CubeState:
        """
        Returns the CubeState represented by the given compact string.

        Raises:
            ValueError: If the text is malformed, has an unsupported
                format_version, or describes an invalid CubeState.
        """
        try:
            header, body = text.split("|", 1)
            version, orientation_code = header.split(":", 1)
        except ValueError as ex:
            raise ValueError(
                f"Malformed CubeState compact string: {text!r}"
            ) from ex

        if version != FORMAT_VERSION:
            raise ValueError(
                f"Unsupported CubeState format_version: {version!r}. "
                f"Expected {FORMAT_VERSION!r}."
            )

        if len(orientation_code) != 2:
            raise ValueError(
                f"Malformed CubeState orientation code: {orientation_code!r}"
            )

        orientation = CubeOrientation.from_top_front(
            _color_from_initial(orientation_code[0]),
            _color_from_initial(orientation_code[1]),
        )

        piece_states = tuple(
            CubeSerializer._piece_state_from_compact_token(token)
            for token in body.split(";")
        )

        return CubeState(orientation, *piece_states)

    @staticmethod
    def _piece_state_from_compact_token(token: str) -> PieceState:
        try:
            position_code, rest = token.split("=", 1)
            color_codes, orientation_digit = rest[:-1], rest[-1]
        except (ValueError, IndexError) as ex:
            raise ValueError(f"Malformed piece token: {token!r}") from ex

        if not color_codes or not orientation_digit.isdigit():
            raise ValueError(f"Malformed piece token: {token!r}")

        position = from_position_notation(position_code)
        piece_type = PieceType(position.position_type.value)
        colors = tuple(_color_from_initial(ch) for ch in color_codes)
        piece = _piece_for(piece_type, colors)

        return PieceState(
            piece,
            position,
            PieceOrientation(piece_type, int(orientation_digit)),
        )


def _piece_for(piece_type: PieceType, colors: tuple[Color, ...]):
    try:
        return _PIECES_BY_SIGNATURE[PieceSignature(piece_type, *colors)]
    except KeyError as ex:
        raise ValueError(f"Unknown piece signature: {colors!r}") from ex


def _color_from_initial(initial: str) -> Color:
    try:
        return _COLOR_BY_INITIAL[initial]
    except KeyError as ex:
        raise ValueError(f"Unknown color initial: {initial!r}") from ex
