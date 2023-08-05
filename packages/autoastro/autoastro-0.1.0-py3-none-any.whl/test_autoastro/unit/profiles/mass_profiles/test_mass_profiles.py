import autoarray as aa
import autoastro as am
import math
from skimage import measure
import numpy as np
import pytest

from test_autoastro.mock import mock_cosmology


@pytest.fixture(autouse=True)
def reset_config():
    """
    Use configuration from the default path. You may want to change this to set a specific path.
    """
    aa.conf.instance = aa.conf.default


class TestEinsteinRadiusMass(object):
    def test__radius_of_critical_curve_and_einstein_radius__radius_unit_conversions(
        self
    ):

        cosmology = mock_cosmology.MockCosmology(kpc_per_arcsec=2.0)

        sis_arcsec = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            einstein_radius=am.dim.Length(2.0, "arcsec"),
        )

        radius = sis_arcsec.average_convergence_of_1_radius_in_units(
            unit_length="arcsec", cosmology=cosmology
        )
        assert radius == pytest.approx(2.0, 1e-4)

        radius = sis_arcsec.einstein_radius_in_units(unit_length="arcsec")
        assert radius == pytest.approx(2.0, 1e-4)

        radius = sis_arcsec.einstein_radius_in_units(
            unit_length="kpc", redshift_profile=0.5, cosmology=cosmology
        )
        assert radius == pytest.approx(4.0, 1e-4)

        sis_kpc = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            einstein_radius=am.dim.Length(2.0, "kpc"),
        )

        radius = sis_kpc.average_convergence_of_1_radius_in_units(unit_length="kpc")
        assert radius == pytest.approx(2.0, 1e-4)

        radius = sis_kpc.einstein_radius_in_units(unit_length="kpc")
        assert radius == pytest.approx(2.0, 1e-4)

        radius = sis_kpc.einstein_radius_in_units(
            unit_length="arcsec", redshift_profile=0.5, cosmology=cosmology
        )
        assert radius == pytest.approx(1.0, 1e-4)

        nfw_arcsec = am.mp.SphericalNFW(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            kappa_s=0.5,
            scale_radius=am.dim.Length(5.0, "arcsec"),
        )

        radius = nfw_arcsec.average_convergence_of_1_radius_in_units(
            unit_length="arcsec"
        )
        assert radius == pytest.approx(2.76386, 1e-4)

        radius = nfw_arcsec.einstein_radius_in_units(
            unit_length="arcsec", cosmology=cosmology
        )
        assert radius == pytest.approx(2.76386, 1e-4)

        radius = nfw_arcsec.einstein_radius_in_units(
            unit_length="kpc", redshift_profile=0.5, cosmology=cosmology
        )
        assert radius == pytest.approx(2.0 * 2.76386, 1e-4)

        nfw_kpc = am.mp.SphericalNFW(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            kappa_s=0.5,
            scale_radius=am.dim.Length(5.0, "kpc"),
        )

        radius = nfw_kpc.average_convergence_of_1_radius_in_units(
            unit_length="kpc", redshift_profile=0.5, cosmology=cosmology
        )
        assert radius == pytest.approx(2.76386, 1e-4)

        radius = nfw_kpc.einstein_radius_in_units(unit_length="kpc")
        assert radius == pytest.approx(2.76386, 1e-4)

        radius = nfw_kpc.einstein_radius_in_units(
            unit_length="arcsec", redshift_profile=0.5, cosmology=cosmology
        )
        assert radius == pytest.approx(0.5 * 2.76386, 1e-4)

    def test__einstein_mass__radius_unit_conversions(self):

        cosmology = mock_cosmology.MockCosmology(
            kpc_per_arcsec=2.0, critical_surface_density=2.0
        )

        sis_arcsec = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            einstein_radius=am.dim.Length(1.0, "arcsec"),
        )

        mass = sis_arcsec.einstein_mass_in_units(
            unit_mass="angular", cosmology=cosmology
        )
        assert mass == pytest.approx(np.pi, 1e-4)

        mass = sis_arcsec.einstein_mass_in_units(
            unit_mass="solMass",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )
        assert mass == pytest.approx(2.0 * np.pi, 1e-4)

        sis_kpc = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            einstein_radius=am.dim.Length(2.0, "kpc"),
        )

        mass = sis_kpc.einstein_mass_in_units(
            unit_mass="angular", redshift_profile=0.5, cosmology=cosmology
        )
        assert mass == pytest.approx(4.0 * np.pi, 1e-4)

        mass = sis_kpc.einstein_mass_in_units(
            unit_mass="solMass",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )
        assert mass == pytest.approx(2.0 * np.pi, 1e-4)

        nfw_arcsec = am.mp.SphericalNFW(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            kappa_s=0.5,
            scale_radius=am.dim.Length(5.0, "arcsec"),
        )

        mass = nfw_arcsec.einstein_mass_in_units(
            unit_mass="angular", cosmology=cosmology
        )
        assert mass == pytest.approx(np.pi * 2.76386 ** 2.0, 1e-4)

        mass = nfw_arcsec.einstein_mass_in_units(
            unit_mass="solMass",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )
        assert mass == pytest.approx(2.0 * np.pi * 2.76386 ** 2.0, 1e-4)

        nfw_kpc = am.mp.SphericalNFW(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            kappa_s=0.5,
            scale_radius=am.dim.Length(5.0, "kpc"),
        )

        mass = nfw_kpc.einstein_mass_in_units(
            unit_mass="angular", redshift_profile=0.5, cosmology=cosmology
        )
        assert mass == pytest.approx(np.pi * 2.76386 ** 2.0, 1e-4)

        mass = nfw_kpc.einstein_mass_in_units(
            unit_mass="solMass",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )
        assert mass == pytest.approx(0.5 * np.pi * 2.76386 ** 2.0, 1e-4)


