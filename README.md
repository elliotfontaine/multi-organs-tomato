# 🌱🍅 Multi-organs Plant Model 🍅🌱
**Python project to do simulations on a genome-scale plant  model with 3 organs (LEAF-STEM-ROOT) using FBA (CobraPy).**


### 💡 Functionalities

- Generates **organ-specific models** from a generic plant model and FlexFlux contraints files,
- Run **sequencial FBA simulations**, where:
    - The leaf tries to *maximize its biomass rate*, while exporting sucrose to sink organs,
    - Root and stem trie to *minimize their sucrose uptake*, while having to attain a fixed biomass rate (expressed as a fraction of the leaf's one)
- Stop the feedback loop and export output (plots, flux tables) when biomass rates converge.


### 📚 How to use

- Inside the `input` directory, add input files (sbml, FlexFlux constraints) and edit `config.yaml` according to your needs.
- Run `main.py` with Python 3.8 or higher, in an environment that has COBRApy installed.
- Results are written in the `output` directory.


### 🏗️ To-do List

- Logging,
- Docstrings,
- Better packaging, for use in another python project,
- Rewrite in OOP when possible (FlexfluxConstraints, OrganModel extends cobra.Model, ...),
- Optimize (may be hard considering the bottleneck that are the FBA themselves).