from __future__ import annotations

from dataclasses import dataclass, field

from cube.face.logical_face import LogicalFace


@dataclass(frozen=True, slots=True, init=False)
class CubeTransformation:
    """
    Immutable physical rotation of the entire cube.

    The face mapping maps a source logical face to its destination logical
    face after the rotation.
    """

    _destinations: tuple[LogicalFace, ...] = field(repr=False)
    _name: str | None = field(default=None, repr=False, compare=False)

    def __init__(
        self,
        face_mapping: dict[LogicalFace, LogicalFace],
        *,
        name: str | None = None,
    ):
        if set(face_mapping) != set(LogicalFace):
            raise ValueError(
                "CubeTransformation must map every LogicalFace exactly once."
            )

        destinations = tuple(
            face_mapping[face]
            for face in LogicalFace
        )

        if len(set(destinations)) != len(LogicalFace):
            raise ValueError(
                "CubeTransformation face mapping must be bijective."
            )

        for face in LogicalFace:
            if (
                face_mapping[face.opposite]
                is not face_mapping[face].opposite
            ):
                raise ValueError(
                    "CubeTransformation must preserve opposite faces."
                )

        if _determinant(destinations) != 1:
            raise ValueError(
                "CubeTransformation must preserve cube handedness."
            )

        object.__setattr__(self, "_destinations", destinations)
        object.__setattr__(self, "_name", name)

    def map_face(
        self,
        face: LogicalFace,
    ) -> LogicalFace:
        """
        Returns the destination of a source logical face.
        """
        return self._destinations[face.bit_index]

    def source_for(
        self,
        destination: LogicalFace,
    ) -> LogicalFace:
        """
        Returns the source face that maps to the given destination.
        """
        return next(
            face
            for face in LogicalFace
            if self.map_face(face) is destination
        )

    def inverse(self) -> CubeTransformation:
        """
        Returns the inverse physical rotation.
        """
        return CubeTransformation({
            self.map_face(face): face
            for face in LogicalFace
        })

    def then(
        self,
        following: CubeTransformation,
    ) -> CubeTransformation:
        """
        Returns the transformation obtained by applying self then following.
        """
        return CubeTransformation({
            face: following.map_face(self.map_face(face))
            for face in LogicalFace
        })

    @property
    def name(self) -> str | None:
        """
        Returns the stable identifier for a primitive transformation.
        """
        return self._name

    def describe(self) -> str:
        if self._name is not None:
            return self._name.replace("_", " ").title()

        mappings = ", ".join(
            f"{face.symbol}->{self.map_face(face).symbol}"
            for face in LogicalFace
        )
        return f"Cube Transformation({mappings})"

    def __str__(self) -> str:
        return self.describe()


_FACE_VECTORS: dict[LogicalFace, tuple[int, int, int]] = {
    LogicalFace.RIGHT: (1, 0, 0),
    LogicalFace.LEFT: (-1, 0, 0),
    LogicalFace.UP: (0, 1, 0),
    LogicalFace.DOWN: (0, -1, 0),
    LogicalFace.FRONT: (0, 0, 1),
    LogicalFace.BACK: (0, 0, -1),
}


def _determinant(destinations: tuple[LogicalFace, ...]) -> int:
    right = _FACE_VECTORS[destinations[LogicalFace.RIGHT.bit_index]]
    up = _FACE_VECTORS[destinations[LogicalFace.UP.bit_index]]
    front = _FACE_VECTORS[destinations[LogicalFace.FRONT.bit_index]]

    return (
        right[0] * (up[1] * front[2] - up[2] * front[1])
        - right[1] * (up[0] * front[2] - up[2] * front[0])
        + right[2] * (up[0] * front[1] - up[1] * front[0])
    )


def _primitive(
    name: str,
    **mapping: LogicalFace,
) -> CubeTransformation:
    return CubeTransformation(
        {
            LogicalFace.UP: mapping["up"],
            LogicalFace.DOWN: mapping["down"],
            LogicalFace.FRONT: mapping["front"],
            LogicalFace.BACK: mapping["back"],
            LogicalFace.LEFT: mapping["left"],
            LogicalFace.RIGHT: mapping["right"],
        },
        name=name,
    )


ROTATE_LEFT = _primitive(
    "rotate_left",
    up=LogicalFace.UP,
    down=LogicalFace.DOWN,
    front=LogicalFace.LEFT,
    back=LogicalFace.RIGHT,
    left=LogicalFace.BACK,
    right=LogicalFace.FRONT,
)

ROTATE_RIGHT = _primitive(
    "rotate_right",
    up=LogicalFace.UP,
    down=LogicalFace.DOWN,
    front=LogicalFace.RIGHT,
    back=LogicalFace.LEFT,
    left=LogicalFace.FRONT,
    right=LogicalFace.BACK,
)

ROTATE_UP = _primitive(
    "rotate_up",
    up=LogicalFace.FRONT,
    down=LogicalFace.BACK,
    front=LogicalFace.DOWN,
    back=LogicalFace.UP,
    left=LogicalFace.LEFT,
    right=LogicalFace.RIGHT,
)

ROTATE_DOWN = _primitive(
    "rotate_down",
    up=LogicalFace.BACK,
    down=LogicalFace.FRONT,
    front=LogicalFace.UP,
    back=LogicalFace.DOWN,
    left=LogicalFace.LEFT,
    right=LogicalFace.RIGHT,
)

ROLL_CLOCKWISE = _primitive(
    "roll_clockwise",
    up=LogicalFace.RIGHT,
    down=LogicalFace.LEFT,
    front=LogicalFace.FRONT,
    back=LogicalFace.BACK,
    left=LogicalFace.UP,
    right=LogicalFace.DOWN,
)

ROLL_COUNTERCLOCKWISE = _primitive(
    "roll_counterclockwise",
    up=LogicalFace.LEFT,
    down=LogicalFace.RIGHT,
    front=LogicalFace.FRONT,
    back=LogicalFace.BACK,
    left=LogicalFace.DOWN,
    right=LogicalFace.UP,
)
