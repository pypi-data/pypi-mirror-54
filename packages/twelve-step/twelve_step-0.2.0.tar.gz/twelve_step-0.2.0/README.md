# Twelve-Step

---

A python tool to analyse dependencies of python projects.

## Installation

This package requires python3.7 or more.

```bash
pip3.7 install twelve-step --user
```

## Example usages

By default twelve step generates a DOT graph and prints it in console.

### To generate a dot file

```bash
twelve-step a_project_path > dependency-graph.dot
```

or

```bash
twelve-step a_project_path -o dependency-graph
```

### To generate a graph .svg in one command

```bash
twelve-step a_project_path | dot -Tsvg -o dependency-graph.svg
```
