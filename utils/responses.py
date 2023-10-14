from rest_framework import status


class ResponseData:
    status: str
    message: str


class ResponseModel:
    @staticmethod
    def respond(status_req: str, message: str | object, data=None):
        response: ResponseData = ResponseData()
        response.status = status_req
        response.message = message
        if data is not None:
            response.data = data
        return response

    @staticmethod
    def get_respond(data=None, success: bool = True, error_type: int = None):
        status_req = status.HTTP_200_OK
        message = "Registros obtenidos satisfactoriamente" if success else "Sin registros" if error_type == 1 else "No encontrado"
        response = ResponseModel.respond(status_req, message, data)
        return response.__dict__

    @staticmethod
    def post_respond(data=None, success: bool = True, errors=None, title: str = None, status_peticion: int = None):
        if success:
            status_req = status.HTTP_201_CREATED if title is None else status.HTTP_200_OK
            message = f"Se ha {title if title is not None else 'guardado'} satisfactoriamente"
            response = ResponseModel.respond(status_req, message, data)
        else:
            status_req = status.HTTP_409_CONFLICT if status_peticion is None else status_peticion
            response = ResponseModel.respond(status_req, errors)
        return response.__dict__

    @staticmethod
    def put_respond(data=None, is_success: bool = None, errors=None, reason: int = None):
        if not is_success:
            if reason == 2:
                status_req = status.HTTP_204_NO_CONTENT
            else:
                status_req = status.HTTP_400_BAD_REQUEST
            message = errors
            response = ResponseModel.respond(status_req, message)
        else:
            status_req = status.HTTP_200_OK
            message = "Guardado Exitosamente"
            response = ResponseModel.respond(status_req, message, data)
        return response.__dict__

    @staticmethod
    def delete_respond(is_success: bool = True):
        status_req = status.HTTP_200_OK if is_success else status.HTTP_204_NO_CONTENT
        message = "Eliminado Exitosamente" if is_success else "Registro no encontrado"
        response = ResponseModel.respond(status_req, message)
        return response.__dict__
    
    @staticmethod
    def unauthorized_respond(success: bool = True, errors=None, title: str = None, status_peticion: int = None):
        status_req = status.HTTP_401_UNAUTHORIZED
        response = ResponseModel.respond(status_req, errors)
        return response.__dict__
    @staticmethod
    
    def no_content_respond(data=None, is_success: bool = None, errors=None, reason: int = None):
        status_req = status.HTTP_204_NO_CONTENT
        message = errors
        response = ResponseModel.respond(status_req, message)
        return response.__dict__
