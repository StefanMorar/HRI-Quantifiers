# Mace4 

The folder contains the compiled Mace4 programs and should be added to PATH. 

## Alternative installation steps

- Mace4 and Prover9: [Prover9 (and Mace4) Download](https://www.cs.unm.edu/~mccune/prover9/download/)
    - Download [LADR-2009-11A.tar.gz](https://www.cs.unm.edu/~mccune/prover9/download/LADR-2009-11A.tar.gz)
    - Extract the archive: `zcat LADR-2009-11A.tar.gz | tar xvf -`
    - Open the `LADR-2009-11A/provers.src/Makefile` file and make the adjustments according to [this Stack Overflow issue answer](https://stackoverflow.com/a/70395714). The option `-lm` is out of position; move it at the end of the line at each occurrence (7 times)
    - Run `make all` in the `LADR-2009-11A` folder. Verify the installation by running `make test1`. For additional details, read the instructions in the `LADR-2009-11A/README.make` file
