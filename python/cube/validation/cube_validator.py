from __future__ import annotations

from cube.cube_state import CubeState
from cube.orientation.cube_orientation import CubeOrientation
from cube.piece.piece import Piece
from cube.piece.piece_type import PieceType


class PieceValidator:
    """Validates legal physical cube pieces."""

    @staticmethod
    def is_valid(piece: Piece) -> bool:
        if not isinstance(piece, Piece):
            return False

        colors = piece.signature.colors

        return (
            len(colors) == piece.piece_type.color_count
            and all(color.opposite not in colors for color in colors)
            and piece.layout.colors == colors
            and piece.layout.piece_type is piece.piece_type
        )


class CubeOrientationValidator:
    """Validates CubeOrientation instances."""

    @staticmethod
    def is_valid(orientation: CubeOrientation) -> bool:
        if not isinstance(orientation, CubeOrientation):
            return False

        try:
            return (
                CubeOrientation.from_top_front(
                    orientation.top,
                    orientation.front,
                )
                == orientation
            )
        except ValueError:
            return False


class CubeStateValidator:
    """Validates complete CubeState instances."""

    @staticmethod
    def is_valid(cube: CubeState) -> bool:
        return not CubeStateValidator.validate(cube)

    @staticmethod
    def validate(cube: CubeState) -> tuple[str, ...]:
        """Returns every detectable structural validation error."""
        if not isinstance(cube, CubeState):
            return ("CubeState is required.",)

        errors = []

        if not CubeOrientationValidator.is_valid(cube.orientation):
            errors.append("CubeOrientation is invalid.")

        if len(cube) != 26:
            errors.append("CubeState must contain exactly 26 PieceStates.")

        if len({state.piece.signature for state in cube}) != 26:
            errors.append("CubeState contains duplicate PieceSignatures.")

        if len({state.position for state in cube}) != 26:
            errors.append("CubeState contains duplicate Positions.")

        if not all(PieceValidator.is_valid(state.piece) for state in cube):
            errors.append("CubeState contains an invalid Piece.")

        if not all(
            state.position.position_type.face_count
            == state.piece_type.color_count
            for state in cube
        ):
            errors.append("CubeState contains an incompatible Piece and Position.")

        return tuple(errors)
