class MultilingualRessourceBase:
    TYPE_TMX = 'tmx'
    TYPE_AF = 'af'
    TYPE_BILINGUAL = 'bilingual'

    def __init__(self, type):
        self._multilingual_ressource_type = type

    def get_multilingual_ressource_type(self):
        return self._multilingual_ressource_type
    multilingual_ressource_type = property(get_multilingual_ressource_type)