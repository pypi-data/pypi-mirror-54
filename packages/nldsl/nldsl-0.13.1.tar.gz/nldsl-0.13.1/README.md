# NLDSL

NLDSL is a tool to create domain specific languages (DSLs) for data science, which can be translated into executable code.
A new DSL is created by deriving from the CodeGenerator class and rules are added to it via simple python functions.
Besides providing code generation NLDSL allows the user to define DSL-level function,
which are then treated as first-class rules. Currently we provide extensions for Pandas and PySpark.

## Documentation and Tutorial

The complete documentation as well as a tutorial can be found on the [project web page](https://einhornstyle.gitlab.io/nldsl/).


## Installing

From the project root folder run:
```
pip install -r requirements.txt
python setup.py install
```


## Example Usage

1. Instanciate a code generator for Pandas
```python
from nldsl import PandasCodeGenerator, grammar
code_gen = PandasCodeGenerator()
```

2. Define a DSL statement and create executable code
```python
dsl_stmt = "## x = on df | rename columns old1 to new1, old2 to new2"
python_code = code_gen(dsl_stmt)
```

3. Add a new rule to the DSL and use it to create executable code
```python
new_rule = "#$ my rule $x = rename columns old to $x | drop duplicates"
dsl_stmt = "## x = on df | my rule new"
python_code = code_gen(new_rule + dsl_stmt)
```

4. Implement a new rule via python
```python
def rename_columns(code, args):
return code + ".rename(columns={})".format({args[i]:args[i+2] for i in range(0, len(args), 3)})
```

5. Implement the "rename columns" rule using the @grammar decorator, which parses the args for you.
```python
@grammar
def rename_columns(code, args):
""" Desc...
Grammar:
    rename columns $my_var[$old to $new]
"""
# The 'Grammar' section in the docstring of this function is mandatory.
return code + ".rename(columns={})".format(dict(args["my_var"]))
```

6. A new rule can either be added to a certain instance of a CodeGenerator or to the class itself.
```python
code_gen["rename columns"] = rename_columns
PandasCodeGenerator.register_function("rename colummns", rename_columns)
```

7. Create a custom CodeGenerator.
```python
from nldsl import CodeGenerator

class MyCodeGenerator(CodeGenerator):
    # optionally you can specify an __init__, extract_environment and postprocessing method.
    pass
```

8. By default a python expression parser is provided for every grammar rule, but you may also create your own.
```python
from nldsl.core import ExpressionRule

class MyExpressionRule(ExpressionRule):
    def __init__(self, expr_name, next_keyword):
        super().__init__(expr_name, next_keyword)
        # The symbol of an expression is modified by specifing it in the operator_map.
        # Note that spaces need to be added explicitly.
        self.operator_map["and"] = " & "
        self.operator_map["not"] = "~"

        # You can also change the type of an operator,
        # e.g. from binary to being a member function of the left argument.
        self.operator_map["in"] = ".isin"
        self.operator_type["in"] = OperatorType.UNARY_FUNCTION

# Tell the grammar rule 'my_rule' to use MyExpressionRule instead of the default.
@grammar(expr=MyExpressionRule)
def my_rule(code, args):
    # ...
```

9. CodeGenerators may be organized in a hierachy and combined or specialized via polymorphism.
```python
class CodeGenA(CodeGenerator): pass
CodeGenA.register_function("my_rule_a", my_rule_a)

class CodeGenB(CodeGenerator): pass
CodeGenB.register_function("my_rule_b", my_rule_b)

# Combine the rules in CodeGenA und CodeGenB
class CodeGenC(A, B): pass

# Specialize a rule in CodeGenA
class CodeGenD(A): pass
CodeGenD.register_function("my_rule_a", new_rule_a)
```


## Python Versions

Tested and supported for Python 3.4+