def mass_within_radius_of_profile_from_grid_calculation(radius, profile):

    mass_total = 0.0

    xs = np.linspace(-radius * 1.5, radius * 1.5, 40)
    ys = np.linspace(-radius * 1.5, radius * 1.5, 40)

    edge = xs[1] - xs[0]
    area = edge ** 2

    for x in xs:
        for y in ys:

            eta = profile.grid_to_elliptical_radii(np.array([[x, y]]))

            if eta < radius:
                mass_total += profile.convergence_func(eta) * area

    return mass_total


class TestMassWithinCircle(object):
    def test__mass_in_angular_units__singular_isothermal_sphere__compare_to_analytic(
        self
    ):

        sis = am.mp.SphericalIsothermal(einstein_radius=2.0)

        radius = am.dim.Length(2.0, "arcsec")

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert math.pi * sis.einstein_radius * radius == pytest.approx(mass, 1e-3)

        sis = am.mp.SphericalIsothermal(einstein_radius=4.0)

        radius = am.dim.Length(4.0, "arcsec")

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert math.pi * sis.einstein_radius * radius == pytest.approx(mass, 1e-3)

    def test__mass_in_angular_units__singular_isothermal__compare_to_grid(self):

        sis = am.mp.SphericalIsothermal(einstein_radius=2.0)

        radius = am.dim.Length(1.0, "arcsec")

        mass_grid = mass_within_radius_of_profile_from_grid_calculation(
            radius=radius, profile=sis
        )

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )

        assert mass_grid == pytest.approx(mass, 0.02)

    def test__radius_units_conversions__mass_profile_updates_units_and_computes_correct_mass(
        self
    ):

        cosmology = mock_cosmology.MockCosmology(kpc_per_arcsec=2.0)

        # arcsec -> arcsec

        sis_arcsec = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            einstein_radius=am.dim.Length(2.0, "arcsec"),
        )

        radius = am.dim.Length(2.0, "arcsec")
        mass = sis_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert math.pi * sis_arcsec.einstein_radius * radius == pytest.approx(
            mass, 1e-3
        )

        # arcsec -> kpc

        radius = am.dim.Length(2.0, "kpc")
        mass = sis_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert math.pi * sis_arcsec.einstein_radius * 1.0 == pytest.approx(mass, 1e-3)

        # 2.0 arcsec = 4.0 kpc, same masses.

        radius = am.dim.Length(2.0, "arcsec")
        mass_arcsec = sis_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        radius = am.dim.Length(4.0, "kpc")
        mass_kpc = sis_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert mass_arcsec == mass_kpc

        # kpc -> kpc

        sis_kpc = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            einstein_radius=am.dim.Length(2.0, "kpc"),
        )

        radius = am.dim.Length(2.0, "kpc")
        mass = sis_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert math.pi * sis_kpc.einstein_radius * radius == pytest.approx(mass, 1e-3)

        # kpc -> arcsec

        radius = am.dim.Length(2.0, "arcsec")
        mass = sis_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert 2.0 * math.pi * sis_kpc.einstein_radius * radius == pytest.approx(
            mass, 1e-3
        )

        # 2.0 arcsec = 4.0 kpc, same masses.

        radius = am.dim.Length(2.0, "arcsec")
        mass_arcsec = sis_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        radius = am.dim.Length(4.0, "kpc")
        mass_kpc = sis_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_arcsec == mass_kpc

    def test__mass_units_conversions__multiplies_by_critical_surface_density_factor(
        self
    ):

        cosmology = mock_cosmology.MockCosmology(critical_surface_density=2.0)

        sis = am.mp.SphericalIsothermal(einstein_radius=2.0)
        radius = am.dim.Length(2.0, "arcsec")

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert math.pi * sis.einstein_radius * radius == pytest.approx(mass, 1e-3)

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="solMass",
            cosmology=cosmology,
        )
        assert 2.0 * math.pi * sis.einstein_radius * radius == pytest.approx(mass, 1e-3)

        mass = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="solMass",
            cosmology=cosmology,
        )
        assert 2.0 * math.pi * sis.einstein_radius * radius == pytest.approx(mass, 1e-3)


