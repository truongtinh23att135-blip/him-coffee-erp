{
    "name": "HIM Shop - Nút Gửi Bar trên POS",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Thêm nút Gửi Bar vào màn hình POS, gửi phần món mới xuống màn hình Bar",
    "author": "HIM COFFEE ERP",
    "depends": ["point_of_sale", "him_shop_pos"],
    "assets": {
        "point_of_sale._assets_pos": [
            "him_shop_pos_button/static/src/pos_bar_button.js",
            "him_shop_pos_button/static/src/pos_bar_button.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
