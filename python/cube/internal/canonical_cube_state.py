from cube.cube_state import CubeState
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.orientation.cube_orientation import CANONICAL_ORIENTATION
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState


CANONICAL_CUBE_STATE = CubeState(
    CANONICAL_ORIENTATION,
    *(
        PieceState(
            piece,
            position,
            PieceOrientation(
                piece.signature.piece_type,
                0,
            ),
        )
        for piece, position in CANONICAL_CUBE.items()
    )
)
