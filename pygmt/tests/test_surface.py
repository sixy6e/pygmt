"""
Tests for surface
"""
import os

import xarray as xr
import pytest

from .. import surface
from .. import which
from ..datasets import load_sample_bathymetry
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_GRID = os.path.join(TEST_DATA_DIR, "tmp_grid.nc")


def test_surface_input_file():
    """
    Run surface by passing in a filename
    """
    fname = which("@tut_ship.xyz", download="c")
    output = surface(data=fname, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_data_array():
    """
    Run surface by passing in a numpy array into data
    """
    ship_data = load_sample_bathymetry()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    output = surface(data=data, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_xyz():
    """
    Run surface by passing in x, y, z numpy.ndarrays individually
    """
    ship_data = load_sample_bathymetry()
    output = surface(
        x=ship_data.longitude,
        y=ship_data.latitude,
        z=ship_data.bathymetry,
        spacing="5m",
        region=[245, 255, 20, 30],
    )
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_xy_no_z():
    """
    Run surface by passing in x and y, but no z
    """
    ship_data = load_sample_bathymetry()
    with pytest.raises(GMTInvalidInput):
        surface(
            x=ship_data.longitude,
            y=ship_data.latitude,
            spacing="5m",
            region=[245, 255, 20, 30],
        )


def test_surface_wrong_kind_of_input():
    """
    Run surface using grid input that is not file/matrix/vectors
    """
    ship_data = load_sample_bathymetry()
    data = ship_data.bathymetry.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, spacing="5m", region=[245, 255, 20, 30])


def test_surface_with_outfile_param():
    """
    Run surface with the -Goutputfile.nc parameter
    """
    ship_data = load_sample_bathymetry()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = surface(
            data=data, spacing="5m", region=[245, 255, 20, 30], outfile=TEMP_GRID
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_GRID)  # check that outfile exists at path
        grid = xr.open_dataset(TEMP_GRID)
        assert isinstance(grid, xr.Dataset)  # check that netcdf grid loaded properly
    finally:
        os.remove(path=TEMP_GRID)
    return output


def test_surface_short_aliases():
    """
    Run surface using short aliases -I for spacing, -R for region, -G for outfile
    """
    ship_data = load_sample_bathymetry()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = surface(data=data, I="5m", R=[245, 255, 20, 30], G=TEMP_GRID)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_GRID)  # check that outfile exists at path
        grid = xr.open_dataset(TEMP_GRID)
        assert isinstance(grid, xr.Dataset)  # check that netcdf grid loaded properly
    finally:
        os.remove(path=TEMP_GRID)
    return output
