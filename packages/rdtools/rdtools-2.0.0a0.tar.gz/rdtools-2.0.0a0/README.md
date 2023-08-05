# About RdTools

Master branch: [![Build Status](https://travis-ci.org/NREL/rdtools.svg?branch=master)](https://travis-ci.org/NREL/rdtools)  
Development branch: [![Build Status](https://travis-ci.org/NREL/rdtools.svg?branch=development)](https://travis-ci.org/NREL/rdtools)

RdTools is a set of Python tools for analysis of photovoltaic data.
In particular, PV production data is evaluated over several years
to obtain rates of performance degradation and soiling loss. RdTools can
handle both high frequency (hourly or better) or low frequency (daily, weekly, etc.)
datasets. Best results are obtained with higher frequency data.

Full examples are worked out in the example notebooks in [rdtools/docs](./docs/degradation_example.ipynb).

## Workflow
RdTools supports a number of workflows, but a typical analysis follows the following: 

0. Import and preliminary calculations
1. Normalize data using a performance metric
2. Filter data that creates bias
3. Aggregate data
4. Analyze aggregated data to estimate the degradation rate and/or soiling loss  

Steps 1 and 2 may be accomplished with the clearsky workflow ([see example](./docs/degradation_example.ipynb))
which can help elliminate problems from irradiance sensor drift.  

<img src="./screenshots/RdTools_workflows.png" width="400" height="247" alt="RdTools Workflow"/>

## Degradation Results

The preferred method for degradation rate estimation is the year-on-year (YOY) approach,
available in `degradation.degradation_year_on_year`. The YOY calculation yields in a distribution
of degradation rates, the central tendency of which is the most representative of the true
degradation. The width of the distribution provides information about the uncertainty in the
estimate via a bootstrap calculation. The [example notebook](./docs/degradation_example.ipynb) uses the output of `degradation.degradation_year_on_year()`
to visualize the calculation.

<img src="./screenshots/Clearsky_result_updated.png" width="600" height="456" alt="RdTools Result"/>


Two workflows are available for system performance ratio calculation, and illustrated in an example notebook. 
The sensor-based approach assumes that site irradiance and temperature sensors are calibrated and in good repair.
Since this is not always the case, a 'clear-sky' workflow is provided that is based on
modeled temperature and irradiance.  Note that site irradiance data is still required to identify
clear-sky conditions to be analyzed.  In many cases, the 'clear-sky' analysis can identify conditions
of instrument errors or irradiance sensor drift, such as in the above analysis.


## Soiling Results
Soiling can be estimated with the stochastic rate and recovery (SRR) method (Deceglie 2018). This method works well when soiling patterns follow a "sawtooth" pattern, a linear decline followed by a sharp recovery associated with natural or mannual cleaning. `rdtools.soiling_srr()` performs the calculation and returns the P50 insolation-weighted soiling ratio, confidence interval, and additional information (`soiling_info`) which includes a summary of the soiling intervals identified, `soiling_info['soiling_interval_summary']`. This summary table can, for example, be used to plot a histogram of the identified soiling rates for the dataset.  

<img src="./screenshots/soiling_histogram.png" width="320" height="216" alt="RdTools Result"/>

## Install RdTools using pip

RdTools can be installed automatically into Python from PyPI using the command line:  
`pip install rdtools`

Alternatively it can be installed manually using the command line:  

1. Download a [release](https://github.com/NREL/rdtools/releases) (Or to work with a development version, clone or download the rdtools repository).
2. Navigate to the repository: `cd rdtools`
3. Install via pip: `pip install .`

On some systems installation with `pip` can fail due to problems installing requirements. If this occurs, the requirements specified in `setup.py` may need to be separately installed (for example by using `conda`) before installing `rdtools`.

RdTools currently runs in both Python 2.7 and 3.6.

## Usage and examples


Full workflow examples are found in the notebooks in [rdtools/docs](./docs/degradation_example.ipynb). The examples are designed to work with python 3.6. For a consistent experience, we recommend installing the packages and versions documented in `docs/notebook_requirements.txt`. This can be achieved in your environment by first installing RdTools as described above, then running `pip install -r docs/notebook_requirements.txt` from the base directory.

The following functions are used for degradation analysis:

```
import rdtools
```

The most frequently used functions are:

```Python
normalization.normalize_with_pvwatts(energy, pvwatts_kws)
  '''
  Inputs: Pandas time series of raw energy, PVwatts dict for system analysis 
    (poa_global, P_ref, T_cell, G_ref, T_ref, gamma_pdc)
  Outputs: Pandas time series of normalized energy and POA insolation
  '''
```

```Python
filtering.poa_filter(poa); filtering.tcell_filter(Tcell); filtering.clip_filter(power); 
filtering.csi_filter(insolation, clearsky_insolation)
  '''
  Inputs: Pandas time series of raw data to be filtered.
  Output: Boolean mask where `True` indicates acceptable data
  '''
```

```Python
aggregation.aggregation_insol(normalized, insolation, frequency='D')
  '''
  Inputs: Normalized energy and insolation
  Output: Aggregated data, weighted by the insolation.
  '''
```

```Python
degradation.degradataion_year_on_year(aggregated)
  '''
  Inputs: Aggregated, normalized, filtered time series data
  Outputs: Tuple: `yoy_rd`: Degradation rate 
    `yoy_ci`: Confidence interval `yoy_info`: associated analysis data
  '''
```

```Python
soiling.soiling_srr(aggregated, aggregated_insolation)
  '''
  Inputs: Daily aggregated, normalized, filtered time series data for normalized performance and insolation
  Outputs: Tuple: `sr`: Insolation-weighted soiling ratio 
    `sr_ci`: Confidence interval `soiling_info`: associated analysis data
  '''
```

## Citing RdTools

The underlying workflow of RdTools has been published in several places.  If you use RdTools in a published work, please cite the following as appropriate:

  - D. Jordan, C. Deline, S. Kurtz, G. Kimball, M. Anderson, "Robust PV Degradation Methodology and Application",
  IEEE Journal of Photovoltaics, 8(2) pp. 525-531, 2018  
  - M. G. Deceglie, L. Micheli and M. Muller, "Quantifying Soiling Loss Directly From PV Yield," in IEEE Journal of Photovoltaics, 8(2), pp. 547-551, 2018  
  - RdTools, version x.x.x, https://github.com/NREL/rdtools, [DOI:10.5281/zenodo.1210316](https://doi.org/10.5281/zenodo.1210316)  
  *(be sure to include the version number used in your analysis)*


  
## References
The clear sky temperature calculation, `clearsky_temperature.get_clearsky_tamb()`, uses data
from images created by Jesse Allen, NASA’s Earth Observatory using data courtesy of the MODIS Land Group.  
https://neo.sci.gsfc.nasa.gov/view.php?datasetId=MOD_LSTD_CLIM_M  
https://neo.sci.gsfc.nasa.gov/view.php?datasetId=MOD_LSTN_CLIM_M

Other useful references which may also be consulted for degradation rate methodology include:

  - D. C. Jordan, M. G. Deceglie, S. R. Kurtz, “PV degradation methodology comparison — A basis for a standard”, in 43rd IEEE Photovoltaic Specialists Conference, Portland, OR, USA, 2016, DOI: 10.1109/PVSC.2016.7749593.
  - Jordan DC, Kurtz SR, VanSant KT, Newmiller J, Compendium of Photovoltaic Degradation Rates, Progress in Photovoltaics: Research and Application, 2016, 24(7), 978 - 989.
  - D. Jordan, S. Kurtz, PV Degradation Rates – an Analytical Review, Progress in Photovoltaics: Research and Application, 2013, 21(1), 12 - 29.
  - E. Hasselbrink, M. Anderson, Z. Defreitas, M. Mikofski, Y.-C.Shen, S. Caldwell, A. Terao, D. Kavulak, Z. Campeau, D. DeGraaff, “Validation of the PVLife model using 3 million module-years of live site data”, 39th IEEE Photovoltaic Specialists Conference, Tampa, FL, USA, 2013, p. 7 – 13, DOI: 10.1109/PVSC.2013.6744087.

## Further Instructions and Updates

Check out the [wiki](https://github.com/NREL/rdtools/wiki) for additional usage documentation, and for information on development goals and framework.

