import bpy
from bpy.props import *
from bpy.types import ShapeKey
from .. events import propertyChanged
from .. base_types import AnimationNodeSocket, PythonListSocket

class ShapeKeySocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_ShapeKeySocket"
    bl_label = "Shape Key Socket"
    dataType = "Shape Key"
    drawColor = (1.0, 0.6, 0.5, 1)
    storable = False
    comparable = True

    object: PointerProperty(type = bpy.types.Object, update = propertyChanged,
        description = "Load the second shape key of this object (the first that is not the reference key)")

    def drawProperty(self, layout, text, node):
        row = layout.row(align = True)
        row.prop(self, "object", text = text)
        self.invokeFunction(row, node, "assignActiveObject", icon = "EYEDROPPER")

    def getValue(self):
        if getattr(self.object, "type", "") not in ("MESH", "CURVE", "LATTICE"): return None
        if self.object.data.shape_keys is None: return None

        try: return self.object.data.shape_keys.key_blocks[1]
        except: return None

    def assignActiveObject(self):
        object = bpy.context.active_object
        if object:
            self.object = object

    def setProperty(self, object):
        self.object = object

    def getProperty(self):
        return self.object

    @classmethod
    def getDefaultValue(cls):
        return None

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, ShapeKey) or value is None:
            return value, 0
        return cls.getDefaultValue(), 2


class ShapeKeyListSocket(bpy.types.NodeSocket, PythonListSocket):
    bl_idname = "an_ShapeKeyListSocket"
    bl_label = "Shape Key List Socket"
    dataType = "Shape Key List"
    baseType = ShapeKeySocket
    drawColor = (1.0, 0.6, 0.5, 0.5)
    storable = False
    comparable = False

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, list):
            if all(isinstance(element, ShapeKey) or element is None for element in value):
                return value, 0
        return cls.getDefaultValue(), 2
