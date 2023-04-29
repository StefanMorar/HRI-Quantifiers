# HRI-Quantifiers

## Installation

- Operating system: Linux. Windows users can use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install). 
- Python 3.10
- Mace4 and Prover9: [Prover9 (and Mace4) Download](https://www.cs.unm.edu/~mccune/prover9/download/)
    - Download [LADR-2009-11A.tar.gz](https://www.cs.unm.edu/~mccune/prover9/download/LADR-2009-11A.tar.gz)
    - Extract the archive: `zcat LADR-2009-11A.tar.gz | tar xvf -`
    - Open the `LADR-2009-11A/provers.src/Makefile` file and make the adjustments according to [this Stack Overflow issue answer](https://stackoverflow.com/a/70395714). The option `-lm` is out of position; move it at the end of the line at each occurrence (7 times)
    - Run `make all` in the `LADR-2009-11A` folder. Verify the installation by running `make test1`. For additional details, read the instructions in the `LADR-2009-11A/README.make` file
    - Add the `bin` directory to PATH:
        - Open the `~/.bashrc` file, add the following line at the end of it: `export PATH="[...]:$PATH"`, where `[..]`
          should be replaced with the absolute path of the `bin` folder (
          e.g., `export PATH="/home/user/LADR-2009-11A/bin:$PATH"`)
        - Save the file and load the new `$PATH` executing `source ~/.bashrc`
- NLTK: [Installing NLTK](https://www.nltk.org/install.html)
   - `pip install --user -U nltk`
   - run `python3`, then type
     ```pycon
     import nltk
     nltk.download('punkt')
     nltk.download('averaged_perceptron_tagger')
     ```
- inflect: `pip install inflect`
- word2number: `pip install word2number`

## Execution

In the root folder of the repository, run `python3 main.py`. The command will read the contents
of [queries.in](input/queries.in) and [commands.in](input/commands.in) and write the output
to [queries.out](output/queries.out) and [commands.out](output/commands.out).

Alternatively, each component can be executed independently:

- `python3 mace4/run-mace4.py`: will evaluate the expression from [expression.in](mace4/expression.in)
  against [background-knowledge.in](mace4/background-knowledge.in) and [sensors.in](mace4/sensors.in) and write the
  models to `result.out`
- `python3 src/evaluator.py`: will evaluate the expressions from the `main()` function. Update the contents of this
  function to test different expressions
- `python3 src/converter.py`: will convert the sentences from the `main()` function to FOL with cardinality. Update the
  contents of this function to test certain conversions

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
