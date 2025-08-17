import subprocess
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage, NewLine,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZNode, TikZOptions, TikZCoordinate,\
    VerticalSpace, HorizontalSpace,\
    LongTabularx, Tabularx,\
    config
from pylatex.base_classes import Arguments, Environment
from pylatex.utils import NoEscape, bold, italic
import funciones as fun

activ = pd.read_csv("actividades.csv")
datos = pd.read_csv("datos.csv")

print(datos)
print(activ)

class Schedule(Environment):
    """Custom LaTeX environment for the schedule package."""
    _latex_name = 'schedule'
    packages = [Package('schedule')]


def generar_horario(datos,actividades):
    #Config
    config.active = config.Version1(row_heigth=1.5)
    #Geometry
    geometry_options = {
        "left": "1mm",
        "right": "5mm",
        "top": "20mm",
        "bottom": "20mm",
    }
    #Document options
    doc = Document(documentclass="article", \
                    fontenc=None, \
                    inputenc=None, \
                    lmodern=False, \
                    textcomp=False, \
                    page_numbers=False, \
                    indent=True, \
                    document_options=["landscape", "12pt", "dvipsnames"], \
                    geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="schedule", options=None))
    doc.packages.append(Package(name="fontawesome", options=None))
    #Preamble
    doc.preamble.append(NoEscape(r"""
\makeatletter
\def\@M@week{{Lunes} {Martes} {Miércoles} {Jueves} {Viernes} {Saturday} {Sunday}}
\makeatother
"""))
    doc.preamble.append(Command("CellHeight", "1.1cm"))
    doc.preamble.append(Command("CellWidth", "5cm"))
    doc.preamble.append(Command("TimeRange", NoEscape(r"7:00-21:00")))
    doc.preamble.append(Command("SubUnits", "30"))
    doc.preamble.append(Command("BeginOn", "Monday"))
    doc.preamble.append(Command("TextSize", NoEscape(r"\small")))
    doc.preamble.append(Command("FiveDay"))
    #define the appointments
    doc.preamble.append(Command("NewAppointment", ["curso", "blue!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["consu", "brown!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["admin", "cyan!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["inves", "green!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["libre", "dark", "black"]))
    doc.preamble.append(Command("NewAppointment", ["desca", "teal!20!white", "black"]))
    #Read data
    sem = str(datos['semestre'].item())
    año = datos['año'].item()

    doc.change_page_style("empty")

    with doc.create(Schedule(options=NoEscape(f'''{fun.number_to_ordinals(sem)} semestre, {año}'''))) as sched:

        # \adm{Comisión para creación\\ de Electromecánica}{}{M}{7:30-11:30}
        sched.append(Command("admin", [
            NoEscape(r"Comisión para creación\\\\ de Electromecánica"), r"", r"M", NoEscape(r"7:30-11:30")]))
    
    # doc.append(NewLine())
    # doc.append(Command("centering"))
    # doc.append(italic("Dr.-Ing. Juan J. Rojas"))
    # doc.append(NoEscape(r"\,\, "))
    # #phone
    # doc.append(Command("faPhone"))
    # doc.append(NoEscape(r"\,\, 8858-1419 \,\, "))
    # #mail
    # doc.append(Command("faEnvelope"))
    # doc.append(" juan.rojas@itcr.ac.cr ")
    # doc.append(NoEscape(r"\,\, "))
    # doc.append(HorizontalSpace("0.333em"))
    doc.generate_pdf(f"Horario-{sem}-{año}", clean=False, clean_tex=False, compiler='lualatex')

generar_horario(datos,activ)