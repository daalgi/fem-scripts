import numpy as np
import math
from datetime import datetime as dt

from rich.table import Table
from rich.console import Console
from rich.pretty import pprint

from concreteproperties.material import Concrete, SteelBar
from concreteproperties.stress_strain_profile import (
    ConcreteLinear,
    RectangularStressBlock,
    ConcreteLinearNoTension,
    SteelElasticPlastic,
)
from sectionproperties.pre.library.concrete_sections import (
    concrete_rectangular_section,
    concrete_tee_section,
)
from concreteproperties.concrete_section import ConcreteSection


time = dt.now()

concrete = Concrete(
    name="30 MPa Concrete",
    density=2.5e-6,
    stress_strain_profile=ConcreteLinear(elastic_modulus=33100),
    ultimate_stress_strain_profile=RectangularStressBlock(
        compressive_strength=30,
        alpha=1,
        gamma=0.8,
        ultimate_strain=0.0025,
    ),
    flexural_tensile_strength=2.896,
    colour="lightgrey",
)

steel = SteelBar(
    name="500 MPa Steel",
    density=7.85e-6,
    stress_strain_profile=SteelElasticPlastic(
        yield_strength=500,
        elastic_modulus=200e3,
        fracture_strain=0.05,
    ),
    colour="grey",
)

geom = concrete_rectangular_section(
    b=500,
    d=1000,
    n_top=5,
    dia_top=25,
    area_top=np.pi / 4 * 25 * 25, # bar area
    n_bot=5,
    dia_bot=25,
    area_bot=np.pi / 4 * 25 * 25,
    cover=50,
    n_circle=4,
    conc_mat=concrete,
    steel_mat=steel,
)
# geom.plot_geometry()

conc_sec = ConcreteSection(geometry=geom)
gross_props = conc_sec.get_gross_properties()

def stress_analysis(n: float, m: float):
    """
    Parameters
    ----------
    n: float
        Axial force (kN).
    m: float
        Bending moment (kNm).
    """
    cracked_res = conc_sec.calculate_cracked_properties()
    cracked_stress_res = conc_sec.calculate_cracked_stress(
        cracked_results=cracked_res,
        n=n * 1e3, 
        m=m * 1e6,
    )
    table = Table(title="Reinforcement Results")
    for idx, reinf_geom in enumerate(cracked_stress_res.lumped_reinforcement_geometries):
        # get the reinforcement results
        centroid = reinf_geom.calculate_centroid()
        stress = cracked_stress_res.lumped_reinforcement_stresses[idx]
        strain = cracked_stress_res.lumped_reinforcement_strains[idx]
        force, d_x, d_y = cracked_stress_res.lumped_reinforcement_forces[idx]

        # calculate the moment each bar creates and store the results
        moment_x = force * d_y
        # forces.append(force)
        # moments_x.append(moment_x)

        # print compression or tension
        if strain > 0:
            t_or_c = "C"
        else:
            t_or_c = "T"

        table.add_row(
            f"{idx + 1}",
            f"({centroid[0]:.1f}, {centroid[1]:.1f})",
            f"{abs(stress):.1f} ({t_or_c})",
            f"{abs(force) / 1e3:.1f}",
            f"{d_y:.1f}",
            f"{moment_x / 1e6:.2f}",
        )

    console = Console()
    console.print(table)
    cracked_stress_res.plot_stress()

# stress_analysis(n=0, m=-750)
# stress_analysis(n=500, m=0)
# stress_analysis(n=-500, m=0)
stress_analysis(n=-100, m=300)
stress_analysis(n=+000, m=300)
stress_analysis(n=+100, m=300)
# stress_analysis(n=+100, m=100)


# # gross_props.print_results(fmt=".3e")

# transformed_props = conc_sec.get_transformed_gross_properties(elastic_modulus=28577)
# # transformed_props.print_results(fmt=".3e")

# cracked_res_sag = conc_sec.calculate_cracked_properties()
# # cracked_res_sag.print_results()
# cracked_res_hog = conc_sec.calculate_cracked_properties(theta=np.pi)
# # cracked_res_hog.print_results()
# cracked_res = cracked_res_sag
# cracking_moment = cracked_res.m_cr
# neutral_axis_depth = cracked_res.d_nc
# cracked_i = cracked_res.iuu_cr
# # print(f"M_cr = {cracking_moment / 1e6:.2f} kN.m")
# # print(f"d_nc = {neutral_axis_depth:.2f} mm")
# # print(f"I_cr = {cracked_i:.3e} mm^4")
# # cr.plot_cracked_geometries()

