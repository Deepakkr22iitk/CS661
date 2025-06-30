# contour_extract.p_y
# that script imports a 2D scalar field from a .vti file and obtains an isocontour.
# (line of fixed scalar value) through linear interpolation at cell boundaries.
#  The output is stored in VTK PolyData format (.vtp).

import vtk
import argparse

# Function to linearly interpolate where the contour crosses an edge
def inter_polate(p1, p2, v1, v2, iso):
    t = (iso - v1) / (v2 - v1)
    return [p1[i] + t * (p2[i] - p1[i]) for i in range(2)]

def main():
    # Taking isovalue as input 
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--isovalue', type=float, required=True, help='Isovalue for contour extraction')
    args = argparser.parse_args()
    isovalue = args.isovalue

    # Reading  the 2D VTK image data (.vti file)
    vti_reader = vtk.vtkXMLImageDataReader()
    vti_reader.SetFileName("Data/Isabel_2D.vti")  
    vti_reader.Update()
    data = vti_reader.GetOutput()

    # Get the dimensions, spacing, origin, and scalar values from the dataset
    dimension = data.GetDimensions()
    space = data.GetSpacing()
    grid_origin = data.GetOrigin()
    scalar_value = data.GetPointData().GetScalars()

    # Preparing to store contour line points and connections
    counter_points = vtk.vtkPoints()
    contour_lines = vtk.vtkCellArray()
    countr_point_id = 0

    # Function to convert (x, y) cell index to flat array index
    def index(x, y):
        return y * dimension[0] + x

    # Looping over each cell in the grid
    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            # Get 4 vertices of the cell
            grid_vertices = [(i, j), (i+1, j), (i+1, j+1), (i, j+1)]
            vertice_position = []  # To store (x, y) position of vertices
            vertice_value = []     # To store scalar value at each vertice

            for x, y in grid_vertices:
                p_x = grid_origin[0] + x * space[0]
                p_y = grid_origin[1] + y * space[1]
                vertice_position.append((p_x, p_y))
                vertice_value.append(scalar_value.GetTuple1(index(x, y)))

            # Checking which edges are crossed by the isocontour
            intersectpoints = []
            edge_pair = [(0, 1), (1, 2), (2, 3), (3, 0)]

            for a, b in edge_pair:
                v1, v2 = vertice_value[a], vertice_value[b]
                if (v1 - isovalue) * (v2 - isovalue) < 0:
                    pt = inter_polate(vertice_position[a], vertice_position[b], v1, v2, isovalue)
                    intersectpoints.append(pt)

            # If two crossings are found, create a contour line segment
            if len(intersectpoints) == 2:
                id1 = countr_point_id
                counter_points.InsertNextPoint(intersectpoints[0][0], intersectpoints[0][1], 0)
                countr_point_id += 1

                id2 = countr_point_id
                counter_points.InsertNextPoint(intersectpoints[1][0], intersectpoints[1][1], 0)
                countr_point_id += 1

                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, id1)
                line.GetPointIds().SetId(1, id2)
                contour_lines.InsertNextCell(line)

    # Create polydata to store the output
    vtk_polydata = vtk.vtkPolyData()
    vtk_polydata.SetPoints(counter_points)
    vtk_polydata.SetLines(contour_lines)

    # Write the result to a .vtp file
    vtk_writer = vtk.vtkXMLPolyDataWriter()
    vtk_writer.SetFileName("isocontour.vtp")
    vtk_writer.SetInputData(vtk_polydata)
    vtk_writer.Write()

    print(" isocontour.vtp saved")

if __name__ == "__main__":
    main()

