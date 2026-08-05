from __future__ import annotations

from cube.cube_state import CubeState
from cube.face.logical_face import LogicalFace
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
from cube.piece.piece_orientation import PieceOrientation
from cube.position.position import Position
from cube.transformation.cube_transformation import CubeTransformation
from cube.algorithm.algorithm import Algorithm
from cube.internal.canonical_positions import ALL_POSITIONS
from cube.internal.piece_projection import project_at_position
from cube.orientation.cube_orientation import CubeOrientation


_POSITION_BY_FACES = {
    position.faces: position
    for position in ALL_POSITIONS
}


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
    def apply_transformation(
        cube: CubeState,
        transformation: CubeTransformation,
    ) -> CubeState:
        """
        Applies a physical whole-cube transformation.
        """
        orientation = CubeTransformer._transform_orientation(
            cube.orientation,
            transformation,
        )

        piece_states = tuple(
            CubeTransformer._transform_piece_state(
                piece_state,
                transformation,
            )
            for piece_state in cube
        )

        return CubeState(orientation, *piece_states)

    @staticmethod
    def apply_transformations(
        cube: CubeState,
        *transformations: CubeTransformation,
    ) -> CubeState:
        """
        Applies whole-cube transformations sequentially from left to right.
        """
        state = cube

        for transformation in transformations:
            state = CubeTransformer.apply_transformation(
                state,
                transformation,
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

        return CubeState(cube.orientation, *piece_states)

    @staticmethod
    def _transform_orientation(
        orientation: CubeOrientation,
        transformation: CubeTransformation,
    ):
        return orientation.from_top_front(
            orientation.color_at(
                transformation.source_for(LogicalFace.UP)
            ),
            orientation.color_at(
                transformation.source_for(LogicalFace.FRONT)
            ),
        )

    @staticmethod
    def _transform_piece_state(
        piece_state: PieceState,
        transformation: CubeTransformation,
    ) -> PieceState:
        position = CubeTransformer._transform_position(
            piece_state.position,
            transformation,
        )

        colors = {
            transformation.map_face(face): color
            for face, color in piece_state.projected_layout.stickers
        }

        orientation = CubeTransformer._orientation_for_colors(
            piece_state,
            position,
            colors,
        )

        return PieceState(
            piece_state.piece,
            position,
            orientation,
        )

    @staticmethod
    def _transform_position(
        position: Position,
        transformation: CubeTransformation,
    ) -> Position:
        faces = frozenset(
            transformation.map_face(face)
            for face in position.faces
        )

        return _POSITION_BY_FACES[faces]

    @staticmethod
    def _orientation_for_colors(
        piece_state: PieceState,
        position: Position,
        colors,
    ) -> PieceOrientation:
        for value in range(piece_state.piece_type.color_count):
            orientation = PieceOrientation(
                piece_state.piece_type,
                value,
            )
            projected = project_at_position(
                piece_state.piece.layout,
                orientation,
                position,
            )

            if all(
                projected.color_on(face) is color
                for face, color in colors.items()
            ):
                return orientation

        raise ValueError(
            "CubeTransformation produced an invalid PieceState."
        )

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