# # # Computation time
# # time = dt.now() - time
# # print(f'\nComputation time: {time} ms\n')

# n_ext = +100000
# m_ext = 122.9e6
# cracked_stress_res = conc_sec.calculate_cracked_stress(
#     cracked_results=cracked_res, m=m_ext, n=n_ext,
# )
# # cracked_stress_res.plot_stress()

# for idx, an_sec in enumerate(cracked_stress_res.concrete_analysis_sections):
#     # Label section and plot section mesh
#     # print(f"Analysis Section {idx + 1}")
#     # an_sec.plot_mesh()

#     # get concrete results
#     sigs_conc = cracked_stress_res.concrete_stresses[idx]
#     f_conc = cracked_stress_res.concrete_forces[idx][0]
#     d_x_conc = cracked_stress_res.concrete_forces[idx][1]
#     d_y_conc = cracked_stress_res.concrete_forces[idx][2]
#     m_x_conc = f_conc * d_y_conc
#     m_y_conc = f_conc * d_x_conc
#     m_conc = np.sqrt(m_x_conc * m_x_conc + m_y_conc * m_y_conc)

#     # print results
#     print("Concrete Stresses:")
#     pprint(sigs_conc)
#     # print("Concrete Net Force & Lever Arm:")
#     # print(f"F_c = {f_conc / 1e3:.2f} kN")
#     # print(f"d_x_n = {d_x_conc:.2f} mm")
#     # print(f"d_y_n = {d_y_conc:.2f} mm")
#     # print(f"M_x_c = {m_x_conc / 1e6:.2f} kN.m")
#     # print(f"M_y_c = {m_y_conc / 1e6:.2f} kN.m")
#     # print(f"M_c = {m_conc / 1e6:.2f} kN.m")

# # store forces & moments for later
# forces = []
# moments_x = []

# # # create a Rich table for pretty printing
# # table = Table(title="Reinforcement Results")
# # table.add_column("Bar No.", justify="center", style="cyan", no_wrap=True)
# # table.add_column("Location (x, y) (mm)", justify="center", style="green")
# # table.add_column("Stress (MPa)", justify="center", style="green")
# # table.add_column("Force (kN)", justify="center", style="green")
# # table.add_column("Lever Arm (mm)", justify="center", style="green")
# # table.add_column("Moment (kN.m)", justify="center", style="green")

# # for idx, reinf_geom in enumerate(cracked_stress_res.lumped_reinforcement_geometries):
# #     # get the reinforcement results
# #     centroid = reinf_geom.calculate_centroid()
# #     stress = cracked_stress_res.lumped_reinforcement_stresses[idx]
# #     strain = cracked_stress_res.lumped_reinforcement_strains[idx]
# #     force, d_x, d_y = cracked_stress_res.lumped_reinforcement_forces[idx]

# #     # calculate the moment each bar creates and store the results
# #     moment_x = force * d_y
# #     forces.append(force)
# #     moments_x.append(moment_x)

# #     # print compression or tension
# #     if strain > 0:
# #         t_or_c = "C"
# #     else:
# #         t_or_c = "T"

# #     table.add_row(
# #         f"{idx + 1}",
# #         f"({centroid[0]:.1f}, {centroid[1]:.1f})",
# #         f"{abs(stress):.1f} ({t_or_c})",
# #         f"{abs(force) / 1e3:.1f}",
# #         f"{d_y:.1f}",
# #         f"{moment_x / 1e6:.2f}",
# #     )

# # console = Console()
# # console.print(table)

# # # sum of forces
# # int_force = sum(forces) + f_conc
# # print(f"Sum of Internal Forces: {int_force / 1e3:.2f} kN")

# # # sum of moments
# # int_moment = sum(moments_x) + m_conc
# # print(f"Sum of Internal Moments: {int_moment / 1e6:.2f} kN.m")
# # print(f"External Moment: {m_ext / 1e6:.2f} kN.m")