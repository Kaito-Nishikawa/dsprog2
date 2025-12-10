import flet as ft

def main(page: ft.Page):
    # カウンター表示用のテキスト
    counter = ft.Text("0", size=50, data=0)

    

    # 増やす処理
    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    # 減らす処理
    def decrement_click(e):
        counter.data -= 1
        counter.value = str(counter.data)
        counter.update()

    # 増やすボタン（右下のFAB）
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, 
        on_click=increment_click
    )

    # 減らすボタン
    minus_button = ft.ElevatedButton(
        text="-1",
        on_click=decrement_click
    )

    # safe areaで中央にカウンター & 減らすボタンを配置
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    counter,
                    minus_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

ft.app(main)

 
