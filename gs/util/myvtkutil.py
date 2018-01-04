# -*- coding:utf-8 -*-
import gzip
import hashlib
import json
import shutil
import sys

import os

jsMapping = {
    'b': 'Int8Array',
    'B': 'Uint8Array',
    'h': 'Int16Array',
    'H': 'Int16Array',
    'i': 'Int32Array',
    'I': 'Uint32Array',
    'l': 'Int32Array',
    'L': 'Uint32Array',
    'f': 'Float32Array',
    'd': 'Float64Array'
}
arrayTypesMapping = '  bBhHiIlLfdL'  # last one is idtype


def writeDataSet(filePath, dataset, outputDir, newDSName=None, compress=True):
    fileName = newDSName if newDSName else os.path.basename(filePath)
    datasetDir = os.path.join(outputDir, fileName)
    dataDir = os.path.join(datasetDir, 'data')

    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    root = {}
    root['metadata'] = {}
    root['metadata']['name'] = fileName

    dumpImageData(datasetDir, dataDir, dataset, root, compress)

    with open(os.path.join(datasetDir, "index.json"), 'w') as f:
        f.write(json.dumps(root, indent=2))


def dumpImageData(datasetDir, dataDir, dataset, container={}, compress=True):
    container['vtkClass'] = 'vtkImageData'

    # Origin / Spacing / Dimension
    container['origin'] = tuple(dataset.GetOrigin())
    container['spacing'] = tuple(dataset.GetSpacing())
    extent = list(dataset.GetExtent())
    for i in (1, 3, 5):
        extent[i] = extent[i] - extent[i - 1]
    for i in (0, 2, 4):
        extent[i] = 0
    container['extent'] = tuple(extent)

    # Attributes (PointData, CellData, FieldData)
    dumpAttributes(datasetDir, dataDir, dataset, container, compress)

    return container


def dumpAttributes(datasetDir, dataDir, dataset, root={}, compress=True):
    # PointData
    _pointData = root['pointData'] = {"vtkClass": "vtkDataSetAttributes", "arrays": []}
    _nbFields = dataset.GetPointData().GetNumberOfArrays()
    for i in range(_nbFields):
        array = dataset.GetPointData().GetArray(i)
        abstractArray = dataset.GetPointData().GetAbstractArray(i)
        if array:
            _array = dumpDataArray(datasetDir, dataDir, array, {}, compress)
            if _array:
                _pointData['arrays'].append({"data": _array})
        elif abstractArray:
            _array = dumpStringArray(datasetDir, dataDir, abstractArray, {}, compress)
            if _array:
                _pointData['arrays'].append({"data": _array})

    # CellData
    _cellData = root['cellData'] = {"vtkClass": "vtkDataSetAttributes", "arrays": []}
    _nbFields = dataset.GetCellData().GetNumberOfArrays()
    for i in range(_nbFields):
        array = dataset.GetCellData().GetArray(i)
        abstractArray = dataset.GetCellData().GetAbstractArray(i)
        if array:
            _array = dumpDataArray(datasetDir, dataDir, array, {}, compress)
            if _array:
                _cellData['arrays'].append({"data": _array})
        elif abstractArray:
            _array = dumpStringArray(datasetDir, dataDir, abstractArray, {}, compress)
            if _array:
                _cellData['arrays'].append({"data": _array})

    # FieldData
    _fieldData = root['FieldData'] = {"vtkClass": "vtkDataSetAttributes", "arrays": []}
    _nbFields = dataset.GetFieldData().GetNumberOfArrays()
    for i in range(_nbFields):
        array = dataset.GetFieldData().GetArray(i)
        abstractArray = dataset.GetFieldData().GetAbstractArray(i)
        if array:
            _array = dumpDataArray(datasetDir, dataDir, array, {}, compress)
            if _array:
                _fieldData['arrays'].append({"data": _array})
        elif abstractArray:
            _array = dumpStringArray(datasetDir, dataDir, abstractArray, {}, compress)
            if _array:
                _fieldData['arrays'].append({"data": _array})
    return root


def dumpStringArray(datasetDir, dataDir, array, root={}, compress=True):
    if not array:
        return None

    stringArray = []
    arraySize = array.GetNumberOfTuples()
    for i in range(arraySize):
        stringArray.append(array.GetValue(i))

    strData = json.dumps(stringArray)

    pMd5 = hashlib.md5(strData).hexdigest()
    pPath = os.path.join(dataDir, pMd5)
    with open(pPath, 'wb') as f:
        f.write(strData)

    if compress:
        with open(pPath, 'rb') as f_in, gzip.open(os.path.join(dataDir, pMd5 + '.gz'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_in.close()
            os.remove(pPath)

    root['ref'] = getRef(os.path.relpath(dataDir, datasetDir), pMd5)
    root['vtkClass'] = 'vtkStringArray'
    root['name'] = array.GetName()
    root['dataType'] = 'JSON'
    root['numberOfComponents'] = array.GetNumberOfComponents()
    root['size'] = array.GetNumberOfComponents() * array.GetNumberOfTuples()

    return root


def dumpDataArray(datasetDir, dataDir, array, root={}, compress=True):
    if not array:
        return None

    if array.GetDataType() == 12:
        # IdType need to be converted to Uint32
        arraySize = array.GetNumberOfTuples() * array.GetNumberOfComponents()
        newArray = vtk.vtkTypeUInt32Array()
        newArray.SetNumberOfTuples(arraySize)
        for i in range(arraySize):
            newArray.SetValue(i, -1 if array.GetValue(i) < 0 else array.GetValue(i))
        pBuffer = buffer(newArray)
    else:
        pBuffer = buffer(array)

    pMd5 = hashlib.md5(pBuffer).hexdigest()
    pPath = os.path.join(dataDir, pMd5)
    with open(pPath, 'wb') as f:
        f.write(pBuffer)

    if compress:
        with open(pPath, 'rb') as f_in, gzip.open(os.path.join(dataDir, pMd5 + '.gz'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_in.close()
            os.remove(pPath)

    # print array
    # print array.GetName(), '=>', jsMapping[arrayTypesMapping[array.GetDataType()]]

    root['ref'] = getRef(os.path.relpath(dataDir, datasetDir), pMd5)
    root['vtkClass'] = 'vtkDataArray'
    root['name'] = array.GetName()
    root['dataType'] = jsMapping[arrayTypesMapping[array.GetDataType()]]
    root['numberOfComponents'] = array.GetNumberOfComponents()
    root['size'] = array.GetNumberOfComponents() * array.GetNumberOfTuples()
    root['ranges'] = []
    if root['numberOfComponents'] > 1:
        for i in range(root['numberOfComponents']):
            root['ranges'].append(getRangeInfo(array, i))
        root['ranges'].append(getRangeInfo(array, -1))
    else:
        root['ranges'].append(getRangeInfo(array, 0))

    return root


def getRangeInfo(array, component):
    r = array.GetRange(component)
    compRange = {}
    compRange['min'] = r[0]
    compRange['max'] = r[1]
    compRange['component'] = array.GetComponentName(component)
    return compRange


def getRef(destDirectory, md5):
    ref = {}
    ref['registration'] = "setScalars"
    ref['id'] = md5
    ref['encode'] = 'BigEndian' if sys.byteorder == 'big' else 'LittleEndian'
    ref['basepath'] = destDirectory
    return ref
