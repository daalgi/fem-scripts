from dataclasses import dataclass, field

@dataclass
class Section:
    points: list
    lines: list
    surface: int
    transfinite: list = field(default_factory=list)
    embedded: list = field(default_factory=list)

def _create_section(points: list, factory):
    lines = [factory.addLine(points[i-1], points[i]) for i in range(1, len(points))]
    lines.append(factory.addLine(points[-1], points[0]))

    boundaries = factory.addCurveLoop(lines, 1)
    surface = factory.addPlaneSurface([boundaries], boundaries)
    factory.synchronize()

    return lines, surface


def section_rectangular(height: float, width: float, factory):
    points = []
    points.append(factory.addPoint(-width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2, 0))
    lines, surface = _create_section(points, factory)
    return Section(
        points=points,
        lines=lines,
        surface=surface
    )


def section_I(height: float, width: float, flange_th: float, web_th: float, factory):
    points = []
    points.append(factory.addPoint(-width/2, -height/2, 0))
    points.append(factory.addPoint(-web_th/2, -height/2, 0))
    points.append(factory.addPoint(+web_th/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(+web_th/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(+web_th/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(+width/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(+width/2, +height/2, 0))
    points.append(factory.addPoint(+web_th/2, +height/2, 0))
    points.append(factory.addPoint(-web_th/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(-web_th/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(-web_th/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(-width/2, -height/2+flange_th, 0))
    lines, surface = _create_section(points, factory)

    transfinite_lines = []#[lines[1], lines[3], lines[5]]
    """ptemp = []
    ptemp.append(factory.addPoint(+web_th/2, -height/2+flange_th, 0))
    ptemp.append(factory.addPoint(+web_th/2, -height/2, 0))
    lines_embedded = []
    lines_embedded.append(factory.addLine(ptemp[0], ptemp[1]))
    """
    lines_embedded = []
    lines_embedded.append((points[1], points[-2]))
    lines_embedded.append((points[2], points[5]))

    lines_embedded.append((points[5], points[-2]))

    lines_embedded.append((points[6], points[9]))
    lines_embedded.append((points[10], points[13]))

    lines_embedded.append((points[6], points[13]))
    
    """lines_embedded.append((
        factory.addPoint(+web_th/2, -height/2+flange_th, 0), 
        factory.addPoint(+web_th/2, -height/2, 0)
    ))
    lines_embedded.append((
        factory.addPoint(-web_th/2, -height/2+flange_th, 0), 
        factory.addPoint(-web_th/2, -height/2, 0)
    ))"""
    """lines_embedded.append(factory.addLine(
        factory.addPoint(+web_th/2, +height/2-flange_th, 0), 
        factory.addPoint(+web_th/2, +height/2, 0)
    ))
    lines_embedded.append(factory.addLine(
        factory.addPoint(-web_th/2, +height/2-flange_th, 0), 
        factory.addPoint(-web_th/2, +height/2, 0)
    ))"""
    return Section(
        points=points,
        lines=lines,
        surface=surface,
        transfinite=transfinite_lines,
        embedded=lines_embedded
    )

