[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# Two-Stage Estimation and Variance Modeling for Latency-Constrained Variational Quantum Algorithms

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[Two-Stage Estimation and Variance Modeling for Latency-Constrained Variational Quantum Algorithms](https://doi.org/10.1287/ijoc.2024.0575) by Yunsoo Ha, Sara Shashaani, and Matt Menickelly. 

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2024.0575

https://doi.org/10.1287/ijoc.2024.0575.cd

Below is the BibTex for citing this snapshot of the repository.

```
@misc{Ha2024,
  author =        {Ha, Yunsoo and Shashaani, Sara and Menickelly, Matt},
  publisher =     {INFORMS Journal on Computing},
  title =         {{Two-Stage Estimation and Variance Modeling for Latency-Constrained Variational Quantum Algorithms}},
  year =          {2024},
  doi =           {10.1287/ijoc.2024.0575.cd},
  url =           {https://github.com/INFORMSJoC/2024.0575},
  note =          {Available for download at https://github.com/INFORMSJoC/2024.0575},
}  
```

## Description

This repository aims to demonstrate the effect of variance model informed two stage stochastic trust region methods (VMI-2STRO-DF) in quantum approximate optimization algorithm (QAOA). 

## Building

You need to install the packages listed in requirements.txt.

```
pip install -r requirements.txt
```

## Results

All detailed results are available in [plots](experiments/plots) folder.

## Replicating

To replicate the results presented in the paper, run the code located in the [figures](figures) folder. This will generate the corresponding plots found in the [plots](experiments/plots) folder using the output .pickle files from the [outputs](experiments/outputs) folder. For instance, to generate Figure 12a, execute the script
```
python figures/figure12a.py
```

To replicate these .pickle files, execute the code in the [run](run) folder. For example, to generate the output .pickle files for Figure 12a, execute the script with circuit depth p = 1 and communication costs set to 0.

```
python run/maxcut_run.py
```
