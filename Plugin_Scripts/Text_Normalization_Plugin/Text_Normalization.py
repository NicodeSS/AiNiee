from ..Plugin_Base.Plugin_Base import PluginBase

import jaconv # 日文文本转换工具
import unicodedata


class Text_Normalization_Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.name = "Text_Normalization_Plugin"
        self.description = "This is an Text_Normalization_Plugin."
        self.add_event('normalize_text', 5)  # 添加感兴趣的事件和优先级


    def load(self):
        print(f"[INFO]  {self.name} loaded!")


    def on_event(self, event_name, configuration_information, event_data):

        # 事件触发
        if event_name == "normalize_text":

            # 将半角（半角假名）片假名转换为全角（全角假名）片假名
            # 全角（全角）ASCII字符和数字转换为半角（半角）ASCII字符和数字。
            # 此外，全角波浪号（～）等也被规范化。
            if configuration_information.source_language == "日语":
                for k in event_data.keys():
                    text = jaconv.normalize(event_data.get(k, ""), mode = "NFKC")
                    text = self.remove_spaces(text)
                    event_data[k] = text

            if configuration_information.source_language == "英语":
                for k in event_data.keys():
                    text = unicodedata.normalize('NFKC', event_data.get(k, ""))
                    text = self.remove_spaces(text)
                    event_data[k] = text



    def remove_spaces(self, text):
        """
        Remove both full-width and half-width spaces from the input text.
        """
        # Full-width space character
        full_width_space = '　'
        # Half-width space character
        half_width_space = ' '

        # Remove full-width spaces
        text = text.replace(full_width_space, '')
        # Remove half-width spaces
        text = text.replace(half_width_space, '')

        return text