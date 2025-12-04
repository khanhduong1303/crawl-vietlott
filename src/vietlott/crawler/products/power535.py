from vietlott.crawler.products.power655 import ProductPower655
from vietlott.crawler.schema.requests import RequestPower535


class ProductPower535(ProductPower655):
    name = "power_535"
    url = "https://vietlott.vn/ajaxpro/Vietlott.PlugIn.WebParts.Game535CompareWebPart,Vietlott.PlugIn.WebParts.ashx"

    org_body = RequestPower535(
        ORenderInfo=ProductPower655.orender_info_default,
        Key="d0ea794f",
        GameDrawId="",
        ArrayNumbers=[["" for _ in range(18)] for _ in range(5)],
        CheckMulti=False,
        PageIndex=0,
    )
