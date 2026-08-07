from __future__ import annotations

from cube.algorithm.algorithm import Algorithm
from cube.analysis.cube_analyzer import CubeAnalyzer
from cube.cube_state import CubeState
from cube.face.logical_face import LogicalFace
from cube.piece.piece_type import PieceType


class CubeStatistics:
    """
    Aggregate numeric statistics derived from a CubeState or an Algorithm.
    """

    @staticmethod
    def move_count(algorithm: Algorithm) -> int:
        """
        Returns the number of Moves in an Algorithm.
        """
        return len(algorithm)

    @staticmethod
    def solved_faces(cube: CubeState) -> int:
        """
        Returns the number of Logical Faces whose visible stickers are
        all a single uniform color, per the CubeState's current
        CubeOrientation.
        """
        return sum(
            1
            for face in LogicalFace
            if all(
                piece_state.color_on(face) is cube.orientation.color_at(face)
                for piece_state in cube
                if piece_state.occupies(face)
            )
        )

    @staticmethod
    def solved_edges(cube: CubeState) -> int:
        """
        Returns the number of correctly placed and correctly oriented
        Edges.
        """
        return sum(
            1
            for piece_state in cube
            if piece_state.piece_type is PieceType.EDGE
            and CubeAnalyzer.is_correctly_oriented(cube, piece_state)
        )

    @staticmethod
    def solved_corners(cube: CubeState) -> int:
        """
        Returns the number of correctly placed and correctly oriented
        Corners.
        """
        return sum(
            1
            for piece_state in cube
            if piece_state.piece_type is PieceType.CORNER
            and CubeAnalyzer.is_correctly_oriented(cube, piece_state)
        )