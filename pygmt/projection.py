#!/usr/bin/env python

"""
Contains the projections supported by GMT, and the necessary mechanisms
to create a projection and output a valid GMT projection string.

>>> from pygmt import projection
>>> proj = projection.LambertAzimuthalEqualArea(central_longitude=30, central_latitude=-20, horizon=60, width=8, unit="i")
>>> proj
LambertAzimuthalEqualArea(central_longitude=30, central_latitude=-20, horizon=60, width=8, unit='i')
>>> print(proj)
A30/-20/60/8i
"""

from enum import Enum
import attr


UNDEFINED = ""


class Supported(Enum):

    """
    The supported projections and their GMT code.
    """

    UNDEFINED = ""
    LAMBERT_AZIMUTH_EQUAL_AREA = "A"  # DONE
    ALBERS_CONIC_EQUAL_AREA = "B"  # DONE
    CASSINI_CYLINDRICAL = "C"  # DONE
    CYLINDRICAL_STEROGRAPHIC = "JCyl_stere/"  # includes `/` according to https://docs.generic-mapping-tools.org/latest/proj_codes.html  # DONE
    EQUIDISTANT_CONIC = "JD"  # DONE
    AZIMUTHAL_EQUIDISTANT = "E"  # DONE
    AZIMUTHAL_GNOMIC = "F"  # DONE
    AZIMUTHAL_ORTHOGRAPHIC = "G"  # DONE
    GENERAL_PERSPECTIVE = "G"  # DONE
    HAMMER_EQUAL_AREA = "H"  # DONE
    SINUSOIDAL_EQUAL_AREA = "I"  # DONE
    MILLER_CYLINDRICAL = "J"  # DONE
    ECKERT_IV_EQUAL_AREA = "Kf"  # DONE
    ECKERT_VI_EQUAL_AREA = "Ks"  # DONE
    LAMBERT_CONIC_CONFORMAL = "L"  # DONE
    MERCATOR_CYLINDRICAL = "M"  # DONE
    ROBINSON = "N"  # DONE
    OBLIQUE_MERCATOR_1 = "Oa"  # DONE
    OBLIQUE_MERCATOR_2 = "Ob"  # DONE
    OBLIQUE_MERCATOR_3 = "Oc"  # DONE
    POLAR = "P"
    POLYCONIC = "Poly"  # DONE
    EQUIDISTANT_CYLINDRICAL = "Q"
    WINKEL_TRIPEL = "R"  # DONE
    GENERAL_STEREOGRAPHIC = "S"  # DONE
    TRANSVERSE_MERCATOR = "T"  # DONE
    UNIVERSAL_TRANSVERSE_MERCATOR = "U"  # DONE
    VAN_DER_GRINTEN = "V"  # DONE
    MOLLWEIDE = "W"  # DONE
    LINEAR = "X"
    CYLINDRICAL_EQUAL_AREA = "Y"  # DONE


@attr.s()
class _Projection:

    """
    Base class for all projections.
    """

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False, default="{_code}")
    _code: str = attr.ib(init=False, repr=False, default=UNDEFINED)

    def __str__(self):
        exclude = attr.fields(self.__class__)._fmt
        kwargs = attr.asdict(self, filter=attr.filters.exclude(exclude))
        return self._fmt.format(**kwargs)


@attr.s(kw_only=True)
class _Azimuthal(_Projection):

    """
    Base class for azimuthal projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    horizon: float = attr.ib(default=90)
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{horizon}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default=UNDEFINED)

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value > 180:
            raise ValueError("horizon must be less than or equal to 180")


@attr.s(kw_only=True)
class _Cylindrical(_Projection):

    """
    Base class for cylindrical projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{wdith}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default=UNDEFINED)


@attr.s(kw_only=True)
class _Conic(_Projection):

    """
    Base class for conic projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    lat1: float = attr.ib()
    lat2: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{lat1}/{lat2}/{width}{unit}",
    )


@attr.s(kw_only=True)
class _Miscellaneous(_Projection):

    """
    Base class for miscellaneous projections.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_meridian: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_meridian}/{width}{unit}",
    )


@attr.s(frozen=True)
class LambertAzimuthalEqualArea(_Azimuthal):

    """
    Class definition for the Lambert azimuthal equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="A")


@attr.s(frozen=True)
class AzimuthalEquidistant(_Azimuthal):

    """
    Class definition for the azimuthal equidistant projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 180.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    horizon: float = attr.ib(default=180, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="E")


@attr.s(frozen=True)
class AzimuthalGnomic(_Azimuthal):

    """
    Class definition for the azimuthal gnomic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 60.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    horizon: float = attr.ib(default=60, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="F")

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value >= 90:
            raise ValueError("horizon must be less than 90")


@attr.s(frozen=True)
class AzimuthalOrthographic(_Azimuthal):

    """
    Class definition for the azimuthal orthographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    horizon: float = attr.ib(default=90)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="G")

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value > 90:
            raise ValueError("horizon must be less than or equal to 90")


