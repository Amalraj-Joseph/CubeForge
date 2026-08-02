from __future__ import annotations

from cube.cube_state import CubeState
from cube.internal.move_cycles import PositionCycle
from cube.internal.move_transformations import (
    MOVE_TRANSFORMATIONS,
    MoveTransformation,
)
from cube.move.move import Move
from cube.move.rotation import Rotation
from cube.piece.piece import Piece
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.algorithm.algorithm import Algorithm


class CubeTransformer:
    """
    Applies Moves to immutable CubeStates.
    """

    @staticmethod
    def apply(
        cube: CubeState,
        move: Move,
    ) -> CubeState:
        """
        Applies a Move to a CubeState.
        """
        transformation = MOVE_TRANSFORMATIONS[
            Move(
                move.face,
                Rotation.CLOCKWISE,
            )
        ]

        state = cube

        for _ in range(
            move.rotation.quarter_turns
        ):
            state = CubeTransformer._apply_transformation(
                state,
                transformation,
            )

        return state
    
    @staticmethod
    def apply_algorithm(
        cube: CubeState,
        algorithm: Algorithm,
    ) -> CubeState:
        """
        Applies an Algorithm to a CubeState.
        """
        state = cube

        for move in algorithm:
            state = CubeTransformer.apply(
                state,
                move,
            )

        return state

    @staticmethod
    def _apply_transformation(
        cube: CubeState,
        transformation: MoveTransformation,
    ) -> CubeState:
        """
        Applies a single canonical clockwise MoveTransformation.
        """
        moved = {
            **CubeTransformer._cycle(
                cube,
                transformation.edge_cycle,
                transformation.orientation_rule,
            ),
            **CubeTransformer._cycle(
                cube,
                transformation.corner_cycle,
                transformation.orientation_rule,
            ),
        }

        piece_states = [
            moved.get(
                piece_state.piece,
                piece_state,
            )
            for piece_state in cube
        ]

        return CubeState(*piece_states)

    @staticmethod
    def _cycle(
        cube: CubeState,
        cycle: PositionCycle,
        rule,
    ) -> dict[Piece, PieceState]:
        """
        Cycles PieceStates around a PositionCycle.
        """
        result: dict[Piece, PieceState] = {}

        positions = cycle.positions
        count = len(positions)

        for index, destination in enumerate(positions):
            source = positions[
                (index - 1) % count
            ]

            source_state = cube.piece_at(source)

            orientation = source_state.orientation

            if (
                source_state.piece_type
                is PieceType.EDGE
            ):
                if rule.edge_flip:
                    orientation = orientation.rotate(1)

            elif (
                source_state.piece_type
                is PieceType.CORNER
            ):
                orientation = orientation.rotate(
                    rule.corner_twists[index]
                )

            result[
                source_state.piece
            ] = PieceState(
                source_state.piece,
                destination,
                orientation,
            )

        return result