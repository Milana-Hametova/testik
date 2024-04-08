from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.base import runTouchApp

kv = """
<RoundedButton@Button>:
    background_color: 0, 0, 0, 0  # делаем кнопку невидимой
    canvas.before:
        Color:
            rgba: (.4, .4, .4, 1) if self.state == 'normal' else (0, .7, .7, 1)  # визуальная обратная связь при нажатии
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]  # устанавливаем радиус скругления краев кнопки
"""

class RoundedButton(Button):
    pass

Builder.load_string(kv)
runTouchApp(RoundedButton(text="Нажми меня!"))


а теперь по этому коду, не меняя размера кнопок закругли края у кнопок и полей в кода:

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.text import LabelBase


class VitaminApp(App):
    def build(self):

        LabelBase.register('CustomFont', fn_regular='6.ttf')
        LabelBase.register('CustomFont_2', fn_regular='1.ttf')
        LabelBase.register('CustomFont_3', fn_regular='2.ttf')
        LabelBase.register('CustomFont_4', fn_regular='3.ttf')

        # Основной контейнер
        main_layout = FloatLayout()

        # Фоновое изображение
        background = Image(source='image.png', allow_stretch=True, keep_ratio=False)
        main_layout.add_widget(background)

        # Надпись "Выбрать продукт"
        item_label = Label(text='Выбрать продукт', size_hint=(None, None), size=(150, 30), font_name='CustomFont', font_size='20sp', pos_hint={'center_x': 0.5, 'top': 0.8})
        main_layout.add_widget(item_label)

        # Кнопка для отображения списка предметов
        self.item_button = Button(text='Не указано', size_hint=(0.5, 0.1), font_name='CustomFont_4', color=(1, 0, 0, 1), font_size='20sp', pos_hint={'center_x': 0.5, 'top': 0.75},
                                  background_color=[1, 1, 1, 0.5], background_normal='', background_down='')
        self.item_button.bind(on_release=self.show_items)
        main_layout.add_widget(self.item_button)
        
        # Текстовое поле для ввода количества грамм продукта
        self.gram_input = TextInput(multiline=False, input_type='number', input_filter='float', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.6},
                                    hint_text='Введите количество грамм', background_color=[0.8, 0.8, 0.8, 1])
        main_layout.add_widget(self.gram_input)

        # Кнопка для расчета количества витамина С
        calculate_button = Button(text='Рассчитать', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.4},
                                  background_color=[1, 1, 1, 0.5], background_normal='', background_down='')
        calculate_button.bind(on_release=self.calculate_vitamin_c)
        main_layout.add_widget(calculate_button)

        # Надпись о количестве витамина C (пока скрыта)
        self.vitamin_c_label = Label(text='', size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5, 'top': 0.2}, color=[0, 0, 0, 1])
        main_layout.add_widget(self.vitamin_c_label)

        # Устанавливаем апельсин по умолчанию
        self.selected_item = 'Апельсин'

        return main_layout

    def show_items(self, instance):
        # Создание списка предметов и их содержания витамина C
        content = FloatLayout()

        items = {'Апельсины': 53, 'Лимоны': 53, 'Киви': 92}  # Пример данных
        y_pos = 0.9
        for item, vitamin_c in items.items():
            button = Button(text=f'{item}', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': y_pos},
                            background_color=[1, 1, 1, 0.5], background_normal='', background_down='')
            button.bind(on_release=self.select_item)
            content.add_widget(button)
            y_pos -= 0.1

        self.popup = Popup(title='Список продуктов', content=content, size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def select_item(self, instance):
        # Обработка выбора продукта
        selected_item = instance.text
        self.item_button.text = selected_item
        self.selected_item = selected_item
        self.popup.dismiss()

    def calculate_vitamin_c(self, instance):
        # Расчет количества витамина C в зависимости от выбранного продукта и введенного количества грамм
        try:
            grams = float(self.gram_input.text)
        except ValueError:
            grams = 0
        items_vitamin_c = {'Апельсины': 53, 'Лимоны': 53, 'Киви': 92}  # Пример данных
        item_vitamin_c = items_vitamin_c.get(self.selected_item, 0)
        if grams > 0:
            total_vitamin_c = item_vitamin_c * (grams / 100)
            self.vitamin_c_label.text = f'Количество витамина C: {total_vitamin_c} мг'
            self.vitamin_c_label.color = [0, 0, 0, 1]  # Делаем видимой надпись о количестве витамина C
        else:
            self.vitamin_c_label.text = ''  # Если граммы не указаны, скрываем надпись о количестве витамина C
        self.gram_input.text = ''  # Очищаем текстовое поле после расчета


if __name__ == '__main__':
    VitaminApp().run()