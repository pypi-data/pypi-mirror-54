My white 🐳 is literate markdown programming in the notebook.

I have made so many attempts at a literate interface to the notebook.  Each of these experiments revealed important features of modern [literate ~~programming~~ computing](http://blog.fperez.org/2013/04/literate-computing-and-computational.html).

I've drawn the concept in packages & single notebooks.  In retrospect, they contain too many opinions to be extensible.  

Here is another go at it.


```python
    import re, textwrap, tokenize, io, itertools, IPython; from toolz.curried import *
    __all__ = 'parse',
```

Use the `mistune` to `parse` block level markdown objects.


```python
    class Lexer(__import__('mistune').BlockLexer):
        def parse(self, text, rules=None):
            text = ''.join(x if x.strip() else "\n" for x in text.splitlines(True))
            rules = rules or self.default_rules
            def manipulate(text):
                for key in rules:
                    m = getattr(self.rules, key).match(text)
                    if m: getattr(self, 'parse_%s' % key)(m); return m
                return False  
            while text:
                m = manipulate(text)
                if m: text = text[len(m.group(0)):]
                if not m and text: raise RuntimeError('Infinite loop at: %s' % text)
                if self.tokens: self.tokens[-1]['match'] = m
            return self.tokens
```


```python
    def quote(str, prior="", tick='"""'):
        """wrap a block of text in quotes. """
        if not str.strip(): return str
        indent, outdent = len(str)-len(str.lstrip()), len(str.rstrip())
        if tick in str or str.endswith(tick[0]): tick = '"""'
        return str[:indent] + prior + tick + str[indent:outdent] + tick + ";" + str[outdent:]
```

`parse`  markdown code into valid python code.


```python
    class Parser:
        def parse_code(self, token, *, indent=-1):
            code = token['match'].group().rstrip(); stripped = code.strip()
            if stripped.startswith(('>>>',)) or (not stripped and 'match' in token): return # don't do anything for blank code.
            if code.startswith(('```',)): 
                code = ''.join(['\n'] + code.rstrip('`').splitlines(True)[1:])
                if textwrap.dedent(code) == code: code = textwrap.indent(code, ' '*max(indent, 4))
            return code
        
        def indent_text(self, body, text, code="", *, indent=-1, block_level=0):
            try: tokenized = list(tokenize.tokenize(io.BytesIO(textwrap.dedent(body).encode('utf-8')).readline)) if body else []
            except tokenize.TokenError as exception:
                if exception.args[0] == 'EOF in multi-line string': text = textwrap.indent(text, ' '*_indent)
                else: text = (text.strip() and quote or identity)(text, ' '*_indent)
            else: 
                while tokenized and not tokenized[-1].string: tokenized.pop()
                this_indent, line = indent, tokenized[-1].line if tokenized else ""
                this_indent += len(line) - len(line.lstrip())
                if body.rstrip().endswith(':'): 
                    for last in code.splitlines() or ['']:
                        if last.strip(): break
                    this_indent += max(len(last)-len(last.lstrip())-this_indent + block_level*2, 4)
                text = quote(textwrap.indent(text, ' '*this_indent)) 
            return body + text + code
        
        def parse(self, object, *, formatted="", indent=-1, block_level=0):
            tokens, attrs = Lexer()(object), set(dir(self))
            while tokens:
                token = tokens.pop(0)
                if token['type'] == 'list_start': block_level += 1
                if token['type'] == 'list_end': block_level -= 1
                if F"parse_{token['type']}" in attrs: 
                    code = getattr(self, F"parse_{token['type']}")(token, indent=indent)
                    if code is None: continue
                    if indent < 0: indent = max(len(code) - len(code.lstrip()), 4)
                    text, object = re.split(r'\s*'.join(re.escape(token['match'].group().rstrip()).splitlines(True)), object)
                    formatted = self.indent_text(formatted, text, code, indent=indent, block_level=block_level)
            return self.indent_text(formatted, object, indent=indent)
        
                    
```

Another notebook defines how the output should be displayed.

Create `IPython` extensions that can be reused.


```python
    parser = Parser()
    def cleanup_transform(x): 
        global parser
        return textwrap.dedent(parser.parse(''.join(x))).splitlines(True)

    def unload_ipython_extension(shell):
        globals()['_transforms'] = globals().get('_transforms', shell.input_transformer_manager.cleanup_transforms)
        global _transforms
        shell.input_transformer_manager.cleanup_transforms = _transforms
    def load_ipython_extension(shell):
        unload_ipython_extension(shell)
        shell.input_transformer_manager.cleanup_transforms = [cleanup_transform]

    __name__ == '__main__' and load_ipython_extension(get_ipython())
```
