from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.text import LabelBase
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import pandas as pd


class ScrollableTable(ScrollView):
    def __init__(self, table_data, **kwargs):
        super(ScrollableTable, self).__init__(**kwargs)

        # Create a GridLayout to hold the table data
        grid = GridLayout(cols=3, spacing=[0, 2], size_hint_y=None)

        # Add a label for each row in the table data
        for row in table_data.split('\n'):
            for item in row.split('\t'):
                grid.add_widget(Label(text=item, size_hint_y=None, height=40))

        # Set the height of the GridLayout based on its content
        grid.bind(minimum_height=grid.setter('height'))

        # Add the GridLayout to the ScrollView
        self.add_widget(grid)


class VitaminApp(App):
    def build(self):
        LabelBase.register('CustomFont', fn_regular='6.ttf')
        LabelBase.register('CustomFont_2', fn_regular='1.ttf')
        LabelBase.register('CustomFont_3', fn_regular='2.ttf')
        LabelBase.register('CustomFont_4', fn_regular='3.ttf')
    
        tab_panel = TabbedPanel(do_default_tab=False)
        tab_panel.default_tab_text = 'Калькулятор'

        # Вкладка для калькулятора
        calculator_tab = TabbedPanelItem(text='Калькулятор')
        calculator_tab.add_widget(self.build_calculator())
        tab_panel.add_widget(calculator_tab)

        # Вкладка для таблицы с данными о фрукте
        fruit_tab = TabbedPanelItem(text='Таблица')
        fruit_tab.add_widget(self.build_table())
        tab_panel.add_widget(fruit_tab)

        # Вкладка для статьи
        article_tab = TabbedPanelItem(text='Статья')
        article_tab.add_widget(Label(text='Статья будет здесь', font_size=20))
        tab_panel.add_widget(article_tab)

        # Вкладка для соцсетей
        social_tab = TabbedPanelItem(text='Соцсети')
        social_tab.add_widget(Label(text='Соцсети будут здесь', font_size=20))
        tab_panel.add_widget(social_tab)

        return tab_panel

    def build_table(self):
        data_layout = FloatLayout()

        # Read data from Excel file
        df = pd.read_excel('example.xlsx')

        # Format data into a string including column names
        table_data = "\n".join([f'{i + 1}\t{row[1]}\t{row[2]}' for i, row in enumerate(df.itertuples(index=False))])

        # Display data in a scrollable table
        table_layout = ScrollableTable(table_data, size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        Window.bind(on_resize=self.on_window_resize_table)

        data_layout.add_widget(table_layout)

        return data_layout

    def on_window_resize_table(self, window, width, height):
        if min(width, height) < 500:
            message_label = Label(text='Пожалуйста, переверните телефон', font_size='20sp', font_name='CustomFont_4', color=(1, 0, 0, 1), size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'y': 10})
            self.build_table().add_widget(message_label)
        else:
            message_label = [widget for widget in self.build_table().children if isinstance(widget, Label) and widget.text == 'Пожалуйста, переверните телефон']
            if message_label:
                self.build_table().remove_widget(message_label[0])


    def build_calculator(self):
        main_layout = FloatLayout()

        background = Image(source='image.png', allow_stretch=True, keep_ratio=False)
        main_layout.add_widget(background)

        item_label = Label(text='Выбрать продукт', size_hint=(None, None), size=(150, 30), font_name='CustomFont', font_size='20sp', pos_hint={'center_x': 0.5, 'top': 0.8})
        main_layout.add_widget(item_label)

        item_spinner = Spinner(text='Не указано', values=('Апельсины', 'Лимоны', 'Киви'), size_hint=(0.5, 0.1), font_name='CustomFont_4', color=(1, 0, 0, 1), font_size='20sp', pos_hint={'center_x': 0.5, 'top': 0.75},
                                  background_color=[1, 1, 1, 0.5], background_normal='', background_down='')
        main_layout.add_widget(item_spinner)
        self.item_spinner = item_spinner  # Assigning the spinner to an id

        self.gram_input = RoundedTextInput(multiline=False, input_type='number', input_filter='float', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.6}, hint_text='Введите количество грамм', foreground_color=(0, 0, 0, 1))
        main_layout.add_widget(self.gram_input)

        calculate_button = RoundedButton(text='Рассчитать', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.4},
                                  background_color=[1, 1, 1, 0.5], background_normal='', background_down='')
        calculate_button.bind(on_release=self.calculate_vitamin_c)
        main_layout.add_widget(calculate_button)

        self.vitamin_c_label = Label(text='', size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5, 'top': 0.2}, color=[0, 0, 0, 1])
        main_layout.add_widget(self.vitamin_c_label)

        self.vitamin_c_bg = RoundedRectangle(pos=self.vitamin_c_label.pos, size=self.vitamin_c_label.size, radius=[10,])
        main_layout.canvas.before.add(Color(0.8, 0.8, 0.8, 1))
        main_layout.canvas.before.add(self.vitamin_c_bg)

        return main_layout

    def calculate_vitamin_c(self, instance):
        try:
            grams = float(self.gram_input.text)
        except ValueError:
            grams = 0
        items_vitamin_c = {'Апельсины': 53, 'Лимоны': 53, 'Киви': 92}
        selected_item = self.item_spinner.text
        item_vitamin_c = items_vitamin_c.get(selected_item, 0)
        if grams > 0:
            total_vitamin_c = round(item_vitamin_c * (grams / 100), 2)  # Округляем до двух знаков после запятой
            self.vitamin_c_label.text = f'Количество витамина C: {total_vitamin_c} мг'
            self.vitamin_c_label.color = [1, 1, 1, 1]
        else:
            self.vitamin_c_label.text = ''
        self.gram_input.text = ''


    def update_vitamin_c_bg(self):
        if self.vitamin_c_label.text:
            if self.vitamin_c_bg not in self.vitamin_c_label.canvas.before.children:
                self.vitamin_c_label.canvas.before.add(self.vitamin_c_bg)
        else:
            if self.vitamin_c_bg in self.vitamin_c_label.canvas.before.children:
                self.vitamin_c_label.canvas.before.remove(self.vitamin_c_bg)


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = [0, 0, 0, 0]
        with self.canvas.before:
            Color(1, 1, 1, 0.5)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(RoundedTextInput, self).__init__(**kwargs)
        self.background_color = [0, 0, 0, 0]
        with self.canvas.before:
            Color(1, 1, 1, 0.5)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10,])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


if __name__ == '__main__':
    VitaminApp().run()
