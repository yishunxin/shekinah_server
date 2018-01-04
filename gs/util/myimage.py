import numpy as np


# import SimpleITK as sitk


def get_LUT_value(data, window, level):
    return np.piecewise(data,
                        [data <= (level - 0.5 - (window - 1) / 2),
                         data > (level - 0.5 + (window - 1) / 2)],
                        [0, 255, lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0)])


def voxel_2_world(voxel_coordinates, origin, spacing):
    stretched_voxel_coordinates = voxel_coordinates * spacing
    world_coordinates = stretched_voxel_coordinates + origin
    return map(lambda x: round(x, 4), world_coordinates)


def world_2_voxel(world_coordinates, origin, spacing):
    stretched_voxel_coordinates = np.absolute(world_coordinates - origin)
    voxel_coordinates = stretched_voxel_coordinates / spacing
    return map(int, map(round, voxel_coordinates))


# # Z X Y
# def load_itk(filename):
#     itkimage = sitk.ReadImage(filename)
#     image = sitk.GetArrayFromImage(itkimage)
#     origin = np.array(list(reversed(itkimage.GetOrigin())))
#     spacing = np.array(list(reversed(itkimage.GetSpacing())))
#     return image, origin, spacing
#
#
# # Z, Y, X
# def load_scan(path):
#     reader = sitk.ImageSeriesReader()
#     dicom_names = reader.GetGDCMSeriesFileNames(path)
#     reader.SetFileNames(dicom_names)
#     itkimage = reader.Execute()
#     # image = sitk.GetArrayFromImage(itkimage)
#     origin = np.array(list(reversed(itkimage.GetOrigin())))
#     spacing = np.array(list(reversed(itkimage.GetSpacing())))
#     return origin, spacing
