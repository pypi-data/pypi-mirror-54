import autoarray as aa
from autoarray.plotters import plotter_util


def image(
    light_profile,
    grid,
    mask=None,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Image",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="image",
):
    """Plot the image of a light profile, on a grid of (y,x) coordinates.

    Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    light_profile : model.profiles.light_profiles.LightProfile
        The light profile whose image are plotted.
    grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
    """
    profile_image = light_profile.profile_image_from_grid(grid=grid)

    aa.plot.array(
        array=profile_image,
        mask_overlay=mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def luminosity_within_circle_in_electrons_per_second_as_function_of_radius(
    light_profile,
    minimum_radius=1.0e-4,
    maximum_radius=10.0,
    radii_bins=10,
    as_subplot=False,
    label="Light Profile",
    plot_axis_type="semilogy",
    effective_radius_line=None,
    einstein_radius_line=None,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    plot_legend=True,
    title="Luminosity (Electrons Per Second) vs Radius",
    ylabel="Luminosity (Electrons Per Second)",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    legend_fontsize=12,
    output_path=None,
    output_format="show",
    output_filename="luminosity_vs_radius",
):

    radii = plotter_util.quantity_radii_from_minimum_and_maximum_radii_and_radii_points(
        minimum_radius=minimum_radius,
        maximum_radius=maximum_radius,
        radii_points=radii_bins,
    )

    luminosities = list(
        map(
            lambda radius: light_profile.luminosity_within_circle_in_units(
                radius=radius
            ),
            radii,
        )
    )

    aa.plot.quantity_as_function_of_radius(
        quantity=luminosities,
        radii=radii,
        as_subplot=as_subplot,
        label=label,
        plot_axis_type=plot_axis_type,
        effective_radius_line=effective_radius_line,
        einstein_radius_line=einstein_radius_line,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        plot_legend=plot_legend,
        title=title,
        ylabel=ylabel,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        legend_fontsize=legend_fontsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def convergence(
    mass_profile,
    grid,
    mask=None,
    positions=None,
    plot_critical_curves=False,
    plot_caustics=False,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Convergence",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="convergence",
):
    """Plot the convergence of a mass profile, on a grid of (y,x) coordinates.

    Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    mass_profile : model.profiles.mass_profiles.MassProfile
        The mass profile whose convergence is plotted.
    grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
    """

    convergence = mass_profile.convergence_from_grid(grid=grid)

    lines = plotter_util.get_critical_curve_and_caustic(
        obj=mass_profile,
        grid=grid,
        plot_critical_curve=plot_critical_curves,
        plot_caustics=plot_caustics,
    )

    aa.plot.array(
        array=convergence,
        mask_overlay=mask,
        positions=positions,
        lines=lines,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def potential(
    mass_profile,
    grid,
    mask=None,
    positions=None,
    as_subplot=False,
    plot_critical_curves=False,
    plot_caustics=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Potential",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="potential",
):
    """Plot the potential of a mass profile, on a grid of (y,x) coordinates.

    Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    mass_profile : model.profiles.mass_profiles.MassProfile
        The mass profile whose potential is plotted.
    grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
    """
    potential = mass_profile.potential_from_grid(grid=grid)

    lines = plotter_util.get_critical_curve_and_caustic(
        obj=mass_profile,
        grid=grid,
        plot_critical_curve=plot_critical_curves,
        plot_caustics=plot_caustics,
    )

    aa.plot.array(
        array=potential,
        mask_overlay=mask,
        positions=positions,
        lines=lines,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def deflections_y(
    mass_profile,
    grid,
    mask=None,
    positions=None,
    plot_critical_curves=False,
    plot_caustics=False,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Deflections (y)",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="deflections_y",
):
    """Plot the y component of the deflection angles of a mass profile, on a grid of (y,x) coordinates.

    Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    mass_profile : model.profiles.mass_profiles.MassProfile
        The mass profile whose y deflecton angles are plotted.
    grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
    """

    deflections = mass_profile.deflections_from_grid(grid=grid)
    deflections_y = grid.mask.mapping.array_from_sub_array_1d(sub_array_1d=deflections[:, 0])

    lines = plotter_util.get_critical_curve_and_caustic(
        obj=mass_profile,
        grid=grid,
        plot_critical_curve=plot_critical_curves,
        plot_caustics=plot_caustics,
    )

    aa.plot.array(
        array=deflections_y,
        mask_overlay=mask,
        positions=positions,
        lines=lines,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def deflections_x(
    mass_profile,
    grid,
    mask=None,
    positions=None,
    plot_critical_curves=False,
    plot_caustics=False,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Deflections (x)",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="deflections_x",
):
    """Plot the x component of the deflection angles of a mass profile, on a grid of (y,x) coordinates.

     Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

     Parameters
     -----------
     mass_profile : model.profiles.mass_profiles.MassProfile
         The mass profile whose x deflecton angles are plotted.
     grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
         The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
     """
    deflections = mass_profile.deflections_from_grid(grid=grid)
    deflections_x = grid.mask.mapping.array_from_sub_array_1d(sub_array_1d=deflections[:, 1])

    lines = plotter_util.get_critical_curve_and_caustic(
        obj=mass_profile,
        grid=grid,
        plot_critical_curve=plot_critical_curves,
        plot_caustics=plot_caustics,
    )

    aa.plot.array(
        array=deflections_x,
        mask_overlay=mask,
        positions=positions,
        lines=lines,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def magnification(
    mass_profile,
    grid,
    mask=None,
    positions=None,
    as_subplot=False,
    plot_critical_curves=False,
    plot_caustics=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Magnification",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10.0,
    grid_pointsize=1,
    output_path=None,
    output_format="show",
    output_filename="magnification",
):
    """Plot the magnification of a mass profile, on a grid of (y,x) coordinates.

    Set *autoastro.hyper_galaxies.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    mass_profile : model.profiles.mass_profiles.MassProfile
        The mass profile whose magnification is plotted.
    grid : ndarray or hyper_galaxies.array.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2)
    """
    magnification = mass_profile.magnification_from_grid(grid=grid)

    lines = plotter_util.get_critical_curve_and_caustic(
        obj=mass_profile,
        grid=grid,
        plot_critical_curve=plot_critical_curves,
        plot_caustics=plot_caustics,
    )

    aa.plot.array(
        array=magnification,
        mask_overlay=mask,
        positions=positions,
        lines=lines,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        grid_pointsize=grid_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )
