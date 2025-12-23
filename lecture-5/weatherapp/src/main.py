import flet as ft
import requests
from datetime import datetime

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.padding = 0
    page.bgcolor = "#B0BEC5"

    area_json = requests.get(AREA_URL).json()
    centers = area_json["centers"]   
    offices = area_json["offices"]   

 
    weather_cards = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
    )

    def weather_icon(weather):
        if "雨" in weather:
            return ft.Icons.UMBRELLA, "blue"
        elif "雪" in weather:
            return ft.Icons.AC_UNIT, "lightblue"
        elif "曇" in weather:
            return ft.Icons.CLOUD, "grey"
        else:
            return ft.Icons.WB_SUNNY, "orange"

    def load_weather(area_code):
        weather_cards.controls.clear()

        try:
            data = requests.get(FORECAST_URL.format(area_code)).json()
        except Exception:
            weather_cards.controls.append(
                ft.Text("天気情報を取得できませんでした", color="red")
            )
            page.update()
            return

        ts_weather = data[0]["timeSeries"][0]
        ts_temp = data[1]["timeSeries"][1]

        dates = ts_weather["timeDefines"][:7]
        weathers = ts_weather["areas"][0]["weathers"][:7]
        temps_min = ts_temp["areas"][0]["tempsMin"][:7]
        temps_max = ts_temp["areas"][0]["tempsMax"][:7]

        for i in range(len(dates)):
            icon, color = weather_icon(weathers[i])
            date_str = datetime.fromisoformat(dates[i]).strftime("%Y-%m-%d")

            weather_cards.controls.append(
                ft.Container(
                    width=160,
                    padding=15,
                    bgcolor="white",
                    border_radius=12,
                    content=ft.Column(
                        horizontal_alignment="center",
                        controls=[
                            ft.Text(date_str, weight="bold"),
                            ft.Icon(icon, size=40, color=color),
                            ft.Text(weathers[i], size=12),
                            ft.Row(
                                alignment="center",
                                controls=[
                                    ft.Text(
                                        f"{temps_min[i]}°C",
                                        color="blue"
                                    ),
                                    ft.Text(" / "),
                                    ft.Text(
                                        f"{temps_max[i]}°C",
                                        color="red"
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )

        page.update()


    sidebar = ft.Container(
        width=260,
        bgcolor="#78909C",
        padding=15,
        content=ft.Column(
            scroll="auto",
            controls=[
                ft.Text("地域を選択", color="white", size=16, weight="bold"),
                ft.Divider(color="white"),
            ],
        ),
    )

    for center in centers.values():
        prefecture_tiles = []

        for office_code in center["children"]:
            office = offices[office_code]
            prefecture_tiles.append(
                ft.ListTile(
                    title=ft.Text(office["name"], color="white"),
                    on_click=lambda e, c=office_code: load_weather(c),
                )
            )

        sidebar.content.controls.append(
            ft.ExpansionTile(
                title=ft.Text(center["name"], color="white"),
                controls=prefecture_tiles,
                icon_color="white",
                collapsed_icon_color="white",
            )
        )

    main_area = ft.Container(
        expand=True,
        padding=30,
        content=weather_cards,
    )


    page.add(
        ft.Row(
            expand=True,
            controls=[
                sidebar,
                main_area,
            ],
        )
    )


ft.app(main)
