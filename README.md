# HRI-Quantifiers

## Installation

- Operating system: Linux
- Python 3.10
- Mace4 and Prover9: [Prover9 (and Mace4) Download](https://www.cs.unm.edu/~mccune/prover9/download/)
    - Download [LADR-2009-11A.tar.gz](https://www.cs.unm.edu/~mccune/prover9/download/LADR-2009-11A.tar.gz)
    - Extract the archive: `zcat LADR-2009-11A.tar.gz | tar xvf -`
    - Open the `LADR-2009-11A/provers.src/Makefile` file and make the adjustments according to [this Stack Overflow issue answer](https://stackoverflow.com/a/70395714). The option `-lm` is out of position; move it at the end of the line at each occurrence (7 times)
    - Run `make all` in the `LADR-2009-11A` folder. Verify the installation by running `make test1`. For additional details, read the instructions in the `LADR-2009-11A/README.make` file
    - Add the `bin` directory to PATH:
        - Open the `~/.bashrc` file (e.g., by running `nano ~/.bashrc`), add the following line at the end of it: `export PATH="[...]:$PATH"`, where `[..]`
          should be replaced with the absolute path of the `bin` folder (
          e.g., `export PATH="/home/user/LADR-2009-11A/bin:$PATH"`)
        - Save the file and load the new `$PATH` executing `source ~/.bashrc`
- requests: `pip install requests`
- python-dotenv: `pip install python-dotenv`
- OpenAI: `pip install --upgrade openai`

## Execution

In the root folder of the repository, run `python3 src/main.py`.

Alternatively, each component can be executed independently:

- `python3 mace4/run_mace4.py`: will evaluate the expression from [expression.in](mace4/expression.in)
  against [background_knowledge.in](mace4/background_knowledge.in) and [sensors.in](mace4/sensors.in) and write the
  models to `result.out`
- `python3 src/evaluator.py`: will evaluate the expressions from the `main()` function. Update the contents of this
  function to test different expressions
- `python3 src/converter.py`: will convert the sentences from the `main()` function to expressions that can be used to query the state or send commands to the robot using the [abe_sim](https://github.com/mpomarlan/abe_sim/tree/3p0) agent simulation in PyBullet. 


## Examples

### Queries

| Sentence                                    | Conversion                                                                                                                          |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| There are twice as many onions than carrots | `{'type':'query','expressions':['\|exists x0 (onion(x0)).\| == 2 * \|exists x0 (carrot(x0)).\|']}`                                  |
| There are twice as many onions than carrots | `{'type':'query','expressions':['\|exists x0 (vegetable(x0) & redOnion(x0)).\| > \|exists x0 (vegetable(x0) & -redOnion(x0)).\|']}` |
| There are exactly 2 ovens                   | `{'type':'query','expressions':['\|exists x0 (oven(x0)).\| == 2']}`                                                                 |

### Commands

| Sentence                             | Conversion                                                                                                                                                                                           |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fetch a couple of red chilli peppers | `{'type':'command','expressions':[['\|exists x1 (redChilliPepper(x1)).\| >= 2']],'commands':['abe(x0) & redChilliPepper(x1) -> fetch(x0, x1).']}`                                                    |
| Cut several broccoli                 | `{'type':'command','expressions':[['\|exists x1 (broccoli(x1)).\| >= 3']],'commands':['abe(x0) & broccoli(x1) & cuttingTool(x2) -> cut(x0, x1, x2).']}`                                              |
| Line a baking tray with paper        | `{'type':'command','expressions':[['\|exists x1 (bakingSheet(x1)).\| >= 1','\|exists x2 (bakingTray(x2)).\| >= 1']],'commands':['abe(x0) & bakingSheet(x1) & bakingTray(x2) -> line(x0, x1, x2).']}` |

For more examples, check [train_data.csv](notebooks/data/train_data.csv).
