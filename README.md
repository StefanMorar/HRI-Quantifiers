# HRI-Quantifiers

## Installation

- NLTK: [Installing NLTK](https://www.nltk.org/install.html)
- inflect: `pip install inflect`
- word2number: `pip install word2number`

## Examples

- `There are twice as many boxes than tools` &rarr; `|exists x0 (box(x0)).| == 2 * |exists x0 (tool(x0)).|`
- `Most objects are boxes` &rarr; `|exists x0 (object(x0) & box(x0)).| > |exists x0 (object(x0) & -box(x0)).|`
- `There are exactly 2 boxes` &rarr; `|exists x0 (box(x0)).| == 2`
