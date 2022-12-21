# 🌱🍅 Multi-organs Plant Model 🍅🌱
**Python project to do simulations on a genome-scale plant  model with 3 organs (LEAF-STEM-ROOT) using FBA (CobraPy).**


### 💡 Functionalities

- Generates **organ-specific models** from a generic plant model and FlexFlux contraints files,
- Runs **sequencial FBA simulations**, where:
    - The leaf tries to *maximize its biomass rate*, while exporting sucrose to sink organs,
    - Then, root and stem trie to *minimize their sucrose uptake*, while having to attain a fixed biomass rate (expressed as a fraction of the leaf's one)
- Stops the feedback loop and export **output (plots, flux tables)** when biomass rates converge.


### 📚 How to use
- Install the required dependencies:
    - **Python 3.8(.10)** (higher versions should work, but not tested yet),
    - **CobraPy** (`pip install cobra`),
    - **PyYAML** (`pip install pyyaml`),
    - **Matplotlib** for output plotting (`pip install matplotlib`).
- Inside the `input` directory, add input files (sbml, FlexFlux constraints) and edit `config.yaml` according to your needs.
- Run `main.py`.
- Results are written in the `output` directory.


### 🏗️ To-do List

- Logging,
- Docstrings,
- Better packaging, for use in another python project,
- Rewrite in OOP when possible (FlexfluxConstraints, OrganModel extends cobra.Model, ...),
- Optimize (may be hard considering the bottleneck that are the FBA themselves).