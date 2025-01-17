from intake.catalog.local import Catalog, DataSource, LocalCatalogEntry
from intake.container import container_map

class MyDriver(DataSource):

    def __init__(self, shape, color, **kwargs):
        self._shape = args['shape']
        self._color = args['color']
        super().__init__(**kwargs)

    def _get_partition(self, partition):
        print('fetching data for {(self._shape, self_color)}')
        print("PARTITION", partition)
        return self._shape, self._color


class InnerCatalog(Catalog):

    def __init__(self, shape, **kwargs):
        self._shape = shape
        super().__init__(*args, **kwargs)

    def _load(self):
        print(f'loaded inner catalog for {self._shape}')
        for color in ('red', 'green', 'blue'):
            self._entries[color] = LocalCatalogEntry(
                name=color,
                driver='remote_test.cat.MyDriver',
                description='',
                catalog=self,
                args={'shape': self._shape, 'color': color})

    def read_partition(self, partition):
        print(partition['index'])


class OuterCatalog(Catalog):

    def _load(self):
        for shape in ('circle', 'square', 'triangle'):
            self._entries[shape] = LocalCatalogEntry(
                name=shape,
                driver='remote_test.cat.InnerCatalog',
                description='',
                catalog=self,
                args={'shape': shape})

    def read_partition(self, partition):
        print(partition['index'])
