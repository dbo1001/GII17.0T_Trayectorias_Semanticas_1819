from wtforms import Form
from wtforms import TextAreaField
class FormularioExportar(Form):
    select=TextAreaField("Introduzca una consulta SELECT de los datos que desea exportar",id="select")