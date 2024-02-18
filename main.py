from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.label import Label
# from kivy.uix.filechooser import FileChooser
from kivy.core.window import Window
from plyer import filechooser
from kivy.app import App


class EditorApp(App):
    def build(self):
        # front ui
        self.title = "CodeEditor"
        self.icon = "assets/icons/icon-x.jpg"

        return Builder.load_file("main.kv")

    # code logic
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None

    def open_file_from_header(self):
        filechooser.open_file(on_selection=self.selected_files)

    def selected_files(self, file_path):
        from components.codetabs.all_tabs import CustomTabs, HeaderForTabs

        if len(file_path) != 0:
            self.file_path = file_path[0]
            self.title += f" {self.file_path}"
            file_name = self.file_path.split("\\")
            with open(self.file_path) as f:
                s = f.read()

            ch = HeaderForTabs(custom_tab_name=f'{file_name[-1]} [ref=s]X[/ref]',
                             action=self.close_tabsT)
            ch.content = CustomTabs(code_text=s)
            self.root.ids.all_tabs_bar.add_widget(ch)

    def close_tabsT(self, obj, ref):
        print('close pressed', ref)
        self.root.ids.all_tabs_bar.remove_widget(obj.parent)
        # self.switch_to(self.tab_list[-1])

        # self.root.ids.all_tabs_bar.add_widget(CustomTabs(custom_tab_name=file_name[-1], code_text=s))

    # def save_file(self, args):
    #     with open(self.file_path, "w") as f:
    #         f.write(self.textinput.text)

    # new tab creater from header
    def create_new_file_from_header(self):
        from components.codetabs.all_tabs import WelcomeTab
        welcome = WelcomeTab()
        welcome.create_new_file_popup()

    def save_text_file(self, file_name):
        with open("code.js", "r") as f:
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
        self.root.ids.all_tabs_bar.add_widget(CustomTabs(custom_tab_name=file_name, code_text=s))

        panel = self.root.ids.all_tabs_bar
        if panel.tab_list:
            panel.switch_to(panel.tab_list[0])

    # close_tab
    def close_tab(self, instance, tab_id):
        self.root.ids.all_tabs_bar.remove_widget(tab_id)
        panel = self.root.ids.all_tabs_bar
        if panel.tab_list:
            panel.switch_to(panel.tab_list[0])
        else:
            panel.clear_widgets()


    # run code function
    def run_code(self):
        import subprocess
        from kivy.uix.popup import Popup

        engine_selection = self.file_path.split(".")
        print(engine_selection)
        if engine_selection[-1] == "js":
            self.engine = "node"
        elif engine_selection[-1] == "py":
            self.engine = "python"
        try:
            co = subprocess.run([self.engine, self.file_path])
            f = Label(text=str(co))
            self.popup = Popup(title='Console Output', title_color="green", title_size=18, content=f,
                               auto_dismiss=True, size_hint=(.45, .21), separator_color="purple",
                               background_color=(0, 0, 1, 1))
        except Exception as e:
            print(type(e))
            l = Label(text=str(e))
            self.popup = Popup(title='Console Output', title_color="blue", title_size=18, content=l,
                               auto_dismiss=True, size_hint=(.45, .21), separator_color="purple",
                               background_color=(0, 0, 1, 1))

        self.popup.open()


EditorApp().run()
