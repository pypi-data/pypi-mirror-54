# -*- coding: utf-8 -*-

from benedict.utils import io_util

from six import string_types, text_type


class IODict(dict):

    def __init__(self, *args, **kwargs):
        # if first argument is data-string,
        # try to decode it using all decoders.
        if len(args) and isinstance(args[0], string_types):
            d = IODict._from_any_data_string(args[0], **kwargs)
            if d and isinstance(d, dict):
                args = list(args)
                args[0] = d
                args = tuple(args)
            else:
                raise ValueError('Invalid string data input.')
        super(IODict, self).__init__(*args, **kwargs)

    @staticmethod
    def _decode(s, decoder, **kwargs):
        d = None
        try:
            content = io_util.read_content(s)
            # decode content using the given decoder
            data = decoder(content, **kwargs)
            if isinstance(data, dict):
                d = data
            elif isinstance(data, list):
                # force list to dict
                d = { 'values':data }
            else:
                raise ValueError(
                    'Invalid data type: {}, expected dict or list.'.format(type(data)))
        except Exception as e:
            raise ValueError(
                'Invalid data or url or filepath input argument: {}\n{}'.format(s, text_type(e)))
        return d

    @staticmethod
    def _encode(d, encoder, filepath=None, **kwargs):
        s = encoder(d, **kwargs)
        if filepath:
            io_util.write_file(filepath, s)
        return s

    @staticmethod
    def _from_any_data_string(s, **kwargs):
        funcs = [
            IODict.from_base64,
            IODict.from_json,
            IODict.from_query_string,
            IODict.from_toml,
            IODict.from_xml,
            IODict.from_yaml,
        ]
        for f in funcs:
            try:
                options = kwargs.copy()
                d = f(s, **options)
                return d
            except ValueError:
                pass

    @staticmethod
    def from_base64(s, format='json', encoding='utf-8', **kwargs):
        kwargs['format'] = format
        kwargs['encoding'] = encoding
        return IODict._decode(s,
            decoder=io_util.decode_base64, **kwargs)

    @staticmethod
    def from_csv(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_csv, **kwargs)

    @staticmethod
    def from_json(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_json, **kwargs)

    @staticmethod
    def from_query_string(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_query_string, **kwargs)

    @staticmethod
    def from_toml(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_toml, **kwargs)

    @staticmethod
    def from_xml(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_xml, **kwargs)

    @staticmethod
    def from_yaml(s, **kwargs):
        return IODict._decode(s,
            decoder=io_util.decode_yaml, **kwargs)

    def to_base64(self, filepath=None, format='json', encoding='utf-8', **kwargs):
        kwargs['format'] = format
        kwargs['encoding'] = encoding
        return IODict._encode(self,
            encoder=io_util.encode_base64,
            filepath=filepath, **kwargs)

    def to_json(self, filepath=None, **kwargs):
        return IODict._encode(self,
            encoder=io_util.encode_json,
            filepath=filepath, **kwargs)

    def to_query_string(self, filepath=None, **kwargs):
        return IODict._encode(self,
            encoder=io_util.encode_query_string,
            filepath=filepath, **kwargs)

    def to_toml(self, filepath=None, **kwargs):
        return IODict._encode(self,
            encoder=io_util.encode_toml,
            filepath=filepath, **kwargs)

    def to_xml(self, filepath=None, **kwargs):
        return IODict._encode(self,
            encoder=io_util.encode_xml,
            filepath=filepath, **kwargs)

    def to_yaml(self, filepath=None, **kwargs):
        return IODict._encode(self,
            encoder=io_util.encode_yaml,
            filepath=filepath, **kwargs)
