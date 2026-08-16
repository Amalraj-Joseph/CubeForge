---
layout: home
title: Home
---

<section class="hero">
  <div class="hero__copy">
    <p class="eyebrow">Pure Python · Zero dependencies · Spec-verified</p>
    <h1>CubeForge</h1>
    <p class="hero__lede">
      A rigorously specified Rubik's Cube engine. Every invariant a
      physical cube actually has &mdash; exactly twenty-six pieces, legal
      orientation and permutation parity, opposite colors never sharing
      a piece &mdash; is enforced the moment a <code>Cube</code> is
      constructed. An illegal state isn't checked for and rejected; it's
      structurally impossible to represent.
    </p>
    <div class="hero__code">
      <pre><code>from cube import Cube, R

cube = Cube.canonical()
cube.solved            # True

cube = cube.apply(R)
cube.solved            # False</code></pre>
    </div>
    <div class="hero__ctas">
      <a class="btn btn--primary" href="{{ '/getting-started.html' | relative_url }}">Get started &rarr;</a>
      <a class="btn btn--ghost" href="{{ site.github_repo }}">View source &#8599;</a>
    </div>
  </div>

  <div class="hero__cube">
    {% include cube-diagram.html
       up="w,w,w,w,w,w,w,w,w"
       front="g,g,g,g,g,g,g,g,g"
       right="r,r,r,r,r,r,r,r,r"
       size="260"
       caption="Cube.canonical() — the one, unique solved state" %}
  </div>
</section>

<section class="stats wrap">
  <div class="stat"><strong>26</strong><span>pieces</span></div>
  <div class="stat"><strong>24</strong><span>legal orientations</span></div>
  <div class="stat"><strong>18</strong><span>standard moves</span></div>
  <div class="stat"><strong>0</strong><span>runtime dependencies</span></div>
  <div class="stat"><strong>865+</strong><span>tests, incl. a per-requirement compliance audit</span></div>
</section>

<section class="section wrap">
  <h2>Start here</h2>
  <div class="cards">
    <a class="card" href="{{ '/getting-started.html' | relative_url }}">
      {% include cube-glyph.html face="w,w,w,w,w,w,w,w,w" %}
      <span class="card__title">Getting Started</span>
      <p class="card__desc">Install the engine and walk through construction, moves, algorithms, and serialization.</p>
      <span class="card__arrow">Read &rarr;</span>
    </a>
    <a class="card" href="{{ '/architecture.html' | relative_url }}">
      {% include cube-glyph.html face="g,b,r,o,w,y,b,g,r" %}
      <span class="card__title">Architecture</span>
      <p class="card__desc">The domain model, built up from colors and pieces to cube state and transformations.</p>
      <span class="card__arrow">Read &rarr;</span>
    </a>
    <a class="card" href="{{ '/api-reference.html' | relative_url }}">
      {% include cube-glyph.html face="b,b,b,b,b,b,b,b,b" %}
      <span class="card__title">API Reference</span>
      <p class="card__desc">Everything reachable from <code>import cube</code>. The contract, if you're building on it.</p>
      <span class="card__arrow">Read &rarr;</span>
    </a>
    <a class="card" href="{{ '/specification.html' | relative_url }}">
      {% include cube-glyph.html face="y,y,y,y,y,y,y,y,y" %}
      <span class="card__title">Specification</span>
      <p class="card__desc">The formal, implementation-independent rules <code>core/</code> is built and verified against.</p>
      <span class="card__arrow">Read &rarr;</span>
    </a>
    <a class="card" href="{{ '/web-app.html' | relative_url }}">
      {% include cube-glyph.html face="o,r,g,b,w,y,r,o,g" %}
      <span class="card__title">Web App</span>
      <p class="card__desc">An interactive 3D cube in the browser &mdash; Flask + Three.js, consuming the public API.</p>
      <span class="card__arrow">Read &rarr;</span>
    </a>
  </div>
</section>

<section class="section wrap prose" markdown="1">

## Why this exists

Most Rubik's Cube libraries bake their model into whatever they're used
for: a solver ties piece representation to its search algorithm, a
visualizer ties it to its rendering pipeline. CubeForge inverts that.
The engine is a pure mathematical model &mdash; colors, pieces, positions,
orientation, moves, algorithms, whole-cube transformations &mdash; with
**zero dependency** on any UI, network, or storage technology.

| Subproject | What it is |
|---|---|
| [`core/`]({{ site.github_repo }}/tree/main/core) | The engine itself: an immutable Python library with zero external dependencies. |
| [`web/`](web-app.html) | A Flask REST API + Three.js browser UI, consuming `core/` through its public API. |
| [`specs/`](specification.html) | The formal specification `core/` is built to. The source of truth. |
| [`examples/`]({{ site.github_repo }}/tree/main/examples) | Small standalone scripts: inspect a cube, render one to the terminal, play an interactive CLI game. |

</section>
