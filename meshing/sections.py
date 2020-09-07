def _create_section(points: list, factory):
    lines = [factory.addLine(points[i-1], points[i]) for i in range(1, len(points))]
    lines.append(factory.addLine(points[-1], points[0]))

    boundaries = factory.addCurveLoop(lines, 1)
    section = factory.addPlaneSurface([boundaries], boundaries)
    factory.synchronize()

    return points, lines, section


def section_rectangular(height: float, width: float, factory):
    points = []
    points.append(factory.addPoint(-width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2, 0))
    return _create_section(points, factory)


def section_I(height: float, width: float, flange_th: float, web_th: float, factory):
    points = []
    points.append(factory.addPoint(-width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2, 0))
    points.append(factory.addPoint(+width/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(+web_th/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(+web_th/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(+width/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(+width/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2, 0))
    points.append(factory.addPoint(-width/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(-web_th/2, +height/2-flange_th, 0))
    points.append(factory.addPoint(-web_th/2, -height/2+flange_th, 0))
    points.append(factory.addPoint(-width/2, -height/2+flange_th, 0))
    return _create_section(points, factory)
