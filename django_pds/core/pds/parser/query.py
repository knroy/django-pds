import json
import re

from mongoengine import Q

from django_pds.core.helper.xstr import xstr
from .terms import WHERE, SELECT, EQUAL, LT, GT, AND, OR, EMPTY, COMMA, FILTER, PARENTHESIS_LEFT, PARENTHESIS_RIGHT, \
    ORDER_BY, RAW_WHERE

REGEX = r'\(|\)|\w+=[\w+|\-*|\d*|\:*|\.*|\ *|\,*|\'*|\%*]*|\&+|\@+'

REGEX_STRING_QUERY = ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith',
                      'endswith', 'iendswith', 'match']

REPLACE_DICT = {
    '%3D': '=',
    '%2B': '+',
    '%2F': '/',
    '%20': ' ',
    '%25': '%'
}


class QueryParser:
    __raw = {}

    def __init__(self, text):
        self.text = text

    def __count_lt_gt(self):
        cnt_lt = self.text.count(LT)
        cnt_gt = self.text.count(GT)
        return cnt_lt == cnt_gt

    def __count_parenthesis(self):
        cnt_lp = self.text.count(PARENTHESIS_LEFT)
        cnt_rp = self.text.count(PARENTHESIS_RIGHT)
        return cnt_lp == cnt_rp

    def validate(self):
        if not self.__count_lt_gt():
            raise Exception('Your SQL missing some < / >')
        if not self.__count_parenthesis():
            raise Exception('Your SQL missing some ( / )')

    def find(self, string, ch):
        pos = []
        ln = len(string)
        for i in range(ln):
            if string[i] in ch:
                pos.append(i)
        return pos

    def replacer(self, clause):
        data = ''
        for i in range(len(clause)):
            if clause[i] == '|':
                data = data + '@'
            elif clause[i] == '@':
                data = data + '|'
            else:
                data = data + clause[i]
        return data

    def reverse_replacer(self, clause):
        return self.replacer(clause)

    def deconstruct_select(self, clause):
        fields = clause.split(COMMA)
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
        return fields

    def make_tree(self, data):
        items = re.findall(REGEX, data)

        def req(index):
            result = []
            item = items[index]
            while item != ")":
                if item == "(":
                    subtree, index = req(index + 1)
                    result.append(subtree)
                else:
                    result.append(item)
                index += 1
                item = items[index]
            return result, index

        return req(1)[0]

    def equal_splitter(self, clause):
        items = clause.split("=")
        return items[0], xstr(items[1]).get()

    def print_dumps(self, dictionary):
        y = json.dumps(dictionary, indent=4, sort_keys=True)
        print(y)

    def making_q(self, tree, _filter, q, start, position=None):
        if position:
            subtree = tree[start:position]
        else:
            subtree = tree[start:]
        if len(subtree) > 1:
            return None
        if isinstance(subtree[0], list):
            sub_q = self.construct_q(subtree[0], _filter)
            if sub_q and start == 0:
                q = sub_q
            elif sub_q and tree[start - 1] == OR:
                q = q.__or__(sub_q)
            elif sub_q and tree[start - 1] == AND:
                q = q.__and__(sub_q)
        else:
            key, value = self.equal_splitter(subtree[0])
            keys = key.strip().rsplit("__", 1)
            _filter.append(keys[0].strip())
            for replace_with in REPLACE_DICT:
                value = value.replace(replace_with, REPLACE_DICT.get(replace_with))
            if len(keys) > 1:
                if keys[1] in REGEX_STRING_QUERY:
                    value = str(value)
            value = self.replacer(value)
            self.__raw[keys[0].strip()] = value
            _pair = {key.strip(): value}
            if start == 0:
                q = Q(**_pair)
            else:
                if tree[start - 1] == AND:
                    q = q.__and__(Q(**_pair))
                elif tree[start - 1] == OR:
                    q = q.__or__(Q(**_pair))

        return q

    def construct_q(self, tree, _filter):
        operators = ['&', '@']
        positions = list(self.find(tree, operators))
        start = 0
        q = Q()
        for position in positions:
            q = self.making_q(tree, _filter, q, start, position)
            start = position + 1
        q = self.making_q(tree, _filter, q, start)
        return q

    def deconstruct_deep_where(self, clause):
        if not clause.endswith(")") or not clause.startswith("("):
            clause = "(" + clause + ")"
        tree = self.make_tree(clause)
        _filter = []
        q = self.construct_q(tree, _filter)
        return _filter, q

    def parse(self):
        self.validate()
        splits = self.text.split(GT)
        dictionary = {}
        for keyword in splits:
            keywords = keyword.split(LT)

            if len(keywords) == 2:
                key = keywords[0].strip()
                key = key.replace(EQUAL, EMPTY)
                at = xstr(keywords[1].strip())
                dictionary[key.lower()] = at.get()

        if dictionary.get(ORDER_BY, None):
            clause = dictionary[ORDER_BY]
            data = []
            items = clause.split(',')
            for item in items:
                data.append(item.strip())
            dictionary[ORDER_BY] = data

        if dictionary.get(SELECT, None):
            dictionary[SELECT] = self.deconstruct_select(dictionary[SELECT])
        if dictionary.get(WHERE, None):
            clause = self.replacer(dictionary[WHERE])
            # pre-caution
            # or operator replaced with @ because | doesn't work
            # with regex that well
            _filters, _where = self.deconstruct_deep_where(clause)
            dictionary[WHERE] = _where
            dictionary[FILTER] = _filters
            dictionary[RAW_WHERE] = self.__raw
        return dictionary
