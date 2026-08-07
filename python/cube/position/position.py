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
    - ordered LogicalFaces defining the canonical position

    Position equality is independent of face ordering.
    """

    position_type: PositionType

    _faces: tuple[
        LogicalFace,
        ...
    ] = field(repr=False)

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

        if len(faces) != expected:
            raise ValueError(
                f"{position_type.display_name} requires "
                f"{expected} logical faces, "
                f"got {len(faces)}."
            )

        object.__setattr__(
            self,
            "position_type",
            position_type,
        )

        object.__setattr__(
            self,
            "_faces",
            tuple(faces),
        )

    @property
    def faces(
        self,
    ) -> frozenset[LogicalFace]:
        """
        Returns the unordered immutable set of LogicalFaces.
        """
        return frozenset(self._faces)

    @property
    def ordered_faces(
        self,
    ) -> tuple[
        LogicalFace,
        ...,
    ]:
        """
        Returns the canonical ordered LogicalFaces.
        """
        return self._faces

    def contains(
        self,
        face: LogicalFace,
    ) -> bool:
        """
        Returns True if this Position contains the given
        LogicalFace.
        """
        return face in self._faces

    @property
    def notation(
        self,
    ) -> str:
        """
        Returns the canonical position notation.
        """
        return "".join(
            face.symbol
            for face in self._faces
        )

    @property
    def description(
        self,
    ) -> str:
        """
        Returns a human-readable description.
        """
        return self.notation

    def describe(
        self,
    ) -> str:
        return self.description

    def __str__(
        self,
    ) -> str:
        return self.description

    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, Position):
            return NotImplemented

        return (
            self.position_type is other.position_type
            and self.faces == other.faces
        )

    def __hash__(
        self,
    ) -> int:
        return hash(
            (
                self.position_type,
                self.faces,
            )
        )
