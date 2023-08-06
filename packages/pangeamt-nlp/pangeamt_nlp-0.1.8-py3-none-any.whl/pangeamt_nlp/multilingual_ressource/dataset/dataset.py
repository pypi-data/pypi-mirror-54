import glob
import os
from pangeamt_nlp.utils.chunk_list import chunk_list
from pangeamt_nlp.multilingual_ressource import Tmx
from pangeamt_nlp.multilingual_ressource import Af
from pangeamt_nlp.multilingual_ressource import Bilingual
from pangeamt_nlp.multilingual_ressource.multilingual_ressource_base import MultilingualRessourceBase
from pangeamt_nlp.multilingual_ressource.dataset.dataset_reader import DatasetReader

class Dataset:
    def __init__(self, dir:str):
        self._dir = dir
        if not os.path.isdir(dir):
            raise ValueError(f"Dataset dir {dir} doesn't exists")
        self._ressources = []
        self._explore()

    def _explore(self):
        # Tmx
        tmxs = glob.glob(self._dir + '/*.tmx')
        for tmx in tmxs:
            self._ressources.append(Tmx(tmx))
        # afs
        afs = glob.glob(self._dir + '/*.af')
        for af in afs:
            self._ressources.append(Af(af))

        files = glob.glob(self._dir + '/*')
        potential_bilinguals = []
        for f in files:
            if not f.endswith('.af') and not f.endswith('.tmx'): #TODO .af could  correspond to Afrikaans language
                potential_bilinguals.append(f)

        potential_bilinguals.sort()
        for pair in chunk_list(potential_bilinguals, 2):
            if len(pair) != 2:
                raise ValueError(f'bilingual pair is missing in {self._dir}')
            file_1 = pair[0]
            file_2 = pair[1]
            base_1, ext_1 = os.path.splitext(file_1)
            base_2, ext_2 = os.path.splitext(file_2)
            if base_1 != base_2:
                raise ValueError(f'bilingual pair is missing in {self._dir}')
            else:
                bilingual = Bilingual(file_1, file_2)
                self._ressources.append(bilingual)

    def get_ressources(self):
        return self._ressources
    ressources = property(get_ressources)


    def read(self, reader: DatasetReader):
        for ressource in self._ressources:
            current_reader = None
            if ressource.multilingual_ressource_type == MultilingualRessourceBase.TYPE_TMX:
                current_reader = reader.tmx_reader
            elif ressource.multilingual_ressource_type == MultilingualRessourceBase.TYPE_AF:
                current_reader = reader.af_reader
            elif ressource.multilingual_ressource_type == MultilingualRessourceBase.TYPE_BILINGUAL:
                current_reader = reader.bilingual_reader

            if current_reader is None:
                raise ValueError("Invalid reader") #TODO
            yield from ressource.read(current_reader)