from __future__ import annotations

from cube.cube_state import CubeState
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType


class CubeAnalyzer:
    """
    Read-only analysis of a CubeState.

    Every check here is defined relative to the CubeState's own
    CubeOrientation, never a hardcoded canonical orientation. A solved
    CubeState expressed in any of the twenty-four legal Cube Orientations
    reports zero errors from every method on this class.
    """

    @staticmethod
    def is_solved(cube: CubeState) -> bool:
        """
        Returns whether every visible sticker matches its face center.
        """
        return cube.solved

    @staticmethod
    def is_correctly_placed(
        cube: CubeState,
        piece_state: PieceState,
    ) -> bool:
        """
        Returns True if the Piece occupies the Position whose expected
        colors, under the CubeState's current CubeOrientation, match the
        Piece's own colors.

        This ignores the Piece's specific PieceOrientation: a correctly
        placed Piece may still be misoriented. See `is_correctly_oriented`.
        """
        expected_colors = frozenset(
            cube.orientation.color_at(face)
            for face in piece_state.position.ordered_faces
        )

        return piece_state.piece.signature.colors == expected_colors

    @staticmethod
    def is_correctly_oriented(
        cube: CubeState,
        piece_state: PieceState,
    ) -> bool:
        """
        Returns True if the Piece is correctly placed and shows the exact
        expected color, per the current CubeOrientation, on every face it
        occupies.
        """
        if not CubeAnalyzer.is_correctly_placed(cube, piece_state):
            return False

        return all(
            piece_state.color_on(face) is cube.orientation.color_at(face)
            for face in piece_state.position.ordered_faces
        )

    @staticmethod
    def misplaced_pieces(cube: CubeState) -> tuple[PieceState, ...]:
        """
        Returns every PieceState occupying the wrong Position.
        """
        return tuple(
            piece_state
            for piece_state in cube
            if not CubeAnalyzer.is_correctly_placed(cube, piece_state)
        )

    @staticmethod
    def misplaced_edges(cube: CubeState) -> tuple[PieceState, ...]:
        """
        Returns every Edge PieceState occupying the wrong Position.
        """
        return tuple(
            piece_state
            for piece_state in CubeAnalyzer.misplaced_pieces(cube)
            if piece_state.piece_type is PieceType.EDGE
        )

    @staticmethod
    def misplaced_corners(cube: CubeState) -> tuple[PieceState, ...]:
        """
        Returns every Corner PieceState occupying the wrong Position.
        """
        return tuple(
            piece_state
            for piece_state in CubeAnalyzer.misplaced_pieces(cube)
            if piece_state.piece_type is PieceType.CORNER
        )

    @staticmethod
    def edge_orientation_errors(cube: CubeState) -> tuple[PieceState, ...]:
        """
        Returns every correctly placed Edge that is flipped: it occupies
        the right Position but shows the wrong color on an occupied face.
        """
        return tuple(
            piece_state
            for piece_state in cube
            if piece_state.piece_type is PieceType.EDGE
            and CubeAnalyzer.is_correctly_placed(cube, piece_state)
            and not CubeAnalyzer.is_correctly_oriented(cube, piece_state)
        )

    @staticmethod
    def corner_orientation_errors(cube: CubeState) -> tuple[PieceState, ...]:
        """
        Returns every correctly placed Corner that is twisted: it occupies
        the right Position but shows the wrong color on an occupied face.
        """
        return tuple(
            piece_state
            for piece_state in cube
            if piece_state.piece_type is PieceType.CORNER
            and CubeAnalyzer.is_correctly_placed(cube, piece_state)
            and not CubeAnalyzer.is_correctly_oriented(cube, piece_state)
        )
