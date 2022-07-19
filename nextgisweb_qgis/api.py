from pyramid.response import FileResponse, Response

from nextgisweb.resource import resource_factory, ResourceScope

from .model import QgisVectorStyle, QgisRasterStyle, read_style


def style_qml(resource, request):
    request.resource_permission(ResourceScope.read)

    if resource.qml_fileobj_id is not None:
        fn = request.env.file_storage.filename(resource.qml_fileobj)
        response = FileResponse(fn, request=request)
    else:
        style = read_style(resource)
        response = Response(style.to_string(), request=request)
    response.content_disposition = 'attachment; filename=%d.qml' % resource.id

    return response


def setup_pyramid(comp, config):
    config.add_route(
        'qgis.style_qml', '/api/resource/{id}/qml',
        factory=resource_factory
    ) \
        .add_view(style_qml, context=QgisVectorStyle, request_method='GET') \
        .add_view(style_qml, context=QgisRasterStyle, request_method='GET')
