# CubeCore

CubeCore is an immutable Rubik's Cube library.

## Quick Start

### Canonical Solved Cube

```python
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)

cube = CANONICAL_CUBE_STATE
```

---

### Applying a Move

```python
from cube.cube_transformer import (
    CubeTransformer,
)
from cube.internal.canonical_moves import (
    R,
)

cube = CubeTransformer.apply(
    CANONICAL_CUBE_STATE,
    R,
)
```

---

### Parsing an Algorithm

```python
from cube.notation.algorithm_parser import (
    parse_algorithm,
)

algorithm = parse_algorithm(
    "R U R' U'"
)
```

---

### Executing an Algorithm

```python
from cube.cube_transformer import (
    CubeTransformer,
)

cube = CubeTransformer.apply_algorithm(
    CANONICAL_CUBE_STATE,
    algorithm,
)
```

---

### Formatting an Algorithm

```python
from cube.notation.algorithm_formatter import (
    format_algorithm,
)

notation = format_algorithm(
    algorithm,
)

print(notation)

# R U R' U'
```

---

### Generating a Scramble

```python
from cube.scramble.scramble_generator import (
    ScrambleGenerator,
)

scramble = ScrambleGenerator.generate()

print(scramble.notation)

# Example:
# U2 R F' L2 D B U' ...
```

---

## Running the Tests

```bash
pytest
```