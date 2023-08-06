import numpy as np
import operator
# noinspection PyUnresolvedReferences
from lxml import etree
from pprint import pformat
from typing import Dict, List, Any, Union, Tuple


class DataFrame:
    """
    Класс датафрейма для хранения и обработки таблиц из .xml документов.
    Структура датафрейма:
        data: np.array((nrows, ncols)) - таблица пользовательских данных. ncols - число граф в соответствующей
            секции проверочной схемы, nrows - число строк в соответствующей секции пользовательского файла.
        specs: np.array((nrows, 3)) - таблица специфик. s1 - 0 столбец, s2 - 1 столбец, s3 - 2 столбец.
        row_codes: np.array(nrows) - вектор кодов строк в соответствии с проверочным файлом.
        col_codes: np.array(ncols) - вектор кодов граф в соответствии с проверочным файлом.
        #col_map: Dict[str, int] - отображение вида {код_графы: индекс_графы_в_col_codes}.

                    col_codes   [][][][]
        s1s2s3      row_codes
        [][][]      []          [][][][]
        [][][]      []          [ data ]
        [][][]      []          [][][][]
    """
    op_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '<': operator.lt,
        '<=': operator.le,
        '=': operator.eq,
        '>': operator.gt,
        '>=': operator.ge,
        '!=': operator.ne,
    }

    def __init__(self, *
                 data: np.array,
                 specs: np.array,
                 row_codes: np.array,
                 col_codes: np.array) -> None:
        self.data = data
        self.specs = specs
        self.row_codes = row_codes
        self.col_codes = col_codes

        # Словарь для сторокового представления внутренней структуры
        self.struct = {
            'data':         self.data,
            'specs':        self.specs,
            'row_codes':    self.row_codes,
            'col_codes':    self.col_codes
        }

    def __str__(self):
        return pformat(self.struct)

    def __add__(self, other):
        return self._op(other, '+')

    def __sub__(self, other):
        return self._op(other, '-')

    def __mul__(self, other):
        return self._op(other, '*')

    def __truediv__(self, other):
        return self._op(other, '/')

    def __gt__(self, other):
        return self._boolop(other, '>')

    def __ge__(self, other):
        return self._boolop(other, '>=')

    def __lt__(self, other):
        return self._boolop(other, '<')

    def __le__(self, other):
        return self._boolop(other, '<=')

    def __eq__(self, other):
        return self._boolop(other, '=')

    def __ne__(self, other):
        return self._boolop(other, '!=')

    def _op(self, other: Union['DataFrame', float], op: str) -> 'DataFrame':
        """ Вспомогательный метод для перегрузки операторов. """
        if type(other) == DataFrame:
            data = DataFrame.op_map[op](self.data, other.data)
        elif type(other) == float:
            data = DataFrame.op_map[op](self.data, other)
        else:
            raise Exception(f'Невалидный аргумент для операции {op}: {other}')

        return DataFrame(data=data,
                         specs=self.specs,
                         row_codes=self.row_codes,
                         col_codes=self.col_codes)

    def _boolop(self, other: Union['DataFrame', float], op: str) -> bool:
        """ Вспомогательный метод для перегрузки булевых операций. """
        if type(other) == DataFrame:
            mask = DataFrame.op_map[op](self.data, other.data)
        elif type(other) == float:
            mask = DataFrame.op_map[op](self.data, other)
        else:
            raise Exception(f'Невалидный аргумент для операции {op}: {other}')

        return mask.all()

    @staticmethod
    def from_file_content(xml_section: etree.ElementTree, scheme_section: Dict[str, Any]) -> 'DataFrame':
        """
        Инициализирует датафрейм по содержимому пользовательского файла.
        :param xml_section: соответствующая секция в пользовательском файле.
        :param scheme_section: соответствующая секция в объекте компендиума.
        :return: инициализированный экземпляр DataFrame.
        """
        # Отображение колонок-специфик на индексы в массиве specs
        spec_map = {'s1': 0, 's2': 1, 's3': 2}
        scheme_columns = scheme_section['columns']

        rows = xml_section.xpath('.//row')
        nrows = len(rows)
        ncols = len(scheme_columns.keys())

        # Векторы строк и колонок
        row_codes = np.zeros(nrows)
        col_codes = np.zeros(ncols)
        for code, item in scheme_section['columns'].items():
            col_codes[item['index']] = code

        # Основная таблица данных для валидации
        data = np.zeros((nrows, ncols))
        # Таблица специфик
        specs = np.zeros((nrows, 3), dtype='U')

        for rx, row in enumerate(rows):
            row_code = int(row.attrib['code'])
            row_codes[rx] = row_code

            # Заполенение массива специфик
            for attrib, value in row.attrib.items():
                if attrib != 'code':
                    sx = spec_map.get(attrib)
                    if sx is None:
                        # TODO: internal exceptions
                        raise Exception('Неверный атрибут элемента "row"')
                    specs[rx, sx] = value.lower()

            # Заполнение основного массива данных data
            cols = row.xpath('.//col')
            for col in cols:
                cx = scheme_columns[col.attrib['code']]
                # TODO: default value?
                data[rx, cx] = col.text or 0

        return DataFrame(data=data,
                         specs=specs,
                         row_codes=row_codes,
                         col_codes=col_codes)

    def dim(self) -> Tuple[int, int]:
        """ Метод для определения размерности массива данных self.data. """
        return self.data.shape

    def get(self, rows: List[int], cols: List[int], *specs: List[int]) -> 'DataFrame':
        """
        Метод для получения выборки из датафрейма по заданным спискам строк, граф и специфик.
        :param rows: список строк.
        :param cols: список граф.
        :param specs: списки специфик. Может содержать от 0 до 3 списков:
            0 - специфики отсутствуют (одиночные строки типа 'F');
            1-3 - соответствующие списки специфик s1-s3.
        :return: отфильрованный объект DataFrame.
        """
        # Получение маски индексов удовлетворяющих специфик
        if any(specs):
            # Список логических условий для фильтрации специфик в self.specs
            conditions = []
            for sx, spec in enumerate(specs):
                conditions.append(np.in1d(self.specs[:, sx], spec))
            spec_mask = np.logical_and.reduce(*conditions)
        else:
            spec_mask = np.full(self.row_codes.shape[0], True)

        # Получение масок индексов удовлетворяющих строк/граф
        row_mask = np.logical_and(spec_mask, np.in1d(self.row_codes, rows))
        col_mask = np.in1d(self.col_codes, cols)

        # Фильтруем массив data по векторам row_codes/col_codes
        grid = np.ix_(row_mask, col_mask)

        return DataFrame(data=self.data[grid],
                         specs=self.specs[row_mask, :],
                         row_codes=self.row_codes[row_mask],
                         col_codes=self.col_codes[col_mask])

    def sum(self, *, axis: int=0) -> Union['DataFrame', float]:
        """
        Выполняет сложение элементов таблицы section вдоль оси axis:
            0 - по столбцам,
            1 - по строкам,
            2 - во всей таблице.
        Возвращает объект DataFrame, если сложение производится по строкам/столбцам,
        или скаляр, если сложение производится по всему датафрейму.
        """
        if axis == 2:
            return np.nansum(self.data)

        data = np.nansum(self.data, axis=axis, keepdims=True)
        return DataFrame(data=data,
                         specs=self.specs,
                         row_codes=self.row_codes,
                         col_codes=self.col_codes)