class TestMassWithinEllipse(object):
    def test__mass_in_angular_units__singular_isothermal_sphere__compare_circle_and_ellipse(
        self
    ):

        sis = am.mp.SphericalIsothermal(einstein_radius=2.0)

        radius = am.dim.Length(2.0)
        mass_circle = sis.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        mass_ellipse = sis.mass_within_ellipse_in_units(
            major_axis=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_circle == mass_ellipse

        sie = am.mp.EllipticalIsothermal(
            einstein_radius=2.0, axis_ratio=0.5, phi=0.0
        )
        radius = am.dim.Length(2.0)
        mass_circle = sie.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        mass_ellipse = sie.mass_within_ellipse_in_units(
            major_axis=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_circle == mass_ellipse * 2.0

    def test__mass_in_angular_units__singular_isothermal_ellipsoid__compare_to_grid(
        self
    ):

        sie = am.mp.EllipticalIsothermal(
            einstein_radius=2.0, axis_ratio=0.5, phi=0.0
        )

        radius = am.dim.Length(0.5)

        mass_grid = mass_within_radius_of_profile_from_grid_calculation(
            radius=radius, profile=sie
        )

        mass = sie.mass_within_ellipse_in_units(
            major_axis=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )

        # Large errors required due to cusp at center of SIE - can get to errors of 0.01 for a 400 x 400 grid.
        assert mass_grid == pytest.approx(mass, 0.1)

    def test__radius_units_conversions__mass_profile_updates_units_and_computes_correct_mass(
        self
    ):

        cosmology = mock_cosmology.MockCosmology(kpc_per_arcsec=2.0)

        # arcsec -> arcsec

        sie_arcsec = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "arcsec"), am.dim.Length(0.0, "arcsec")),
            einstein_radius=am.dim.Length(2.0, "arcsec"),
        )

        major_axis = am.dim.Length(0.5, "arcsec")

        mass_grid = mass_within_radius_of_profile_from_grid_calculation(
            radius=major_axis, profile=sie_arcsec
        )

        mass = sie_arcsec.mass_within_ellipse_in_units(
            major_axis=major_axis,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_grid == pytest.approx(mass, 0.1)

        # arcsec -> kpc

        major_axis = am.dim.Length(0.5, "kpc")
        mass = sie_arcsec.mass_within_ellipse_in_units(
            major_axis=major_axis,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert 0.5 * mass_grid == pytest.approx(mass, 0.1)

        # 2.0 arcsec = 4.0 kpc, same masses.

        radius = am.dim.Length(2.0, "arcsec")
        mass_arcsec = sie_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        radius = am.dim.Length(4.0, "kpc")
        mass_kpc = sie_arcsec.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert mass_arcsec == mass_kpc

        # kpc -> kpc

        sie_kpc = am.mp.SphericalIsothermal(
            centre=(am.dim.Length(0.0, "kpc"), am.dim.Length(0.0, "kpc")),
            einstein_radius=am.dim.Length(2.0, "kpc"),
        )

        major_axis = am.dim.Length(0.5, "kpc")
        mass = sie_kpc.mass_within_ellipse_in_units(
            major_axis=major_axis,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_grid == pytest.approx(mass, 0.1)

        # kpc -> arcsec

        major_axis = am.dim.Length(0.5, "arcsec")
        mass = sie_kpc.mass_within_ellipse_in_units(
            major_axis=major_axis,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert 2.0 * mass_grid == pytest.approx(mass, 0.1)

        # 2.0 arcsec = 4.0 kpc, same masses.

        radius = am.dim.Length(2.0, "arcsec")
        mass_arcsec = sie_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )
        radius = am.dim.Length(4.0, "kpc")
        mass_kpc = sie_kpc.mass_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )
        assert mass_arcsec == mass_kpc

    def test__mass_unit_conversions__compare_to_grid__mutliplies_by_critical_surface_density(
        self
    ):

        cosmology = mock_cosmology.MockCosmology(critical_surface_density=2.0)

        sie = am.mp.EllipticalIsothermal(
            einstein_radius=2.0, axis_ratio=0.5, phi=0.0
        )

        radius = am.dim.Length(2.0, "arcsec")

        mass_grid = mass_within_radius_of_profile_from_grid_calculation(
            radius=radius, profile=sie
        )
        mass = sie.mass_within_ellipse_in_units(
            major_axis=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
            cosmology=cosmology,
        )

        # Large errors required due to cusp at center of SIE - can get to errors of 0.01 for a 400 x 400 grid.
        assert mass_grid == pytest.approx(radius * sie.axis_ratio * mass, 0.1)

        critical_surface_density = am.dim.MassOverLength2(2.0, "arcsec", "solMass")
        mass = sie.mass_within_ellipse_in_units(
            major_axis=radius,
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="solMass",
            cosmology=cosmology,
        )

        # Large errors required due to cusp at center of SIE - can get to errors of 0.01 for a 400 x 400 grid.
        assert mass_grid == pytest.approx(0.5 * radius * sie.axis_ratio * mass, 0.1)


class TestDensityBetweenAnnuli(object):
    def test__circular_annuli__sis__analyic_density_agrees(self):

        cosmology = mock_cosmology.MockCosmology(
            kpc_per_arcsec=2.0, critical_surface_density=2.0
        )

        einstein_radius = 1.0
        sis_arcsec = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=einstein_radius
        )

        inner_annuli_radius = am.dim.Length(2.0, "arcsec")
        outer_annuli_radius = am.dim.Length(3.0, "arcsec")

        inner_mass = math.pi * einstein_radius * inner_annuli_radius
        outer_mass = math.pi * einstein_radius * outer_annuli_radius

        density_between_annuli = sis_arcsec.density_between_circular_annuli_in_angular_units(
            inner_annuli_radius=inner_annuli_radius,
            outer_annuli_radius=outer_annuli_radius,
            unit_length="arcsec",
            unit_mass="angular",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )

        annuli_area = (np.pi * outer_annuli_radius ** 2.0) - (
            np.pi * inner_annuli_radius ** 2.0
        )

        assert (outer_mass - inner_mass) / annuli_area == pytest.approx(
            density_between_annuli, 1e-4
        )

        density_between_annuli = sis_arcsec.density_between_circular_annuli_in_angular_units(
            inner_annuli_radius=inner_annuli_radius,
            outer_annuli_radius=outer_annuli_radius,
            unit_length="arcsec",
            unit_mass="solMass",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )

        annuli_area = (np.pi * outer_annuli_radius ** 2.0) - (
            np.pi * inner_annuli_radius ** 2.0
        )

        assert (2.0 * outer_mass - 2.0 * inner_mass) / annuli_area == pytest.approx(
            density_between_annuli, 1e-4
        )

        density_between_annuli = sis_arcsec.density_between_circular_annuli_in_angular_units(
            inner_annuli_radius=inner_annuli_radius,
            outer_annuli_radius=outer_annuli_radius,
            unit_length="kpc",
            unit_mass="angular",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )

        inner_mass = math.pi * 2.0 * einstein_radius * inner_annuli_radius
        outer_mass = math.pi * 2.0 * einstein_radius * outer_annuli_radius

        annuli_area = (np.pi * 2.0 * outer_annuli_radius ** 2.0) - (
            np.pi * 2.0 * inner_annuli_radius ** 2.0
        )

        assert (outer_mass - inner_mass) / annuli_area == pytest.approx(
            density_between_annuli, 1e-4
        )

    def test__circular_annuli__nfw_profile__compare_to_manual_mass(self):

        cosmology = mock_cosmology.MockCosmology(
            kpc_per_arcsec=2.0, critical_surface_density=2.0
        )

        nfw = am.mp.EllipticalNFW(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=45.0, kappa_s=1.0
        )

        inner_mass = nfw.mass_within_circle_in_units(
            radius=am.dim.Length(1.0),
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )

        outer_mass = nfw.mass_within_circle_in_units(
            radius=am.dim.Length(2.0),
            redshift_profile=0.5,
            redshift_source=1.0,
            unit_mass="angular",
        )

        density_between_annuli = nfw.density_between_circular_annuli_in_angular_units(
            inner_annuli_radius=am.dim.Length(1.0),
            outer_annuli_radius=am.dim.Length(2.0),
            unit_length="arcsec",
            unit_mass="angular",
            redshift_profile=0.5,
            redshift_source=1.0,
            cosmology=cosmology,
        )

        annuli_area = (np.pi * 2.0 ** 2.0) - (np.pi * 1.0 ** 2.0)

        assert (outer_mass - inner_mass) / annuli_area == pytest.approx(
            density_between_annuli, 1e-4
        )


class TestDeflectionsViaPotential(object):
    def test__compare_sis_deflections_via_potential_and_calculation(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=1
        )

        deflections_via_calculation = sis.deflections_from_grid(grid=grid)

        deflections_via_potential = sis.deflections_via_potential_from_grid(grid=grid)

        mean_error = np.mean(deflections_via_potential.in_1d - deflections_via_calculation.in_1d)

        assert mean_error < 1e-4

    def test__compare_sie_at_phi_45__deflections_via_potential_and_calculation(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=45.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=1
        )

        deflections_via_calculation = sie.deflections_from_grid(grid=grid)

        deflections_via_potential = sie.deflections_via_potential_from_grid(grid=grid)

        mean_error = np.mean(deflections_via_potential.in_1d - deflections_via_calculation.in_1d)

        assert mean_error < 1e-4

    def test__compare_sie_at_phi_0__deflections_via_potential_and_calculation(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=1
        )

        deflections_via_calculation = sie.deflections_from_grid(grid=grid)

        deflections_via_potential = sie.deflections_via_potential_from_grid(grid=grid)

        mean_error = np.mean(deflections_via_potential.in_1d - deflections_via_calculation.in_1d)

        assert mean_error < 1e-4


class TestJacobian(object):
    def test__jacobian_components(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=1
        )

        jacobian = sie.jacobian_from_grid(grid=grid)

        A_12 = jacobian[0][1]
        A_21 = jacobian[1][0]

        mean_error = np.mean(A_12.in_1d - A_21.in_1d)

        assert mean_error < 1e-4

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        jacobian = sie.jacobian_from_grid(grid=grid)

        A_12 = jacobian[0][1]
        A_21 = jacobian[1][0]

        mean_error = np.mean(A_12.in_1d - A_21.in_1d)

        assert mean_error < 1e-4


class TestMagnification(object):

    def test__compare_magnification_from_eigen_values_and_from_determinant(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=1
        )

        magnification_via_determinant = sie.magnification_from_grid(grid=grid)

        tangential_eigen_value = sie.tangential_eigen_value_from_grid(grid=grid)

        radal_eigen_value = sie.radial_eigen_value_from_grid(grid=grid)

        magnification_via_eigen_values = 1 / (
            tangential_eigen_value * radal_eigen_value
        )

        mean_error = np.mean(
            magnification_via_determinant.in_1d - magnification_via_eigen_values.in_1d
        )

        assert mean_error < 1e-4

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        magnification_via_determinant = sie.magnification_from_grid(grid=grid)

        tangential_eigen_value = sie.tangential_eigen_value_from_grid(grid=grid)

        radal_eigen_value = sie.radial_eigen_value_from_grid(grid=grid)

        magnification_via_eigen_values = 1 / (
            tangential_eigen_value * radal_eigen_value
        )

        mean_error = np.mean(
            magnification_via_determinant.in_1d - magnification_via_eigen_values.in_1d
        )

        assert mean_error < 1e-4

    def test__compare_magnification_from_determinant_and_from_convergence_and_shear(
        self
    ):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=1
        )

        magnification_via_determinant = sie.magnification_from_grid(grid=grid)

        convergence = sie.convergence_via_jacobian_from_grid(grid=grid)

        shear = sie.shear_via_jacobian_from_grid(grid=grid)

        magnification_via_convergence_and_shear = 1 / (
            (1 - convergence) ** 2 - shear ** 2
        )

        mean_error = np.mean(
            magnification_via_determinant.in_1d - magnification_via_convergence_and_shear.in_1d
        )

        assert mean_error < 1e-4

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        magnification_via_determinant = sie.magnification_from_grid(grid=grid)

        convergence = sie.convergence_via_jacobian_from_grid(grid=grid)

        shear = sie.shear_via_jacobian_from_grid(grid=grid)

        magnification_via_convergence_and_shear = 1 / (
            (1 - convergence) ** 2 - shear ** 2
        )

        mean_error = np.mean(
            magnification_via_determinant.in_1d - magnification_via_convergence_and_shear.in_1d
        )

        assert mean_error < 1e-4


