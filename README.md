# HRI-Quantifiers

## Installation

- Python 3.10
- Mace4: [Prover9 (and Mace4) Download](https://www.cs.unm.edu/~mccune/prover9/download/)
    - Add the `bin` directory to PATH:
        - Open the `~/.bashrc` file, add the following line at the end of it: `export PATH="[...]:$PATH"`, where `[..]`
          should be replaced with the absolute path of the `bin` folder (
          e.g., `export PATH="/home/user/LADR-2009-11A/bin:$PATH"`)
        - Save the file and load the new `$PATH` executing `source ~/.bashrc`
- NLTK: [Installing NLTK](https://www.nltk.org/install.html)
- inflect: `pip install inflect`
- word2number: `pip install word2number`

## Execution

In the root folder of the repository, run `python main.py`. The command will read the contents
of [queries.in](input/queries.in) and [commands.in](input/commands.in) and write the output
to [queries.out](output/queries.out) and [commands.out](output/commands.out).

### Queries

For each line in [queries.in](input/queries.in) that contains a query in natural language, a JSON object is generated
in [queries.out](output/queries.out). The object has the following
structure: `{"expression": string, "evaluation": boolean/number}`

#### Example

- `queries.in`: `There are less tools than boxes`
- `queries.out`: `{"expression": "|exists x0 (tool(x0)).| < |exists x0 (box(x0)).|", "evaluation": true}`

### Commands

_To be implemented_

## Examples

- `There are twice as many boxes than tools` &rarr; `|exists x0 (box(x0)).| == 2 * |exists x0 (tool(x0)).|`
- `Most objects are boxes` &rarr; `|exists x0 (object(x0) & box(x0)).| > |exists x0 (object(x0) & -box(x0)).|`
- `There are exactly 2 boxes` &rarr; `|exists x0 (box(x0)).| == 2`
