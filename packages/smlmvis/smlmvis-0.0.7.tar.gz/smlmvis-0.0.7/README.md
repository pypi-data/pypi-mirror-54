# Superresolution visualization of 3D protein localization data from a range of microscopes
See demo.ipynb for example usage.

## Requirements
### Python
* vtk
* numpy
* jupyter
* pandas
* seaborn
* requests

See requirements.yml for Conda, piprequirements.txt for pip
### Optional
* [Paraview](https://www.paraview.org/)

## Gif of install
![](smlmvis.gif)

## Supported microscopes:
* Leica GSD, Abbelight, EPFL Challenge dataset, Rainstorm, Tafteh et al,
For the full list please see demo.ipynb 

## Install
### PIP
```bash
$pip install smlmvis
```
### Conda
```bash
$conda conda install -c bcardoen smlmvis 
```

### Local from git master
```bash
$git clone git@github.com:bencardoen/smlmvis.git
$pip install .
```

## Usage
See demo.ipynb for example usage.

A typical workflow is
* use one of the readers (e.g. GSDReader in smlmvis.gsreader) to load in the SMLM data
* write out the data to vtk/paraview format using e.g. VtuWriter in vtuwriter


## Cite
```latex
@misc{Cardoen2019,
  author = {Cardoen, Ben},
  title = {Superresolution visualization of 3D protein localization data from a range of microscopes},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bencardoen/smlmvis/}}
}
```
## Tests
See tests/test_writer.py

This will download the challenge data set, read it, decode it, write it to VTK and compare with a reference.

## Acknowledgements
VTU writing code uses the VTK examples heavily to figure out how to interface with VTK.
* [VTK Python API](https://lorensen.github.io/VTKExamples/site/Python/)