def critical_curve_via_magnification_from_mass_profile_and_grid(mass_profile, grid):

    magnification = mass_profile.magnification_from_grid(grid=grid)

    inverse_magnification = 1 / magnification

    critical_curves_indices = measure.find_contours(inverse_magnification.in_2d, 0)

    no_critical_curves = len(critical_curves_indices)
    contours = []
    critical_curves = []

    for jj in np.arange(no_critical_curves):

        contours.append(critical_curves_indices[jj])
        contour_x, contour_y = contours[jj].T
        pixel_coord = np.stack((contour_x, contour_y), axis=-1)

        critical_curve = grid.geometry.grid_arcsec_from_grid_pixels_1d_for_marching_squares(
            grid_pixels_1d=pixel_coord, shape_2d=magnification.sub_shape_2d
        )

        critical_curves.append(critical_curve)

    return critical_curves


def caustics_via_magnification_from_mass_profile_and_grid(mass_profile, grid):

    caustics = []

    critical_curves = critical_curve_via_magnification_from_mass_profile_and_grid(
        mass_profile=mass_profile, grid=grid
    )

    for i in range(len(critical_curves)):

        critical_curve = critical_curves[i]

        deflections_1d = mass_profile.deflections_from_grid(grid=critical_curve)

        caustic = critical_curve - deflections_1d

        caustics.append(caustic)

    return caustics


