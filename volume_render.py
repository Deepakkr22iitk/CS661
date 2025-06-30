
#volume_render.py
# The script renders the a hurricane scalar field data (3D .vti file)
# using VTK's volume rendering. Optional Phong shading can be enabled via CLI.


import vtk
import argparse
import os
import faulthandler

faulthandler.enable()

data_path = os.path.join("Data", "Isabel_3D.vti")

def volume_render(apply_phong_shading):

    # loading the 3D data into the reader object
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(data_path)
    reader.Update()
    input_vol_data = reader.GetOutput()
    
    # creating an outline filter
    outl_filter = vtk.vtkOutlineFilter()
    outl_filter.SetInputData(input_vol_data)

    # creating an outline filter mapper
    outl_mapper = vtk.vtkPolyDataMapper()
    outl_mapper.SetInputConnection(outl_filter.GetOutputPort())
    
    # creating the outline actor
    outl_actor = vtk.vtkActor()
    outl_actor.SetMapper(outl_mapper)
    outl_actor.GetProperty().SetColor(1, 1, 1)
    
    # initializing the color transfer function and opacity function
    tf = vtk.vtkColorTransferFunction()
    tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    tf.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
    tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    tf.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

    opf = vtk.vtkPiecewiseFunction()
    opf.AddPoint(-4931.54, 1.0)
    opf.AddPoint(101.815, 0.002)
    opf.AddPoint(2594.97, 0.0)

    # Creating the volume property mapper and adding the properties to it
    vol_property = vtk.vtkVolumeProperty()
    vol_property.SetColor(tf)
    vol_property.SetScalarOpacity(opf)

    if apply_phong_shading:

        vol_property.ShadeOn()
        vol_property.SetAmbient(0.5)
        vol_property.SetDiffuse(0.5)
        vol_property.SetSpecular(0.5)
        vol_property.SetSpecularPower(10)

    vol_property.SetInterpolationTypeToLinear()

    # Creating the volume Mapper
    vol_mapper = vtk.vtkSmartVolumeMapper()
    vol_mapper.SetInputData(input_vol_data)

    # Creating the volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(vol_mapper)
    volume.SetProperty(vol_property)

    # Rendering the volume data
    renderer = vtk.vtkRenderer()
    rendering_window = vtk.vtkRenderWindow()
    rendering_window.SetSize(1000, 1000)
    rendering_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    interactor.SetRenderWindow(rendering_window)
    renderer.SetBackground(0.5, 0.5, 0.5)
    renderer.AddActor(outl_actor)
    renderer.AddVolume(volume)
    rendering_window.Render()
    interactor.Start()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--phongshading", type = str, choices = ["yes", "no"], default = "no")
    args = parser.parse_args()
    if args.phongshading == "yes":
        apply_phong_shading = True
    else: 
        apply_phong_shading = False
    
    volume_render(apply_phong_shading)

