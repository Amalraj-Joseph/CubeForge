from __future__ import annotations

from dataclasses import dataclass, field

from cube.face.logical_face import LogicalFace
from cube.position.position_type import PositionType


@dataclass(frozen=True, slots=True, init=False)
class Position:
    """
    Immutable logical location within the cube.

    A Position consists of

    - PositionType
    - unordered set of LogicalFaces

    Position identity is independent of notation.
    """

    position_type: PositionType
    _faces: frozenset[LogicalFace] = field(repr=False)

    def __init__(
        self,
        position_type: PositionType,
        *faces: LogicalFace,
    ):
        if not faces:
            raise ValueError(
                "At least one LogicalFace must be provided."
            )

        unique_faces = frozenset(faces)

        if len(unique_faces) != len(faces):
            raise ValueError(
                "Duplicate LogicalFaces are not permitted."
            )

        expected = position_type.face_count

        if len(unique_faces) != expected:
            raise ValueError(
                f"{position_type.display_name} requires "
                f"{expected} logical faces, "
                f"got {len(unique_faces)}."
            )

        object.__setattr__(
            self,
            "position_type",
            position_type,
        )

        object.__setattr__(
            self,
            "_faces",
            unique_faces,
        )

    @property
    def faces(self) -> frozenset[LogicalFace]:
        """
        Returns the unordered immutable set of logical faces.
        """
        return self._faces

    @property
    def ordered_faces(self) -> tuple[LogicalFace, ...]:
        """
        Returns the logical faces in canonical order.
        """
        return tuple(
            sorted(
                self._faces,
                key=lambda face: face.bit_index,
            )
        )

    def contains(
        self,
        face: LogicalFace,
    ) -> bool:
        """
        Returns True if this Position contains the given LogicalFace.
        """
        return face in self._faces

    @property
    def notation(self) -> str:
        """
        Returns the canonical position notation.

        Examples

        U
        UF
        UFR
        """
        return "".join(
            face.symbol
            for face in self.ordered_faces
        )

    @property
    def description(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"{self.position_type.display_name}"
            f"({self.notation})"
        )

    def describe(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.description