class TestConvergenceViajacobian(object):
    def test__compare_sis_convergence_via_jacobian_and_calculation(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.05, sub_size=1
        )

        convergence_via_calculation = sis.convergence_from_grid(grid=grid)

        convergence_via_jacobian = sis.convergence_via_jacobian_from_grid(grid=grid)

        mean_error = np.mean(
            convergence_via_jacobian.in_1d - convergence_via_calculation.in_1d
        )

        assert convergence_via_jacobian.in_2d_binned.shape == (20, 20)
        assert mean_error < 1e-1

        mean_error = np.mean(
            convergence_via_jacobian.in_1d - convergence_via_calculation.in_1d
        )

        assert mean_error < 1e-1

    def test__compare_sie_at_phi_45__convergence_via_jacobian_and_calculation(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=45.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.05, sub_size=1
        )

        convergence_via_calculation = sie.convergence_from_grid(grid=grid)

        convergence_via_jacobian = sie.convergence_via_jacobian_from_grid(grid=grid)

        mean_error = np.mean(convergence_via_jacobian.in_1d - convergence_via_calculation.in_1d)

        assert mean_error < 1e-1


class TestCriticalCurvesAndCaustics(object):
    def test_compare_magnification_from_determinant_and_from_convergence_and_shear(
        self
    ):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        magnification_via_determinant = sie.magnification_from_grid(grid=grid)

        convergence = sie.convergence_via_jacobian_from_grid(grid=grid)

        shear = sie.shear_via_jacobian_from_grid(grid=grid)

        magnification_via_convergence_and_shear = 1 / (
            (1 - convergence) ** 2 - shear ** 2
        )

        mean_error = np.mean(
            magnification_via_determinant - magnification_via_convergence_and_shear
        )

        assert mean_error < 1e-2

    def test__tangential_critical_curve_radii__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=2
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        tangential_critical_curve = critical_curves[0]

        x_critical_tangential, y_critical_tangential = (
            tangential_critical_curve[:, 1],
            tangential_critical_curve[:, 0],
        )

        assert np.mean(
            x_critical_tangential ** 2 + y_critical_tangential ** 2
        ) == pytest.approx(sis.einstein_radius ** 2, 5e-1)

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.5, sub_size=4
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        tangential_critical_curve = critical_curves[0]

        x_critical_tangential, y_critical_tangential = (
            tangential_critical_curve[:, 1],
            tangential_critical_curve[:, 0],
        )

        assert np.mean(
            x_critical_tangential ** 2 + y_critical_tangential ** 2
        ) == pytest.approx(sis.einstein_radius ** 2, 5e-1)

    def test__tangential_critical_curve_centres__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        tangential_critical_curve = critical_curves[0]

        y_centre = np.mean(tangential_critical_curve[:, 0])
        x_centre = np.mean(tangential_critical_curve[:, 1])

        assert -0.03 < y_centre < 0.03
        assert -0.03 < x_centre < 0.03

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=4
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        tangential_critical_curve = critical_curves[0]

        y_centre = np.mean(tangential_critical_curve[:, 0])
        x_centre = np.mean(tangential_critical_curve[:, 1])

        assert -0.01 < y_centre < 0.01
        assert -0.01 < x_centre < 0.01

        sis = am.mp.SphericalIsothermal(
            centre=(0.5, 1.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(60, 60), pixel_scales=0.25, sub_size=1
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        tangential_critical_curve = critical_curves[0]

        y_centre = np.mean(tangential_critical_curve[:, 0])
        x_centre = np.mean(tangential_critical_curve[:, 1])

        assert 0.47 < y_centre < 0.53
        assert 0.97 < x_centre < 1.03

    def test__radial_critical_curve_centres__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        radial_critical_curve = critical_curves[1]

        y_centre = np.mean(radial_critical_curve[:, 0])
        x_centre = np.mean(radial_critical_curve[:, 1])

        assert -0.05 < y_centre < 0.05
        assert -0.05 < x_centre < 0.05

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=4
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        radial_critical_curve = critical_curves[1]

        y_centre = np.mean(radial_critical_curve[:, 0])
        x_centre = np.mean(radial_critical_curve[:, 1])

        assert -0.01 < y_centre < 0.01
        assert -0.01 < x_centre < 0.01

        sis = am.mp.SphericalIsothermal(
            centre=(0.5, 1.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(60, 60), pixel_scales=0.25, sub_size=1
        )

        critical_curves = sis.critical_curves_from_grid(grid=grid)

        radial_critical_curve = critical_curves[1]

        y_centre = np.mean(radial_critical_curve[:, 0])
        x_centre = np.mean(radial_critical_curve[:, 1])

        assert 0.45 < y_centre < 0.55
        assert 0.95 < x_centre < 1.05

    def test__tangential_caustic_centres__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        caustics = sis.caustics_from_grid(grid=grid)

        tangential_caustic = caustics[0]

        y_centre = np.mean(tangential_caustic[:, 0])
        x_centre = np.mean(tangential_caustic[:, 1])

        assert -0.03 < y_centre < 0.03
        assert -0.03 < x_centre < 0.03

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=4
        )

        caustics = sis.caustics_from_grid(grid=grid)

        tangential_caustic = caustics[0]

        y_centre = np.mean(tangential_caustic[:, 0])
        x_centre = np.mean(tangential_caustic[:, 1])

        assert -0.01 < y_centre < 0.01
        assert -0.01 < x_centre < 0.01

        sis = am.mp.SphericalIsothermal(
            centre=(0.5, 1.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(60, 60), pixel_scales=0.25, sub_size=1
        )

        caustics = sis.caustics_from_grid(grid=grid)

        tangential_caustic = caustics[0]

        y_centre = np.mean(tangential_caustic[:, 0])
        x_centre = np.mean(tangential_caustic[:, 1])

        assert 0.47 < y_centre < 0.53
        assert 0.97 < x_centre < 1.03

    def test__radial_caustics_radii__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.5, sub_size=4
        )

        caustics = sis.caustics_from_grid(grid=grid)

        caustic_radial = caustics[1]

        x_caustic_radial, y_caustic_radial = (
            caustic_radial[:, 1],
            caustic_radial[:, 0],
        )

        assert np.mean(x_caustic_radial ** 2 + y_caustic_radial ** 2) == pytest.approx(
            sis.einstein_radius ** 2, 5e-1
        )

    def test__radial_caustic_centres__spherical_isothermal(self):

        sis = am.mp.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        caustics = sis.caustics_from_grid(grid=grid)

        radial_caustic = caustics[1]

        y_centre = np.mean(radial_caustic[:, 0])
        x_centre = np.mean(radial_caustic[:, 1])

        assert -0.2 < y_centre < 0.2
        assert -0.2 < x_centre < 0.2

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=4
        )

        caustics = sis.caustics_from_grid(grid=grid)

        radial_caustic = caustics[1]

        y_centre = np.mean(radial_caustic[:, 0])
        x_centre = np.mean(radial_caustic[:, 1])

        assert -0.09 < y_centre < 0.09
        assert -0.09 < x_centre < 0.09

        sis = am.mp.SphericalIsothermal(
            centre=(0.5, 1.0), einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(60, 60), pixel_scales=0.25, sub_size=1
        )

        caustics = sis.caustics_from_grid(grid=grid)

        radial_caustic = caustics[1]

        y_centre = np.mean(radial_caustic[:, 0])
        x_centre = np.mean(radial_caustic[:, 1])

        assert 0.3 < y_centre < 0.7
        assert 0.8 < x_centre < 1.2

    def test__compare_tangential_critical_curves_from_magnification_and_eigen_values(
        self
    ):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2, axis_ratio=0.8, phi=40
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        tangential_critical_curve_from_magnification = critical_curve_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            0
        ]

        tangential_critical_curve_from_eigen_values = sie.tangential_critical_curve_from_grid(
            grid=grid
        )

        assert tangential_critical_curve_from_eigen_values == pytest.approx(
            tangential_critical_curve_from_magnification, 5e-1
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.5, sub_size=2
        )

        tangential_critical_curve_from_magnification = critical_curve_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            0
        ]

        tangential_critical_curve_from_eigen_values = sie.tangential_critical_curve_from_grid(
            grid=grid
        )

        assert tangential_critical_curve_from_eigen_values == pytest.approx(
            tangential_critical_curve_from_magnification, 5e-1
        )

    def test__compare_radial_critical_curves_from_magnification_and_eigen_values(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2, axis_ratio=0.8, phi=40
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        critical_curve_radial_from_magnification = critical_curve_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            1
        ]

        critical_curve_radial_from_eigen_values = sie.radial_critical_curve_from_grid(
            grid=grid
        )

        assert sum(critical_curve_radial_from_magnification) == pytest.approx(
            sum(critical_curve_radial_from_eigen_values), 5e-1
        )

    def test__compare_tangential_caustic_from_magnification_and_eigen_values(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2, axis_ratio=0.8, phi=40
        )

        grid = aa.grid.uniform(
            shape_2d=(20, 20), pixel_scales=0.25, sub_size=1
        )

        tangential_caustic_from_magnification = caustics_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            0
        ]

        tangential_caustic_from_eigen_values = sie.tangential_caustic_from_grid(
            grid=grid
        )

        assert sum(tangential_caustic_from_eigen_values) == pytest.approx(
            sum(tangential_caustic_from_magnification), 5e-1
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.5, sub_size=2
        )

        tangential_caustic_from_magnification = caustics_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            0
        ]

        tangential_caustic_from_eigen_values = sie.tangential_caustic_from_grid(
            grid=grid
        )

        assert sum(tangential_caustic_from_eigen_values) == pytest.approx(
            sum(tangential_caustic_from_magnification), 5e-1
        )

    def test__compare_radial_caustic_from_magnification_and_eigen_values__grid(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=2, axis_ratio=0.8, phi=40
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=1
        )

        caustic_radial_from_magnification = caustics_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            1
        ]

        caustic_radial_from_eigen_values = sie.caustics_from_grid(grid=grid)[1]

        assert sum(caustic_radial_from_eigen_values) == pytest.approx(
            sum(caustic_radial_from_magnification), 7e-1
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        caustic_radial_from_magnification = caustics_via_magnification_from_mass_profile_and_grid(
            mass_profile=sie, grid=grid
        )[
            1
        ]

        caustic_radial_from_eigen_values = sie.caustics_from_grid(grid=grid)[1]

        assert sum(caustic_radial_from_eigen_values) == pytest.approx(
            sum(caustic_radial_from_magnification), 5e-1
        )


class TestGridsBinning:
    def deflections_via_potential(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=2
        )

        deflections = sie.deflections_via_potential_from_grid(grid=grid)

        deflections_first_binned_pixel = (
            deflections[0] + deflections[1] + deflections[2] + deflections[3]
        ) / 4

        assert deflections.in_1d_binned[0] == pytest.approx(
            deflections_first_binned_pixel, 1e-4
        )

        deflections_100th_binned_pixel = (
            deflections[399] + deflections[398] + deflections[397] + deflections[396]
        ) / 4

        assert deflections.in_1d_binned[99] == pytest.approx(
            deflections_100th_binned_pixel, 1e-4
        )

    def test__jacobian(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=2
        )

        jacobian = sie.jacobian_from_grid(grid=grid)

        jacobian_1st_pixel_binned_up = (
            jacobian[0][0][0]
            + jacobian[0][0][1]
            + jacobian[0][0][2]
            + jacobian[0][0][3]
        ) / 4

        assert jacobian[0][0].in_2d_binned.shape == (10, 10)
        assert jacobian[0][0].sub_shape_2d == (20, 20)
        assert jacobian[0][0].in_1d_binned[0] == pytest.approx(
            jacobian_1st_pixel_binned_up, 1e-4
        )

        jacobian_last_pixel_binned_up = (
            jacobian[0][0][399]
            + jacobian[0][0][398]
            + jacobian[0][0][397]
            + jacobian[0][0][396]
        ) / 4

        assert jacobian[0][0].in_1d_binned[99] == pytest.approx(
            jacobian_last_pixel_binned_up, 1e-4
        )

    def test__shear_via_jacobian(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=2
        )

        shear_via_jacobian = sie.shear_via_jacobian_from_grid(grid=grid)

        shear_1st_pixel_binned_up = (
            shear_via_jacobian[0]
            + shear_via_jacobian[1]
            + shear_via_jacobian[2]
            + shear_via_jacobian[3]
        ) / 4

        assert shear_via_jacobian.in_1d_binned[0] == pytest.approx(
            shear_1st_pixel_binned_up, 1e-4
        )

        shear_last_pixel_binned_up = (
            shear_via_jacobian[399]
            + shear_via_jacobian[398]
            + shear_via_jacobian[397]
            + shear_via_jacobian[396]
        ) / 4

        assert shear_via_jacobian.in_1d_binned[99] == pytest.approx(
            shear_last_pixel_binned_up, 1e-4
        )

    def test__tangential_eigen_values(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(10, 10), pixel_scales=0.05, sub_size=2
        )

        tangential_eigen_values = sie.tangential_eigen_value_from_grid(grid=grid)

        first_pixel_binned_up = (
            tangential_eigen_values[0]
            + tangential_eigen_values[1]
            + tangential_eigen_values[2]
            + tangential_eigen_values[3]
        ) / 4

        assert tangential_eigen_values.in_1d_binned[0] == pytest.approx(
            first_pixel_binned_up, 1e-4
        )

        pixel_10000_from_av_sub_grid = (
            tangential_eigen_values[399]
            + tangential_eigen_values[398]
            + tangential_eigen_values[397]
            + tangential_eigen_values[396]
        ) / 4

        assert tangential_eigen_values.in_1d_binned[99] == pytest.approx(
            pixel_10000_from_av_sub_grid, 1e-4
        )

    def test__radial_eigen_values(self):

        sie = am.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), phi=0.0, axis_ratio=0.8, einstein_radius=2.0
        )

        grid = aa.grid.uniform(
            shape_2d=(100, 100), pixel_scales=0.05, sub_size=2
        )

        radial_eigen_values = sie.radial_eigen_value_from_grid(grid=grid)

        first_pixel_binned_up = (
            radial_eigen_values[0]
            + radial_eigen_values[1]
            + radial_eigen_values[2]
            + radial_eigen_values[3]
        ) / 4

        assert radial_eigen_values.in_1d_binned[0] == pytest.approx(
            first_pixel_binned_up, 1e-4
        )

        pixel_10000_from_av_sub_grid = (
            radial_eigen_values[399]
            + radial_eigen_values[398]
            + radial_eigen_values[397]
            + radial_eigen_values[396]
        ) / 4

        assert radial_eigen_values.in_1d_binned[99] == pytest.approx(
            pixel_10000_from_av_sub_grid, 1e-4
        )
