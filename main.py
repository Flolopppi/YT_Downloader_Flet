from flet import *
import time
import threading
from YoTube_object import youtube_downloader_object


def main(page: Page):
    page.title = 'YouTube Downloader'
    page.window.width = 700
    page.window.height = 150
    page.fonts = {
        'Satoshi': '/Users/florianpaulus/Library/Fonts/Satoshi-Medium.otf'
    }
    page.theme = Theme(font_family='Satoshi')
    page.bgcolor = '#fffbf8'

# ---------------------- PROGRESS BAR, Update, Reset


    p_bar = ProgressBar(
        width=510,
        height=10,
        border_radius=25,
        color='#7bcf50',
        bgcolor='#ffebe6',
        value=0,
        visible=False
    )

    p_label = Text(
        '',
    )

    def update_p_bar_value():
        while youtube_downloader_object.stop_progress == False:
            p_bar.visible = True
            p_bar.value = float(youtube_downloader_object.percentage_of_completion) / 100
            p_label.value = f'{str(int(youtube_downloader_object.percentage_of_completion))}%'
            if youtube_downloader_object.percentage_of_completion == '100':
                youtube_downloader_object.stop_progress = True
                p_label.value = 'Done!'
            page.update()
            time.sleep(.2)


    def reset_p_bar_value():
        p_bar.value = 0
        p_label.value = '0%'
        youtube_downloader_object.stop_progress = False
        youtube_downloader_object.percentage_of_completion = '0'
        page.update()


# ---------------------- DOWNLOAD BUTTON, on_click, get URL Input


    def btn_activate_is_true():
        if youtube_downloader_object.selected_output != '' and url_textfield.value != '':
            download_btn.disabled = False
            download_btn.bgcolor = '#f76a4a'
            page.update()
        elif youtube_downloader_object.selected_output != '' and url_textfield.value == '':
            download_btn.disabled = True
            download_btn.bgcolor='#ffcec2'
            page.update()
        elif youtube_downloader_object.select_folder == '' and url_textfield.value != '':
            download_btn.disabled = True
            download_btn.bgcolor='#ffcec2'
            page.update()


    url_textfield = TextField(
        label='enter YouTube link',
        border_radius=10,
        height=40,
        text_size= 14,
        border_width=2.5,
        border_color='#f76a4a',
        bgcolor='#fffbf8',
        on_change=lambda _: btn_activate_is_true()
        )


    def on_download_btn_click():
        reset_p_bar_value()
        sep_thread = threading.Thread(target=youtube_downloader_object.download_video, 
                                      args=(get_textfield_value(),))
        sep_thread.start()
        update_p_bar_value()
        

    def get_textfield_value():
        url = url_textfield.value
        return url


    download_btn = IconButton(
        disabled=True,
        icon_color='#ffffff',
        icon=icons.DOWNLOAD_ROUNDED,
        bgcolor='#ffcec2',
        on_click=lambda _: on_download_btn_click()
    )


# ---------------------- FILE PICKER, SELECT FOLDER BUTTON, on_click, get selected Folder/Path


    def on_dialog_result(e: FilePickerResultEvent):
        youtube_downloader_object.selected_output = e.path
        btn_activate_is_true()

    file_picker = FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    select_folder_btn = IconButton(
        icon=icons.FOLDER_ROUNDED,
        icon_color='#ffffff',
        bgcolor='#f76a4a',
        mouse_cursor='click',
        on_click=lambda _: file_picker.get_directory_path()
    )


# ---------------------- ADD WIDGETS TO PAGE


    page.add(
        Column(
            spacing=0,
            controls=[
                Container(
                    content=url_textfield,
                    padding=5,
                    margin=0
                ),
                Container(
                    padding=5,
                    margin=0,
                    content=Row(    
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Row(spacing=10,
                                controls=[
                                    p_bar,
                                    p_label
                                ]
                            ),
                            Row(
                                controls=[
                                    download_btn,
                                    select_folder_btn
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    )


# ---------------------- RUN APP

app(target=main)