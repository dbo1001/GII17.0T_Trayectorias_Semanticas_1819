from wtforms import Form
from wtforms import StringField,IntegerField,validators
class FormularioCargar(Form):
    columnaTiempo2=IntegerField("Columna de tiempo 2:",[validators.Required()],id="columnaTiempo2")
    formatoTiempo1=StringField("Formato del tiempo 1:",[validators.Required()],id="formatoTiempo1")