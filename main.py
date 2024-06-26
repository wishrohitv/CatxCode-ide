from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.splitter import Splitter
from plyer import filechooser
from app_storage_implement.app_storage import storage_path
import threading, time, asyncio, os, sys, io
from kivy.app import App

from components.sidemenu.side_menu import SideMenuTabWindows


class EditorApp(App):
    console_open = True
    side_menu_open = True

    def build(self):
        # front ui
        self.title = "CodeEditor"
        self.icon = "assets/icons/icon-x.jpg"

        return Builder.load_file("main.kv")

    def on_start(self):
        Window.softinput_mode = 'below_target'

    # code logic starts here --
    def __init__(self, **args):
        super(EditorApp, self).__init__(**args)
        self.current_tabs_active_code = ""
        self.current_tabs_active_file_path = ""

        self.current_active_tabs = []

        # sidemenutabwindows initialization
        self.spliter_side_workspace_menu = Splitter(size_hint_x=.4, sizable_from="right", strip_size='3pt',
                                                    min_size="145dp",
                                                    max_size="450dp")
        self.spliter_side_workspace_menu.add_widget(SideMenuTabWindows())


    # side tabs state mananger if tab is opend or not
    def on_left_tab_state(self, instance):
        # print(instance.name, instance.state)
        side_tab_list = self.root.ids.tab_container.children
        # print(side_tab_list)

        if self.side_menu_open:
            if instance.state == "normal":
                self.root.ids.tab_container.remove_widget(self.root.ids.tab_container.children[1])
                self.side_menu_open = False

        else:
            if instance.state == "down":
                self.root.ids.tab_container.add_widget(self.spliter_side_workspace_menu, 1)
                self.side_menu_open = True

    def open_console_and_close(self, instance):
        from components.widgets.terminal_splitter import TerminalSplitter
        from components.terminal.py_terminal import Terminal
        terminal_splitter = TerminalSplitter()
        terminal_splitter.add_widget(Terminal())

        tab_and_console = self.root.ids.tab_and_consle_container
        # print(tab_and_console.children)

        if self.console_open:
            tab_and_console.remove_widget(tab_and_console.children[0])
            self.console_open = False
        else:
            tab_and_console.add_widget(terminal_splitter, 0)
            self.console_open = True

    # update cursor line and column
    def update_bottom_header_label_cursor_point(self, pos, selected_text):
        ln, col = pos
        self.root.ids.cursor_pos.text = f'Ln {ln + 1}, Col {col + 1}'

        if len(selected_text) > 0:
            self.root.ids.selected_text.text = f"{len(selected_text)} selected"
        else:
            self.root.ids.selected_text.text = ""

    # ================================================

    # windows files state manager selection on code tabs explorer
    def explorer_tabs(self, instance):
        from actions.file_type_checker import get_file_type
        filename = instance.file_and_folders_name
        path = instance.source_path
        filenameAndPath = {"file_name": filename, "file_path": path}
        if not os.path.isdir(path):
            # self.text_lang_tab(filenameAndPath)
            match get_file_type(path):
                case "Text_lang":
                    self.text_lang_tab(filenameAndPath)
                    # t1 = threading.Thread(target=self.thredign, args=[file_name, self.file_path])
                    # t1.start()
                    # asyncio.create_task(self.text_lang_tab(file_name, self.file_path))

                case "Video":
                    self.media_tab(filenameAndPath)
                case "Image":
                    self.image_tab(filenameAndPath)
        # --------------------------------------

    # opening file from chooser
    def open_file_from_header(self):
        # filechooser.open_file(on_selection=self.selected_files)
        from components.kivyfilechooser.file_chooser import ModalFileChooser
        Factory.ModalFileChooser().open()

    def selected_files(self, file_path):
        from actions.file_type_checker import get_file_type
        from actions.filepath_spliter import file_name_

        if len(file_path) != 0:
            self.file_path = file_path[0]
            self.title = f"CatxCode {self.file_path}"

            # file name and path form filepath in dict
            file_name_and_path_dict = file_name_(self.file_path)

            # adding to tabs by checking filetype
            match get_file_type(self.file_path):
                case "Text_lang":
                    self.text_lang_tab(file_name_and_path_dict)
                    # t1 = threading.Thread(target=self.thredign, args=[file_name, self.file_path])
                    # t1.start()
                    # asyncio.create_task(self.text_lang_tab(file_name, self.file_path))

                case "Video":
                    self.media_tab(file_name_and_path_dict)
                case "Image":
                    self.image_tab(file_name_and_path_dict)

    async def my_async_function(self, file_name_and_path_dict):
        print("woohooo running async function on kivy app")
        await self.text_lang_tab(file_name_and_path_dict)

    # def thredign(self,file_name, filepath):
    #     with open(filepath) as f:
    #         content = f.read()
    #     self.text_lang_tab(file_name, content)
    # @mainthread
    def text_lang_tab(self, file_name_and_path_dict):
        from components.codetabs.all_tabs import CustomTabs
        if file_name_and_path_dict["file_path"] not in self.current_active_tabs:
            with open(file_name_and_path_dict["file_path"]) as f:
                content = f.read()
            self.root.ids.all_tabs_bar.add_widget(
                CustomTabs(custom_tab_name=file_name_and_path_dict["file_name"], code_text=content,
                           file_path=file_name_and_path_dict["file_path"]))

            # appending file path to identify which tab is active and removed
            self.current_active_tabs.append(file_name_and_path_dict["file_path"])

        self.switch_to_current_tab(file_name_and_path_dict)

    def media_tab(self, file_name_and_path_dict):
        from components.codetabs.all_tabs import MediaTabs, ImageTabs
        self.root.ids.all_tabs_bar.add_widget(MediaTabs(media_tab_name=file_name_and_path_dict["file_name"],
                                                        media_source=file_name_and_path_dict["file_path"]))

        self.current_active_tabs.append(file_name_and_path_dict["file_path"])
        self.switch_to_current_tab(file_name_and_path_dict)

    def image_tab(self, file_name_and_path_dict):
        from components.codetabs.all_tabs import ImageTabs
        self.root.ids.all_tabs_bar.add_widget(ImageTabs(image_tab_name=file_name_and_path_dict["file_name"],
                                                        image_source=file_name_and_path_dict["file_path"]))

        self.current_active_tabs.append(file_name_and_path_dict["file_path"])
        self.switch_to_current_tab(file_name_and_path_dict)

    # def save_file(self, args):
    #     with open(self.file_path, "w") as f:
    #         f.write(self.textinput.text)

    # new tab creater from header
    def create_new_file_from_header(self):
        from components.codetabs.all_tabs import WelcomeTab
        welcome = WelcomeTab()
        welcome.create_new_file_popup()

    def save_text_file(self, file_name):
        with open(f"{storage_path}/{file_name}", "w"), open(f"{storage_path}/{file_name}") as f:
            s = f.read()
            n = s.splitlines()

        from components.codetabs.all_tabs import CustomTabs
        from components.codetabs.all_tabs import CodeLineCounter

        customtabs = CustomTabs()

        # code line counter
        for i in range(len(n)):
            customtabs.ids.code_line_counter_container.add_widget(CodeLineCounter(
                row_number_counter_for_code=i))

        # tab code
        print(file_name)
        self.root.ids.all_tabs_bar.add_widget(
            CustomTabs(custom_tab_name=file_name, code_text=s, file_path=f"{storage_path}/{file_name}"))

        self.switch_to_current_tab("file_name_and_path_dict")

    def switch_to_current_tab(self, file_name_and_path_dict):
        panel = self.root.ids.all_tabs_bar
        if panel.tab_list:
            # print(panel.tab_list[0].file_path)
            panel.switch_to(panel.tab_list[0])

    # close_tab
    def close_tab(self, instance, tab_id):
        self.root.ids.all_tabs_bar.remove_widget(tab_id)

        panel = self.root.ids.all_tabs_bar
        if panel.tab_list:
            panel.switch_to(panel.tab_list[0])
        else:
            panel.clear_widgets()

        # removing file path of closed tab
        self.current_active_tabs.remove(tab_id.file_path)

    # run code function
    def run_code(self):
        import subprocess
        from components.widgets.popup_console_output import ConsoleOutPutPopup
        from kivy.uix.popup import Popup
        compiler = None
        output = None

        popup = Popup(title='Console Output', title_color="green", title_size=18,
                      auto_dismiss=True, size_hint=(.7, .4), separator_color="purple",
                      background_color=(0, 0, 1, 1))

        compiler_selection = self.current_tabs_active_file_path.split(".")
        # print(compiler_selection)
        if compiler_selection[-1] == "js":
            compiler = "node"
        elif compiler_selection[-1] == "py":
            compiler = "python"
        try:

            if platform == "android":
                with open(self.current_tabs_active_file_path, mode="r", encoding="utf-8") as j:
                    code = j.read()
                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout
                exec(code, locals(), globals())
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
                # print(output)

                popup.content = ConsoleOutPutPopup(str(output))
                popup.open()

            else:
                output = subprocess.run([compiler, self.current_tabs_active_file_path], stdout=subprocess.PIPE,
                                        universal_newlines=True, text=True)

                popup.content = ConsoleOutPutPopup(str(output.stdout))
                popup.open()

        except Exception as e:
            print(type(e))
            popup.content = ConsoleOutPutPopup(str(e))
            popup.open()

    # this call coming from tabbed paned
    def _on_current_active_tabs(self, instance):
        try:
            # print(instance.ids.code_input.text, instance.file_path)
            self.current_tabs_active_code = instance.ids.code_input.text
            self.current_tabs_active_file_path = instance.file_path
        except BaseException as e:
            print(e)

    # save file from active tabs
    def save_active_file_from_header(self):
        if self.current_tabs_active_file_path:
            with open(self.current_tabs_active_file_path, "w") as f:
                f.write(self.current_tabs_active_code)

            from components.widgets.notify import Notify
            obj = Notify()

    def _current_tabs_active_code(self, code):
        self.current_tabs_active_code = code


asyncio.run(EditorApp().async_run('asyncio'))
