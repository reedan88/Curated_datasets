import numpy as np
from scipy.stats import median_abs_deviation
import datetime
import pandas as pd
import xarray as xr


def ntp_seconds_to_datetime(ntp_seconds):
    """Convert OOINet timestamps to unix-convertable timestamps."""
    # Specify some constant needed for timestamp conversions
    ntp_epoch = datetime.datetime(1900, 1, 1)
    unix_epoch = datetime.datetime(1970, 1, 1)
    ntp_delta = (unix_epoch - ntp_epoch).total_seconds()

    return datetime.datetime.utcfromtimestamp(ntp_seconds - ntp_delta)


def convert_time(ms):
    """Calculate UTC timestamp from OOI milliseconds"""
    if ms is None:
        return None
    else:
        return datetime.datetime.utcfromtimestamp(ms/1000)


def unix_epoch_time(date_time):
    """Convert a datetime to unix epoch microseconds."""
    # Convert the date time to a string
    date_time = int(pd.to_datetime(date_time).strftime("%s"))*1000
    return date_time


def mad(array):
    """Calculate the median absolute standard deviation"""
    return median_abs_deviation(array, axis=0, nan_policy='omit')


def burst_resample(ds):
    """Resample the data to a defined time interval using a median average"""
    # Load the dataset to speed up calculation
    burst = ds
    burst.load()
    
    # First, grab the corrected nitrate concentrations and return the median absolute deviation
    # resampled to every 15 minutes
    cnc = burst["corrected_nitrate_concentration"]
    cnc = cnc.resample(time='900s', base=3150, loffset='450s', skipna=True)
    cnc = xr.apply_ufunc(mad,
               cnc,
               input_core_dims=[['time']])
    # Next, we'll do the normal resample across the other datasets
    burst = burst.resample(time='900s', base=3150, loffset='450s', skipna=True).median(keep_attrs=True)
    # Add in the median absolute deviation calculation
    burst['corrected_nitrate_concentration_mad'] = (['time'], cnc.data)
    burst['corrected_nitrate_concentration_mad'].attrs = {
        'comment': 'The median absolute standard deviation.'}
    burst = burst.where(~np.isnan(burst.deployment), drop=True)
    # save the newly averaged data
    ds = burst

    # and reset some data types
    data_types = ['deployment', 'spectrum_average', 'serial_number', 'dark_value_used_for_fit',
                  'raw_spectral_measurements']
    for v in data_types:
        ds[v] = ds[v].astype('int32')

    return ds


def quality_checks(ds, param):
    """
    Quality assessment of the raw and calculated nitrate concentration data
    using a susbset of the QARTOD flags to indicate the quality. QARTOD
    flags used are:

        1 = Pass
        3 = Suspect or of High Interest
        4 = Fail

    The final flag value represents the worst case assessment of the data quality.

    :param ds: xarray dataset with the raw signal data and the calculated
               seawater pH
    :param param: the name of the nitrate variable to check the range of
    :return qc_flag: array of flag values indicating seawater pH quality
    """
    qc_flag = ds['time'].astype('int32') * 0 + 1   # default flag values, no errors

    # "RMSE: The root-mean-square error parameter from the SUNA V2 can be used to make
    # an estimate of how well the nitrate spectral fit is. This should usually be less than 1E-3. If
    # it is higher, there is spectral shape (likely due to CDOM) that adversely impacts the nitrate
    # estimate." SUNA V2 vendor documentation (Sea-Bird Scientific Document# SUNA180725)
    m = ds.fit_rmse > 0.001  # per the vendor documentation
    qc_flag[m] = 3
    m = ds.fit_rmse > 0.100  # based on experience with the instrument data sets
    qc_flag[m] = 4

    # "Absorption: The data output of the SUNA V2 is the absorption at 350 nm and 254 nm
    # (A350 and A254). These wavelengths are outside the nitrate absorption range and can be
    # used to make an estimate of the impact of CDOM. If absorption is high (>1.3 AU), the
    # SUNA will not be able to collect adequate light to make a measurement." SUNA V2 vendor
    # documentation (Sea-Bird Scientific Document# SUNA180725)
    m254 = ds.absorbance_at_254_nm > 1.3
    qc_flag[m254] = 4
    m350 = ds.absorbance_at_350_nm > 1.3
    qc_flag[m350] = 4

    # test for failed dark value measurements (can't be less than 0)
    m = ds.dark_value_used_for_fit <= 0
    qc_flag[m] = 4

    # test for a blocked absorption channel (or a failed lamp)
    m = ds.spectrum_average < 10000
    qc_flag[m] = 4

    # test for out of range corrected dissolved nitrate readings
    m = (ds[param].values < -2.0) | (ds[param].values > 3000)
    qc_flag[m] = 4

    return qc_flag
	
	

	
