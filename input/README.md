# 🔧 Config

Before running this project, you need to specify in `config.yaml`:
- Path to a default **SBML file** (represent whole plant), 
- Paths to **FlexFlux constraints files** for each organ (so 3 in total),
- Experimental values for **biomass rates** (they won't be used as is, but only to specify growth ratios between organ),
- **Dry-weight ratios** between organs (used to adjust the transports in xylem/phloem),
- **List of nutrients** (metabolites) that should be allowed in xylem,
- ID of the **sucrose exchange reaction**.

For the SBML and FlexFlux constraints files, it is advised to put them inside this directory to simplify the path (just write the filename).

There are more optional configuration option available in `config.yaml`, with explanations in the form of comments.
