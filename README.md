# Debian-based Docker image analysis
This repository represents a replication package for our analysis on Debian-based Docker images.

This replication package requires Python 3.5+ to be installed, and all the dependencies listed in ``requirements.txt``.
They can be automatically installed using ``pip install -r requirements.txt``. 
These experiments were executed on a Linux Ubuntu OS.

To obtain the analysis used in the paper, one should execute ``jupyter notebook`` at the root of this replication package, and open the notebook contained in ``notebooks``.

This replication package contains three folders (i.e scripts, notebooks and data).
- script: contains all scripts needed to pull images, inspect DockerHub API, extract Debian bugs, etc.
- data.zip: should be unzipped. The folder data inside contains all datasets needed for the analysis and prepared before. To download this dataset, please use this zenodo repository: https://doi.org/10.5281/zenodo.3568160
- notebooks: contains notebooks where we prepare and analyze data. If you are more specifically interested in the empirical analysis you can find it in the folder ``3 - Analysis of Debian-based Docker images``. All data is already provided in data.zip

The data is under the Creative Commons Attribution Share-Alike 4.0 license.
The source code is under the GNU General Public License.
