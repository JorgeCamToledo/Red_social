from rest_framework import status

# Excepción que servirá para personalizar los errores
class ExcepcionPersonalizada(Exception):
    def __init__(self, mensaje="Error en la solicitud", status=status.HTTP_400_BAD_REQUEST):
        self.mensaje=mensaje
        self.status=status
        super().__init__(self.mensaje)