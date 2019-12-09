# Debian-based Docker images analysis
This repository represents a replication package for our analysis on Debian-based Docker images.

This replication package requires Python 3.5+ to be installed, and all the dependencies listed in ``requirements.txt``.
They can be automatically installed using ``pip install -r requirements.txt``. 
These experiment were executed on a Linux Ubuntu OS.

To obtain the analysis used in the paper, one should execute ``jupyter notebook`` at the root of this replication package, and open the notebook contained in ``notebooks``.

This replication package contains three folders (i.e scripts, notebooks and data).
- script: contains all scripts needed to pull images, inspect DockerHub API, extract Debian bugs, etc.
- data.zip: should be unzipped. The folder data inside contains all datasets needed for the analysis and prepared before. To download this dataset, please use this zenodo repository: https://zenodo.org/record/3568161.
- notebooks: contains notebooks where we prepare data. If you are more concerned about the analysis you can focus on the folder ``3 - Analysis``. All data is already provided in data.zip

The data is under the Creative Commons Attribution Share-Alike 4.0 license.
The source code is under the GNU General Public License.
