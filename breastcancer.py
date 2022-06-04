# -*- coding: utf8 -*-
"""
created on Wed June 06 2022
@ author : windows10
"""
from pydantic import BaseModel


# class which describes Breast cancer measurements
class BreastCancer(BaseModel):
    Radius_mean: float
    Radius_texture: float
    Method: str
