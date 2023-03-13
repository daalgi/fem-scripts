import meshio


def print_mesh_info(file: str):
    m = meshio.read(file)
    print('-' * 60)
    print('Mesh information')
    print('-' * 60)
    print(m)

    print("\n>>meshio object attributes:")
    for att in m.__dict__.items():
        print(att)

    print("\n>>points:")
    npoints = len(m.points)
    for att in m.points[:min(5, npoints)]:
        print(att)

    print("\n>>cells:")
    for att in m.cells:
        print(att)

    print("\n>>cells[0]:", type(m.cells[0]))
    for att in m.cells[0].__dict__.items():
        print(att)

    print("\n>>cells[1]:", type(m.cells[1]))
    for att in m.cells[1].__dict__.items():
        print(att)


if __name__ == "__main__":
    file = "./meshing/foundation2d.med"
    print_mesh_info(file=file)
