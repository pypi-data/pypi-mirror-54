# topa

topa - Top Output Python Analyzer

A command line app to analyze linux top command output.

It will shows you below information for each pid you specified:

- Total record count 
- Max Cpu
- Min Cpu
- Average Cpu
- Max Mem
- Min Mem
- Average Mem

## Install

```bash
pip install topa
```

## Usage

```bash
topa -h(--help)
```

```
Usage: topa [OPTIONS] FILENAME

  TOPA - Top Output Python Analyzer

  A python cli application to analyze standard linux top output

Options:
  -p, --pid INTEGER       The pid list to be analyzed  [required]
  -o, --out [STD|MD|PDF]  The analyze report file format  [default: STD]
  -h, --help              Show this message and exit.

```

> `MD` and `PDF` are not supported yet. 
