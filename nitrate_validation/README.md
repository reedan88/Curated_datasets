# A 5-year validated Nitrate Dataset from the Pioneer-NES array
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14908032.svg)](https://doi.org/10.5281/zenodo.14908032) <br>
@author: Andrew Reed <br>
@email: areed@whoi.edu


---
## Overview
### Scope
The [Ocean Observatories Initiative (OOI)](https://oceanobservatories.org/) deployed both the In-Situ Ultraviolet Spectrophotometer (ISUS) and Submersible Underwater Nitrate Sensor (SUNA) for continuous, in-situ measurement of nitrate. At the Pioneer-New England Shelf Array (Pioneer-NES), ISUS/SUNA sensors were deployed at 7-meters depth at the Inshore (ISSM), Central (CNSM), and Offshore (OSSM) Surface Mooring locations. The SUNA sensor replaced the ISUS sensors spring 2018. The SUNA was a major improvement in technology, with significant improvements in accuracy and precision. However, it still suffers from calibration drift due to lamp fatigue and biofouling as well as spectral interference due to bromide and fluorometric CDOM. Drift is corrected by application of post-cruise calibrations to recalculate the temperature-and-salinity corrected nitrate concentration following Sakamoto (2009a) and estimating a linear drift between pre-and-post cruise deployments. Validation is performed by comparison with discrete water samples collected during deployment/recovery of the sensors. Quality control is performed following vendor documentation, operator-added annotations, and OOI-supplied QARTOD tests.

### Purpose
The purpose of this repository is to document the methods used to create a validated, science-ready dataset of SUNA-measured nitrate from the Pioneer-NES array. This involves quality control, drift correction, and validation using discrete water samples, of the nitrate time series from the three Pioneer-NES SUNA nitrate sensors.

---
## Dependencies
This notebook relies on using the open-source OOI-maintained gitHub repository [ooi-data-explorations](https://github.com/oceanobservatories/ooi-data-explorations). Installation requires cloning or downloading the repo and installing it as a local developer repo. Detailed instructions are available at the repo.

## Files
* ```utils.py```: contains supporting functions that are used throughout the processing notebook
* ```SUNA_analysis_final.ipynb```: A step-by-step jupyter notebook for accessing, processing, and creating the drift-and-bottle-corrected nitrate timeseries from the OOI SUNA instruments deployed at the Pioneer-NES array

--
## References
Johnson, K. and Coletti, L.J. 2002. In situ ultraviolet spectrophotometry for high resolution and long-term monitoring of nitrate, bromide and bisulfide in the ocean. Deep-Sea Research I, 49, 1291–130 [https://doi.org/10.1016/S0967-0637(02)00020-1 ](https://doi.org/10.1016/S0967-0637(02)00020-1)

Palevsky, H.I., Clayton, S., et al. 2023. OOI Biogeochemical Sensor Data: Best Practices & User Guide, Version 1.1.1. Ocean Observatories Initiative Biogeochemical Sensor Data Working Group, 134pp. DOI: [https://doi.org/10.25607/OBP-1865.2 ](https://doi.org/10.25607/OBP-1865.2 )

Sakamoto, C.M., Johnson, K.S., and L.J. Coletti. 2009. Improved algorithm for the computation of nitrate concentrations in seawater using an in situ ultraviolet spectrophotometer. Limnology and Oceanography: Methods 7.1 (2009): 132-143. [https://doi.org/10.3390%2Fs21030965 ](https://doi.org/10.3390%2Fs21030965)
