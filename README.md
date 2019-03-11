# Alpha Waves Dataset
Repository with basic scripts for using the Alpha Waves Dataset developed at GIPSA-lab [1]. The dataset files and their documentation are all available at 

[https://zenodo.org/record/2348892](https://zenodo.org/record/2348892#.XBdqNs9Ki3I)

The code of this repository was developed in **Python 3** using MNE-Python [2, 3] as tool for the EEG processing.

To make things work, you might need to install some packages. They are all listed in the `requirements.txt` file and can be easily installed by doing

```
pip install -r requirements.txt
```

in your command line. 

Then, to ensure that your code finds the right scripts whenever you do `import alphawaves`, you should also do

```
python setup.py develop # because no stable release yet
```

Note that you might want to create a *virtual environment* before doing all these installations.

# References

[1] Cattan et al. "EEG Alpha Waves dataset" [DOI](https://10.5281/zenodo.2348891)

[2] Gramfort et al. "MNE software for processing MEG and EEG data" [DOI](https://doi.org/10.1016/j.neuroimage.2013.10.027)

[3] Gramfort et al. "MEG and EEG data analysis with MNE-Python" [DOI](https://doi.org/10.3389/fnins.2013.00267)

