from dataclasses import dataclass


@dataclass(frozen=True)
class Cabeceras:
    nombre_pagina: str
    nombre_DB: str