@attr.s(frozen=True, kw_only=True)
class GeneralPerspective(_Projection):

    """
    Class definition for the azimuthal general perspective projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre (in degrees).
    central_latitude : float
        The latitude of the projection centre (in degrees).
    altitude : float
        The height in km of the viewpoint above local sea level.
    azimuth : float
        The direction (in degrees) in which you are looking is specified, measured clockwise from north.
    tilt : float
        The viewing angle relative to zenith (in degrees).
    twist : float
        The clockwise rotation of the image (in degrees).
    viewport_width : float
        The width of the viewing angle (in degrees).
    viewport_height : float
        The height of the viewing angle (in degrees).
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    altitude: float = attr.ib()
    azimuth: float = attr.ib()
    tilt: float = attr.ib()
    twist: float = attr.ib()
    Width: float = attr.ib()
    Height: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{altitude}/{azimuth}/{tilt}/{twist}/{viewport_width}/{viewport_height}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="G")


@attr.s(frozen=True)
class GeneralSterographic(_Azimuthal):

    """
    Class definition for the azimuthal general sterographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    horizon: float = attr.ib(default=90, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="S")

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value >= 180:
            raise ValueError("horizon must be less than 180")


@attr.s(frozen=True, kw_only=True)
class AlbersConicEqualArea(_Conic):

    """
    Class definition for the Albers conic equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="B")


@attr.s(frozen=True, kw_only=True)
class EquidistantConic(_Conic):

    """
    Class definition for the equidistant conic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="JD")


@attr.s(frozen=True)
class CassiniCylindrical(_Cylindrical):

    """
    Class definition for the Cassini cylindrical projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="C")


@attr.s(frozen=True)
class MercatorCylindrical(_Cylindrical):

    """
    Class definition for the Mercator cylindrical projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre. Default is 180.
    central_latitude : float
        The latitude of the projection centre. Default is 0.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib(default=180, kw_only=True)
    central_latitude: float = attr.ib(default=0, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="M")


@attr.s(frozen=True)
class CylindricalStereographic(_Cylindrical):

    """
    Class definition for the cylindrical stereographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre. Default is 180.
    central_latitude : float
        The latitude of the projection centre. Default is 0.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib(default=180, kw_only=True)
    central_latitude: float = attr.ib(default=0, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="JCyl_stere/")


@attr.s(frozen=True)
class CylindricalEqualArea(_Cylindrical):

    """
    Class definition for the cylindrical equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="Y")


@attr.s(frozen=True)
class HammerEqualArea(_Miscellaneous):

    """
    Class definition for the Hammer equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="H")


@attr.s(frozen=True)
class SinusoidalEqualArea(_Miscellaneous):

    """
    Class definition for the sinusoidal equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="I")


@attr.s(frozen=True)
class EckertIVEqualArea(_Miscellaneous):

    """
    Class definition for the Eckert IV equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="Kf")


@attr.s(frozen=True)
class EckertVIEqualArea(_Miscellaneous):

    """
    Class definition for the Eckert VI equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="Ks")


@attr.s(frozen=True)
class Robinson(_Miscellaneous):

    """
    Class definition for the Robinson projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="N")


@attr.s(frozen=True)
class WinkelTripel(_Miscellaneous):

    """
    Class definition for the Winkel tripel projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="R")


@attr.s(frozen=True)
class Mollweide(_Miscellaneous):

    """
    Class definition for the Mollweide projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="W")


@attr.s(frozen=True)
class VanDerGrinten(_Miscellaneous):

    """
    Class definition for the Van der Grinten projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="V")


@attr.s(frozen=True)
class LambertConicConformal(_Conic):

    """
    Class definition for the Lambert conic conformal projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="L")


@attr.s(frozen=True, kw_only=True)
class Polyconic(_Projection):

    """
    Class definition for the (American) polyconic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="Poly")


@attr.s(frozen=True)
class Miller(_Miscellaneous):

    """
    Class definition for the Miller cylindrical projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="J")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator1(_Projection):

    """
    Class definition for the oblique Mercator 1 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    azimuth : float
        Azimuth of the oblique equator.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{azimuth}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="Oa")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator2(_Projection):

    """
    Class definition for the oblique Mercator 2 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    oblique_longitude : float
        The longitude of the second point on an oblique equator.
    oblique_latitude : float
        The latitude of the second point on an oblique equator.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    oblique_longitude: float = attr.ib()
    oblique_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{oblique_longitude}/{oblique_latitude}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="Ob")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator3(_Projection):

    """
    Class definition for the oblique Mercator 3 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    pole_longitude : float
        The longitude of the projection pole.
    pole_latitude : float
        The latitude of the projection pole.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    pole_longitude: float = attr.ib()
    pole_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{pole_longitude}/{pole_latitude}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="Oc")


@attr.s(frozen=True)
class TransverseMercator(_Cylindrical):

    """
    Class definition for the Transverse Mercator projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False, default="T")


@attr.s(frozen=True, kw_only=True)
class UniversalTransverseMercator(_Projection):

    """
    Class definition for the Universal Transverse Mercator projection.

    Parameters
    ----------
    zone : str
        The UTM zone {A, B, Y, Z, 1-60}. Use negative values for numerical
        zones in the southern hemisphere, or append the latitude modifiers
        {C-N, P-X} to specify and exact UTM grid zone.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``i``.
    """
    zone: str = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="i")

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{zone}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="U")
