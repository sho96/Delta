import ast

def get_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    if isinstance(node, ast.Name):
        return get_Name_datatype(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Subscript):
        return get_Subscript_datatype(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Call):
        return get_Call_datatype(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Attribute):
        return get_Attribute_datatype(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Constant):
        return get_Constant_datatype(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.BinOp):
        return get_BinOp_datatype(node, identifier_datatype_map, **kwargs)
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")
    

def get_Name_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript:
    if node.id in identifier_datatype_map:
        return identifier_datatype_map[node.id]
    else:
        raise ValueError(f"Name '{node.id}' is not tracked or defined")
def get_Subscript_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript: #slicing
    base_type = get_datatype(node.value, identifier_datatype_map, **kwargs)
    slice_value = node.slice
    if isinstance(base_type, ast.Name):
        match base_type.id:
            case "str":
                return ast.Name(id="str", ctx=ast.Load())
            case _:
                raise ValueError(f"{base_type.id} is not subscriptable")
    elif isinstance(base_type, ast.Subscript):
        basename = base_type.value.id
        match basename:
            case "list":
                return base_type.slice
            case "dict":
                return base_type.slice.elts[1]
            case "tuple":
                if "index" not in kwargs:
                    raise ValueError("retrieving datatype of tuple requires a provided index")
                return base_type.slice.elts[kwargs.get("index", 0)]
            case _:
                raise ValueError(f"{base_type.id} is not subscriptable")
    else:
        raise ValueError(f"{base_type.id} is not subscriptable")
def get_Call_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    if isinstance(node.func, ast.Name) and node.func.id in ["print", "input", "len", "int", "float", "str", "list", "max", "min", "sum", "sorted"]:
        return get_builtin_datatype(node, identifier_datatype_map, **kwargs)    
    base_type = get_datatype(node.func, identifier_datatype_map, **kwargs)
    return base_type
def get_builtin_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    if node.func.id == "print":
        return ast.Name(id="None", ctx=ast.Load())
    elif node.func.id == "input":
        return ast.Name(id="str", ctx=ast.Load())
    elif node.func.id == "len":
        return ast.Name(id="int", ctx=ast.Load())
    elif node.func.id in ["int", "float", "str", "list"]:
        return node.func
    elif node.func.id in ("min", "max"):
        target = node.args[0]
        target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
        if isinstance(target_dtype, ast.Name):
            match target_dtype.id:
                case "str":
                    return ast.Name(id="str", ctx=ast.Load())
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        elif isinstance(target_dtype, ast.Subscript):
            match target_dtype.value.id:
                case "list":
                    return target_dtype.slice
                case "set":
                    return target_dtype.slice
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        else:
            raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
    elif node.func.id == "sum":
        target = node.args[0]
        target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
        if isinstance(target_dtype, ast.Name):
            match target_dtype.id:
                case "str":
                    return ast.Name(id="int", ctx=ast.Load())
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        elif isinstance(target_dtype, ast.Subscript):
            match target_dtype.value.id:
                case "list":
                    return target_dtype.slice
                case "set":
                    return target_dtype.slice
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        else:
            raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
    elif node.func.id == "sorted":
        return get_datatype(node.args[0], identifier_datatype_map, **kwargs)
    elif node.func.id == "round":
        target = node.args[0]
        target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
        if isinstance(target_dtype, ast.Name):
            match target_dtype.id:
                case "float":
                    return ast.Name(id="float", ctx=ast.Load())
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        else:
            raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
    elif node.func.id == "abs":
        target = node.args[0]
        target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
        if isinstance(target_dtype, ast.Name):
            match target_dtype.id:
                case "int":
                    return ast.Name(id="int", ctx=ast.Load())
                case "float":
                    return ast.Name(id="float", ctx=ast.Load())
                case _:
                    raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
        else:
            raise ValueError(f"{target_dtype} is not supported for {node.func.id}")
    else:
        raise ValueError(f"{node.func} is not supported nor found")
def get_Attribute_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    base_type = get_datatype(node.value, identifier_datatype_map, **kwargs)
    attr = node.attr
    if isinstance(base_type, ast.Name):
        match base_type.id:
            case "str":
                match attr:
                    case "upper":
                        return ast.Name(id="str", ctx=ast.Load())
                    case "lower":
                        return ast.Name(id="str", ctx=ast.Load())
                    case "split":
                        return ast.Subscript(value=ast.Name(id="list", ctx=ast.Load()), slice=ast.Index(value=ast.Name(id="str", ctx=ast.Load())), ctx=ast.Load())
                    case "join":
                        return ast.Name(id="str", ctx=ast.Load())
                    case "strip":
                        return ast.Name(id="str", ctx=ast.Load())
                    case "replace":
                        return ast.Name(id="str", ctx=ast.Load())
                    case "find":
                        return ast.Name(id="int", ctx=ast.Load())
                    case "count":
                        return ast.Name(id="int", ctx=ast.Load())
                    case "isdigit":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isdecimal":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isnumeric":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isalpha":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isalnum":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isascii":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isspace":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "isupper":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case "islower":
                        return ast.Name(id="bool", ctx=ast.Load())
                    case _:
                        raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case "char":
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case "int":
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case "float":
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case "bool":
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case _:
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
    elif isinstance(base_type, ast.Subscript):
        match base_type.value.id:
            case "list":
                match attr:
                    case "append":
                        return ast.Constant(value=None, kind=None)
                    case "insert":
                        return ast.Constant(value=None, kind=None)
                    case "pop":
                        return ast.Name(id="int", ctx=ast.Load())
                    case "remove":
                        return ast.Constant(value=None, kind=None)
                    case "clear":
                        return ast.Constant(value=None, kind=None)
                    case _:
                        raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case "dict":
                match attr:
                    case "clear":
                        return ast.Constant(value=None, kind=None)
                    case "pop":
                        return ast.Constant(value=None, kind=None)
            case "set":
                match attr:
                    case "clear":
                        return ast.Constant(value=None, kind=None)
                    case "remove":
                        return ast.Constant(value=None, kind=None)
                    case "discard":
                        return ast.Constant(value=None, kind=None)
                    case "add":
                        return ast.Constant(value=None, kind=None)
                    case _:
                        raise ValueError(f"{base_type} has no available attributes nor supports attributes")
            case _:
                raise ValueError(f"{base_type} has no available attributes nor supports attributes")
    else:
        raise ValueError(f"{base_type} doesn't support attributes")
def get_Constant_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    datatype = node.value
    if datatype is None:
        return ast.Constant(value=None, kind=None)
    if isinstance(datatype, str):
        return ast.Name(id="str", ctx=ast.Load())
    elif isinstance(datatype, int):
        return ast.Name(id="int", ctx=ast.Load())
    elif isinstance(datatype, float):
        return ast.Name(id="float", ctx=ast.Load())
    elif isinstance(datatype, bool):
        return ast.Name(id="bool", ctx=ast.Load())
    else:
        raise ValueError(f"Unsupported constant type: {type(datatype)}")


def get_BinOp_datatype(node, identifier_datatype_map, **kwargs) -> ast.Name | ast.Subscript | ast.Constant:
    left = get_datatype(node.left, identifier_datatype_map, **kwargs)
    right = get_datatype(node.right, identifier_datatype_map, **kwargs)
    operator = node.op
    if isinstance(left, ast.Name) and isinstance(right, ast.Name):
        left_type = left.id
        right_type = right.id
        if left_type in ["int", "float"] and right_type in ["int", "float"]:
            match operator:
                case ast.Add():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        return ast.Name(id="float", ctx=ast.Load())
                case ast.Sub():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        return ast.Name(id="float", ctx=ast.Load())
                case ast.Mult():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        return ast.Name(id="float", ctx=ast.Load())
                case ast.Div():
                    return ast.Name(id="float", ctx=ast.Load())    
                case ast.Mod():
                    return ast.Name(id="int", ctx=ast.Load())
                case ast.Pow():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        return ast.Name(id="float", ctx=ast.Load())
                case ast.BitOr():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
                case ast.BitXor():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
                case ast.BitAnd():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
                case ast.LShift():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
                case ast.RShift():
                    if left_type == "int" and right_type == "int":
                        return ast.Name(id="int", ctx=ast.Load())
                    else:
                        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
                case ast.FloorDiv():
                    return ast.Name(id="int", ctx=ast.Load())
                case _:
                    raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
        elif left_type == "str" and right_type == "str":
            return ast.Name(id="str", ctx=ast.Load())
        elif left_type == "str" and right_type == "int":
            return ast.Name(id="str", ctx=ast.Load())
        else:
            raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
    elif isinstance(left, ast.Subscript) and isinstance(right, ast.Subscript):
        left_type = left.value.id
        right_type = right.value.id
        if left_type == "list" and right_type == "list":
            #check left and right dtype equality if possible
            return left
        elif left_type == "dict" and right_type == "dict":
            #check left and right dtype equality if possible
            return left
        elif left_type == "set" and right_type == "set":
            #check left and right dtype equality if possible
            return left
        else:
            raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
    elif isinstance(left, ast.Subscript) and isinstance(right, ast.Name):
        left_type = left.value.id
        right_type = right.id
        if left_type == "list" and right_type == "int":
            return left
        else:
            raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
    elif isinstance(left, ast.Name) and isinstance(right, ast.Subscript):
        left_type = left.id
        right_type = right.value.id
        raise ValueError(f"Unsupported operation '{operator}' between {left_type} and {right_type}")
    else:
        raise ValueError(f"what kind of operation is this???")

#def compile_part(node, compile_function=False, compile_importFrom=False, is_type_hint=False) -> list[str]:
def compile_part(node, identifier_datatype_map, **kwargs) -> list[str]:
    if isinstance(node, ast.Constant):
        return compile_Constant(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.JoinedStr):
        return compile_JoinedStr(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.List):
        return compile_List(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Tuple):
        return compile_Tuple(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Dict):
        return compile_Dict(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Set):
        return compile_Set(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Name):
        return compile_Name(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Expr):
        return compile_Expr(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.UnaryOp):
        return compile_UnaryOp(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.BinOp):
        return compile_BinOp(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.BoolOp):
        return compile_BoolOp(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Compare):
        return compile_Compare(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Call):
        return compile_Call(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.keyword):
        return compile_keyword(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.NamedExpr):
        return compile_NamedExpr(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Subscript):
        return compile_Subscript(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Assign):
        return compile_Assign(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.AnnAssign):
        return compile_AnnAssign(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.AugAssign):
        return compile_AugAssign(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Assert):
        return compile_Assert(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Pass):
        return compile_Pass(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.ImportFrom):
        if kwargs.get("compile_importFrom", False):
            return compile_ImportFrom(node, identifier_datatype_map, **kwargs)
        else:
            return []
    elif isinstance(node, ast.If):
        return compile_If(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.For):
        return compile_For(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.While):
        return compile_While(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Match):
        return compile_Match(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Break):
        return compile_Break(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Continue):
        return compile_Continue(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.FunctionDef):
        if kwargs.get("compile_function", False):
            return compile_FunctionDef(node, identifier_datatype_map, **kwargs)
        else:
            return []
    elif isinstance(node, ast.arguments):
        return compile_arguments(node, identifier_datatype_map, **kwargs)
    elif isinstance(node, ast.Return):
        return compile_Return(node, identifier_datatype_map, **kwargs)
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")

def compile_Constant(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Constant)
    value = node.value
    if isinstance(value, str):
        return [f'"{repr(value)[1:-1]}"']
    elif isinstance(value, bool):
        return [str(value).lower()]
    elif isinstance(value, (int, float)):
        return [str(value)]
    elif value is None:
        return ["NULL"]
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

def compile_JoinedStr(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.JoinedStr)
    elements = []
    for element in node.values:
        elements.append(
            compile_part(element, identifier_datatype_map) if isinstance(element, ast.Constant)
            else compile_part(element.value, identifier_datatype_map)
        )
        elements.append(",")
    elements = elements[:-1]
    return [
        "createJoinedStr(", 
        elements,
        ")"
    ]

def compile_List(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.List)
    tokens = ["{"]
    for element in node.elts:
        tokens += compile_part(element, identifier_datatype_map)
        tokens.append(",")
    if len(tokens) == 1:
        tokens.append("}")
    else:
        tokens[-1] = "}"
    return tokens

def compile_Tuple(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Tuple)
    tokens = ["std::make_tuple("]
    for element in node.elts:
        tokens += compile_part(element, identifier_datatype_map)
        tokens.append(",")
    if len(tokens) == 1:
        tokens.append(")")
    else:
        tokens[-1] = ")"
    return tokens

def compile_Dict(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Dict)
    tokens = ["{"]
    for key, value in zip(node.keys, node.values):
        tokens.append("{")
        tokens += compile_part(key, identifier_datatype_map)
        tokens.append(",")
        tokens += compile_part(value, identifier_datatype_map)
        tokens.append("}")
        tokens.append(",")
    if len(tokens) == 1:
        tokens.append("}")
    else:
        tokens[-1] = "}"
    return tokens

def compile_Set(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Set)
    tokens = ["{"]
    for element in node.elts:
        tokens += compile_part(element, identifier_datatype_map)
        tokens.append(",")
    if len(tokens) == 1:
        tokens.append("}")
    else:
        tokens[-1] = "}"
    return tokens

def compile_Name(node, identifier_datatype_map, **kwargs) -> list[str]:
    type_mapping = {
        "str": "std::string",
        "list": "std::vector",
        "dict": "std::map",
        "tuple": "std::tuple",
        "set": "std::set",
        "float": "double",
    }
    
    assert isinstance(node, ast.Name)
    for to_convert in type_mapping:
        if node.id == to_convert:
            return [type_mapping[to_convert]]
    return [node.id]


def compile_Expr(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Expr)
    return ["(", compile_part(node.value, identifier_datatype_map), ")"]

def compile_UnaryOp(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.UnaryOp)
    op_type = node.op
    operand = node.operand
    if isinstance(op_type, ast.UAdd):
        return ["+", compile_part(operand, identifier_datatype_map)]
    if isinstance(op_type, ast.USub):
        return ["-", compile_part(operand, identifier_datatype_map)]
    if isinstance(op_type, ast.Not):
        return ["!", compile_part(operand, identifier_datatype_map)]
    if isinstance(op_type, ast.Invert):
        return ["~", compile_part(operand, identifier_datatype_map)]

def compile_BinOp(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.BinOp)
    left = node.left
    right = node.right
    left_type = get_datatype(left, identifier_datatype_map)
    right_type = get_datatype(right, identifier_datatype_map)
    op_type = node.op
    if isinstance(left_type, ast.Name) and isinstance(right_type, ast.Name):
        left_type_name = left_type.id
        right_type_name = right_type.id
        if left_type_name in ["float", "int"] and right_type_name in ["float", "int"]:
            match op_type:
                case ast.Add():
                    return [compile_part(left, identifier_datatype_map), "+", compile_part(right, identifier_datatype_map)]
                case ast.Sub():
                    return [compile_part(left, identifier_datatype_map), "-", compile_part(right, identifier_datatype_map)]
                case ast.Mult():
                    return [compile_part(left, identifier_datatype_map), "*", compile_part(right, identifier_datatype_map)]
                case ast.Div():
                    return ["(float)", compile_part(left, identifier_datatype_map), "/ (float)", compile_part(right, identifier_datatype_map)]
                case ast.Mod():
                    return [compile_part(left, identifier_datatype_map), "%", compile_part(right, identifier_datatype_map)]
                case ast.Pow():
                    pref = ""
                    if left_type_name == "int" and right_type_name == "int":
                        pref = "(int)"
                    return [f"{pref}std::pow(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
                case ast.BitOr():
                    return [compile_part(left, identifier_datatype_map), "|", compile_part(right, identifier_datatype_map)]
                case ast.BitXor():
                    return [compile_part(left, identifier_datatype_map), "^", compile_part(right, identifier_datatype_map)]
                case ast.BitAnd():
                    return [compile_part(left, identifier_datatype_map), "&", compile_part(right, identifier_datatype_map)]
                case ast.LShift():
                    return [compile_part(left, identifier_datatype_map), "<<", compile_part(right, identifier_datatype_map)]
                case ast.RShift():
                    return [compile_part(left, identifier_datatype_map), ">>", compile_part(right, identifier_datatype_map)]
                case ast.FloorDiv():
                    return ["(int)(", compile_part(left, identifier_datatype_map), "/", compile_part(right, identifier_datatype_map), ")"]
                case _:
                    raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
        if left_type_name == "str" and right_type_name == "str":
            match op_type:
                case ast.Add():
                    return [compile_part(left, identifier_datatype_map), "+", compile_part(right, identifier_datatype_map)]
                case _:
                    raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
        if left_type_name == "str" and right_type_name == "int":
            match op_type:
                case ast.Mult():
                    return ["repeatStr(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
                case _:
                    raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
    elif isinstance(left_type, ast.Subscript) and isinstance(right_type, ast.Subscript):
        left_type_name = left_type.value.id
        right_type_name = right_type.value.id
        if left_type_name == "list" and right_type_name == "list":
            #check left and right dtype equality if possible
            return ["concatVec(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
        elif left_type_name == "dict" and right_type_name == "dict":
            #check left and right dtype equality if possible
            return ["concatMap(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
        elif left_type_name == "set" and right_type_name == "set":
            #check left and right dtype equality if possible
            return ["concatSet(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
        else:
            raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
    elif isinstance(left_type, ast.Subscript) and isinstance(right_type, ast.Name):
        left_type_name = left_type.value.id
        right_type_name = right_type.id
        if left_type_name == "list" and right_type_name == "int":
            return ["repeatVec(", compile_part(left, identifier_datatype_map), ",", compile_part(right, identifier_datatype_map), ")"]
        else:
            raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
    elif isinstance(left_type, ast.Name) and isinstance(right_type, ast.Subscript):
        left_type_name = left_type.id
        right_type_name = right_type.value.id
        raise ValueError(f"Unsupported operation '{op_type}' between {left_type_name} and {right_type_name}")
    else:
        raise ValueError(f"what kind of operation is this???")
    raise ValueError(f"not yet implemented: {left_type} {op_type} {right_type}")

def compile_BoolOp(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.BoolOp)
    op_type = node.op
    values = node.values
    if isinstance(op_type, ast.And):
        return [" && ".join(assemble_to_string(compile_part(value, identifier_datatype_map)) for value in values)]
    if isinstance(op_type, ast.Or):
        return [" || ".join(assemble_to_string(compile_part(value, identifier_datatype_map)) for value in values)]
    raise ValueError(f"Unsupported boolean operator: {op_type}")

def compile_Compare(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Compare)
    left = node.left
    comparators = node.comparators
    op_type = node.ops
    if isinstance(op_type[0], ast.Eq):
        return [compile_part(left, identifier_datatype_map), "==", compile_part(comparators[0], identifier_datatype_map)]
    if isinstance(op_type[0], ast.NotEq):
        return [compile_part(left, identifier_datatype_map), "!=", compile_part(comparators[0], identifier_datatype_map)]
    if isinstance(op_type[0], ast.Lt):
        return [compile_part(left, identifier_datatype_map), "<", compile_part(comparators[0], identifier_datatype_map)]
    if isinstance(op_type[0], ast.LtE):
        return [compile_part(left, identifier_datatype_map), "<=", compile_part(comparators[0], identifier_datatype_map)]
    if isinstance(op_type[0], ast.Gt):
        return [compile_part(left, identifier_datatype_map), ">", compile_part(comparators[0], identifier_datatype_map)]
    if isinstance(op_type[0], ast.GtE):
        return [compile_part(left, identifier_datatype_map), ">=", compile_part(comparators[0], identifier_datatype_map)]
    raise ValueError(f"Unsupported comparison operator: {op_type[0]}")
    


def compile_Call(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Call)
    func = node.func
    args = node.args
    keywords = node.keywords
    
    #print(args, identifier_datatype_map)
    if isinstance(func, ast.Name):
        if func.id == "print":
            end = "std::endl"
            if len(keywords) > 0:
                if keywords[0].arg == "end":
                    end = compile_part(keywords[0].value, identifier_datatype_map)
                else:
                    raise ValueError(f"Unsupported keyword argument for print: {keywords[0].arg}")
            if len(args) == 0:
                return ["std::cout << ", end]
            else:
                return ["std::cout << ", " << ".join(assemble_to_string(compile_part(arg, identifier_datatype_map)) for arg in args), " << ", end]
        if func.id == "input":
            return ["userInput(", ", ".join(assemble_to_string(compile_part(arg, identifier_datatype_map)) for arg in args), ")"]
        if func.id == "len":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        return [compile_part(target, identifier_datatype_map, **kwargs), ".length()"]
                    case _:
                        raise ValueError(f"cannot get length of {target_dtype}")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        return [compile_part(target, identifier_datatype_map, **kwargs), ".size()"]
                    case "dict":
                        return [compile_part(target, identifier_datatype_map, **kwargs), ".size()"]
                    case "set":
                        return [compile_part(target, identifier_datatype_map, **kwargs), ".size()"]
                    case "tuple":
                        return ["std::tuple_size<", compile_part(target, identifier_datatype_map, **kwargs), ">::value"]
                    case _:
                        raise ValueError(f"cannot get length of {target_dtype}")
            else:
                raise ValueError(f"cannot get length of {target_dtype}")
        if func.id == "int":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        return ["std::stoi(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "float":
                        return ["static_cast<int>(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "int":
                        return [compile_part(target, identifier_datatype_map, **kwargs)]
                    case _:
                        raise ValueError(f"cannot convert {target_dtype} to int")
            else:
                raise ValueError(f"cannot convert {target_dtype} to int")
        if func.id == "float":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        return ["std::stod(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "int":
                        return ["static_cast<float>(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "float":
                        return [compile_part(target, identifier_datatype_map, **kwargs)]
                    case _:
                        raise ValueError(f"cannot convert {target_dtype} to float")
            else:
                raise ValueError(f"cannot convert {target_dtype} to float")
        if func.id == "str":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "int":
                        return ["std::to_string(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "float":
                        return ["std::to_string(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "bool":
                        return [compile_part(target, identifier_datatype_map, **kwargs), " ? \"True\" : \"False\""]
                    case "char":
                        return ["std::to_string(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "str":
                        return [compile_part(target, identifier_datatype_map, **kwargs)]
                    case _:
                        raise ValueError(f"cannot convert {target_dtype} to string")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        return ["vec2str(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "dict":
                        return ["dict2str(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "set":
                        return ["set2str(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "tuple":
                        return ["tuple2str(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case _:
                        raise ValueError(f"cannot convert {target_dtype} to string")
            else:
                raise ValueError(f"cannot convert {target_dtype} to string")
        if func.id == "list":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        return ["splitStringToChars(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case _:
                        raise ValueError(f"cannot convert {target_dtype} to list")
            else:
                raise ValueError(f"cannot convert {target_dtype} to list")
        if func.id == "max":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::max_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply max to {target_dtype}")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::max_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case "set":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::max_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply max to {target_dtype}")
        if func.id == "min":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::min_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply min to {target_dtype}")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::min_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case "set":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["*std::min_element(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply min to {target_dtype}")
        
        if func.id == "sum":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::reduce(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply sum to {target_dtype}")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::reduce(", compiled, ".begin(), ", compiled, ".end())"]
                    case "set":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::reduce(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply sum to {target_dtype}")
        
        if func.id == "sorted":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            reversed = ast.Constant(value=False)
            if len(keywords) > 0:
                if keywords[0].arg == "reverse":
                    raise ValueError(f"reverse sorting not implemented")
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "str":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::sort(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply sorted to {target_dtype}")
            elif isinstance(target_dtype, ast.Subscript):
                match target_dtype.value.id:
                    case "list":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::sort(", compiled, ".begin(), ", compiled, ".end())"]
                    case "set":
                        compiled = compile_part(target, identifier_datatype_map, **kwargs)
                        return ["std::sort(", compiled, ".begin(), ", compiled, ".end())"]
                    case _:
                        raise ValueError(f"cannot apply sorted to {target_dtype}")
        if func.id == "round":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "float":
                        return ["std::round(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case _:
                        raise ValueError(f"cannot apply round to {target_dtype}")
            else:
                raise ValueError(f"cannot apply round to {target_dtype}")
        if func.id == "abs":
            target = args[0]
            target_dtype = get_datatype(target, identifier_datatype_map, **kwargs)
            if isinstance(target_dtype, ast.Name):
                match target_dtype.id:
                    case "int":
                        return ["std::abs(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case "float":
                        return ["std::abs(", compile_part(target, identifier_datatype_map, **kwargs), ")"]
                    case _:
                        raise ValueError(f"cannot apply abs to {target_dtype}")
            else:
                raise ValueError(f"cannot apply abs to {target_dtype}")
        
        
        
        if func.id == "cpp":
            return [args[0].value]
        
        #not print
        if len(keywords) == 0:
            return [func.id, "(",  ", ".join(assemble_to_string(compile_part(arg, identifier_datatype_map)) for arg in args), ")"]
        else:
            return [func.id, "(",  ", ".join(assemble_to_string(compile_part(arg, identifier_datatype_map)) for arg in args), ",", ", ".join(assemble_to_string(compile_part(kw), identifier_datatype_map) for kw in keywords), ")"]
    elif isinstance(func, ast.Attribute):
        value = func.value
        attr = func.attr
        
        if isinstance(value, ast.Name):
            value_type = get_datatype(value, identifier_datatype_map, **kwargs)
            
            if value_type is None:
                raise ValueError(f"datatype of identifier '{value.id}' is not tracked nor defined")
            
            if isinstance(value_type, ast.Subscript):
                if value_type.value.id == "list":
                    #to add: insert
                    if attr == "append":
                        return [compile_part(value, identifier_datatype_map), ".push_back(", compile_part(args[0], identifier_datatype_map), ")"]
                    if attr == "pop":
                        if len(args) == 0:
                            return [compile_part(value, identifier_datatype_map), ".pop_back()"]
                        else:
                            return ["deleteAtIndex(", compile_part(value, identifier_datatype_map), ", ", compile_part(args[0], identifier_datatype_map), ")"]
                    if attr == "clear":
                        return [compile_part(value, identifier_datatype_map), ".clear()"]
                    if attr == "remove":
                        return ["removeByValue(", compile_part(value, identifier_datatype_map), ", ", compile_part(args[0], identifier_datatype_map), ")"]
                if value_type.value.id == "dict":
                    if attr == "clear":
                        return [compile_part(value, identifier_datatype_map), ".clear()"]
                    if attr == "pop":
                        return [compile_part(value, identifier_datatype_map), ".erase(", compile_part(args[0], identifier_datatype_map), ")"]
                if value_type.value.id == "set":
                    if attr == "clear":
                        return [compile_part(value, identifier_datatype_map), ".clear()"]
                    if attr in ("remove", "discard"):
                        return [compile_part(value, identifier_datatype_map), ".erase(", compile_part(args[0], identifier_datatype_map), ")"]
                    if attr == "add":
                        return [compile_part(value, identifier_datatype_map), ".insert(", compile_part(args[0], identifier_datatype_map), ")"]
                        
            elif isinstance(value_type, ast.Name):
                if value_type.id == "str":
                    match attr:
                        case "upper":
                            return ["str_toupper(", compile_part(args[0], identifier_datatype_map), ")"]
                        case "lower":
                            return ["str_tolower(", compile_part(args[0], identifier_datatype_map), ")"]
                        case "split":
                            if len(args) != 1:
                                raise ValueError(f"str.split requires 1 argument")
                            if isinstance(args[0], ast.Constant) and len(args[0].value) == 1:
                                return ["splitString(", compile_part(value, identifier_datatype_map), ", \'", args[0].value, "\')"]
                            else:
                                return ["splitStringWithString(", compile_part(value, identifier_datatype_map), ", ", compile_part(args[0], identifier_datatype_map), ")"]
                        case "join":
                            return ["string_join(", compile_part(args[0], identifier_datatype_map), ", ", compile_part(value, identifier_datatype_map), ")"]
                        case "strip":
                            if len(args) == 0:
                                return ["string_strip(", compile_part(value, identifier_datatype_map), ", \" \\n\\t\\r\")"]
                            else:
                                return ["string_strip(", compile_part(value, identifier_datatype_map), ", ", compile_part(args[0], identifier_datatype_map), ")"]
                        case "replace":
                            if len(args) != 2:
                                raise ValueError(f"str.replace requires 2 arguments")
                            return ["string_replace(", compile_part(value, identifier_datatype_map), ", ", compile_part(args[0], identifier_datatype_map), ", ", compile_part(args[1], identifier_datatype_map), ")"]
                        case "find":
                            return [compile_part(value, identifier_datatype_map), ".find(", compile_part(args[0], identifier_datatype_map), ")"]
                        case "count":
                            if len(args) != 1:
                                raise ValueError(f"str.count requires 1 argument")
                            arg = args[0]
                            if isinstance(arg, ast.Constant) and len(arg.value) == 1:
                                return ["string_count_char(", compile_part(value, identifier_datatype_map), ", \'", arg.value, "\')"]
                            else:
                                return ["string_count(", compile_part(value, identifier_datatype_map), ", ", compile_part(arg, identifier_datatype_map), ")"]
                        case "isdigit":
                            return ["string_isdigit(", compile_part(value, identifier_datatype_map), ")"]
                        case "isdecimal":
                            return ["string_isdigit(", compile_part(value, identifier_datatype_map), ")"]
                        case "isnumeric":
                            return ["string_isdigit(", compile_part(value, identifier_datatype_map), ")"]
                        case "isalpha":
                            return ["string_isalpha(", compile_part(value, identifier_datatype_map), ")"]
                        case "isalnum":
                            return ["string_isalnum(", compile_part(value, identifier_datatype_map), ")"]
                        case "isascii":
                            return ["string_isascii(", compile_part(value, identifier_datatype_map), ")"]
                        case "isspace":
                            return ["string_isspace(", compile_part(value, identifier_datatype_map), ")"]
                        case "isupper":
                            return ["string_isupper(", compile_part(value, identifier_datatype_map), ")"]
                        case "islower":
                            return ["string_islower(", compile_part(value, identifier_datatype_map), ")"]
                        case _:
                            raise ValueError(f"attribute '{attr}' is not supported for string")
                if value_type.id == "char":
                    pass
                if value_type.id == "int":
                    pass
                if value_type.id == "float":
                    pass
                if value_type.id == "bool":
                    pass
        else:
            raise ValueError(f"{value} is not supported for attribute call")
            
        

def compile_keyword(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.keyword)
    return [node.arg, "=", compile_part(node.value, identifier_datatype_map)]

def compile_NamedExpr(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.NamedExpr)
    target = node.target
    value = node.value
    return [compile_part(target, identifier_datatype_map), "=", compile_part(value, identifier_datatype_map)]

def compile_Subscript(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Subscript)
    base = node.value
    slice_value = node.slice
    
    num_of_slice_values = 0
    slice_indices = []
    if isinstance(slice_value, ast.Tuple):
        slice_indices = slice_value.elts
        num_of_slice_values = len(slice_indices)
    elif isinstance(slice_value, ast.Slice):
        if slice_value.step is None:
            num_of_slice_values = 2
            slice_indices = [slice_value.lower, slice_value.upper]
        else:
            num_of_slice_values = 3
            slice_indices = [slice_value.lower, slice_value.upper, slice_value.step]
    elif isinstance(slice_value, (ast.Name, ast.Constant, ast.Subscript, ast.Attribute, ast.Call)):
        num_of_slice_values = 1
        slice_indices = [slice_value]
    
    
    else:
        raise ValueError(f"slicing with {slice_value} is not supported")
    
    if kwargs.get("is_type_hint", False):
        #to be implemented
        match base.id:
            case "list":
                return ["std::vector<", compile_part(slice_indices[0], identifier_datatype_map, is_type_hint=True), ">"]
            case "dict":
                return ["std::map<", compile_part(slice_indices[0], identifier_datatype_map, is_type_hint=True), ", ", compile_part(slice_indices[1], identifier_datatype_map, is_type_hint=True), ">"]
            case "tuple":
                slicing_parts = []
                for slice_value in slice_indices:
                    slicing_parts.append(compile_part(slice_value, identifier_datatype_map, is_type_hint=True))
                    slicing_parts.append(",")
                return ["std::tuple<", slicing_parts[:-1], ">"]
            case "set":
                return ["std::set<", compile_part(slice_indices[0], identifier_datatype_map, is_type_hint=True), ">"]
    
    basetype = get_datatype(base, identifier_datatype_map)
    if isinstance(basetype, ast.Name):
        basename = basetype.id
        match basename:
            case "str":
                #substring
                if num_of_slice_values == 1:
                    return [compile_part(base, identifier_datatype_map), "[", compile_part(slice_indices[0], identifier_datatype_map), "]"]
                elif num_of_slice_values == 2:
                    return ["sliceString(", compile_part(base, identifier_datatype_map), ",", compile_part(slice_indices[0], identifier_datatype_map), ",", compile_part(slice_indices[1], identifier_datatype_map), ")"]
                elif num_of_slice_values == 3:
                    return ["sliceString(", compile_part(base, identifier_datatype_map), ",", compile_part(slice_indices[0], identifier_datatype_map), ",", compile_part(slice_indices[1], identifier_datatype_map), ",", compile_part(slice_indices[2], identifier_datatype_map), ")"]
                else:
                    raise ValueError(f"{basename} can't be subscripted with more than 3 values")
            case _:
                raise ValueError(f"{basename} is not subscriptable")
    elif isinstance(basetype, ast.Subscript):
        basename = basetype.value.id
        match basename:
            case "list":
                if num_of_slice_values == 1:
                    return [compile_part(base, identifier_datatype_map), "[", compile_part(slice_indices[0], identifier_datatype_map), "]"]
                elif num_of_slice_values == 2:
                    return ["sliceVector(", compile_part(base, identifier_datatype_map), ",", compile_part(slice_indices[0], identifier_datatype_map), ",", compile_part(slice_indices[1], identifier_datatype_map), ")"]
                elif num_of_slice_values == 3:
                    return ["sliceVector(", compile_part(base, identifier_datatype_map), ",", compile_part(slice_indices[0], identifier_datatype_map), ",", compile_part(slice_indices[1], identifier_datatype_map), ",", compile_part(slice_indices[2], identifier_datatype_map), ")"]
                else:
                    raise ValueError(f"{basename} can't be subscripted with more than 3 values")
            case "dict":
                if num_of_slice_values == 1:
                    return [compile_part(base, identifier_datatype_map), "[", compile_part(slice_value, identifier_datatype_map), "]"]
                else:
                    raise ValueError(f"{basename} can't be subscripted with more than 1 value")
            case "tuple":
                if num_of_slice_values == 1:
                    return ["std::get<", compile_part(slice_value, identifier_datatype_map), ">(", compile_part(base, identifier_datatype_map), ")"]
                else:
                    raise ValueError(f"{basename} can't be subscripted with more than 1 value for type safety")
            case _:
                raise ValueError(f"{basename} is not subscriptable")
    else:
        raise ValueError(f"{basetype} is not subscriptable")

def compile_Assign(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Assign)
    targets = node.targets
    value = node.value
    return [compile_part(targets[0], identifier_datatype_map), "=", compile_part(value, identifier_datatype_map)]


def compile_AnnAssign(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.AnnAssign)
    target = node.target
    annotation = node.annotation
    value = node.value
    
    identifier_datatype_map[target.id] = annotation
    
    if value is None:
        return [compile_part(annotation, identifier_datatype_map, is_type_hint=True), compile_part(target, identifier_datatype_map)]
    else:
        return [compile_part(annotation, identifier_datatype_map, is_type_hint=True), compile_part(target, identifier_datatype_map), "=", compile_part(value, identifier_datatype_map)]

def compile_AugAssign(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.AugAssign)
    target = node.target
    op = node.op
    value = node.value
    if isinstance(op, ast.Add):
        op = "+="
    if isinstance(op, ast.Sub):
        op = "-="
    if isinstance(op, ast.Mult):
        op = "*="
    if isinstance(op, ast.Div):
        op = "/="
    if isinstance(op, ast.Mod):
        op = "%="
    if isinstance(op, ast.BitOr):
        op = "|="
    if isinstance(op, ast.BitXor):
        op = "^="
    if isinstance(op, ast.BitAnd):
        op = "&="
    if isinstance(op, ast.LShift):
        op = "<<="
    if isinstance(op, ast.RShift):
        op = ">>="
    
    if not isinstance(op, str):
        raise ValueError(f"Unsupported augmented assignment operator: {op}")
    return [compile_part(target, identifier_datatype_map), op, compile_part(value, identifier_datatype_map)]

def compile_Assert(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Assert)
    test = node.test
    msg = node.msg
    if msg is None:
        return ["assert(", compile_part(test, identifier_datatype_map), ");"]
    else:
        return ["assert(", compile_part(test, identifier_datatype_map), ", ", compile_part(msg, identifier_datatype_map), ")"]

def compile_Pass(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Pass)
    return ["/*pass*/"]

#TO_IMPLEMENT: Import, ImportFrom
def compile_ImportFrom(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.ImportFrom)
    module = node.module
    names = node.names
    
    if module.startswith("cpp"):
        ext = module[3:]
        if ext == "":
            return [f"#include <{alias.name}>\n" for alias in names]
        elif ext[0] == "s":
            ext = ext[1:]
            return [f"#include \"{alias.name}.{ext}\"\n" for alias in names]
        else:
            return [f"#include <{alias.name}.{ext}>\n" for alias in names]
    
    
    
        
    return ["/*import from ", module, "*/"]

def compile_If(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.If)
    test = node.test
    body = node.body
    orelse = node.orelse
    return ["if(", compile_part(test, identifier_datatype_map), ") {\n", compile_body(body, identifier_datatype_map), "\n} else {\n", compile_body(orelse, identifier_datatype_map), "\n}"]

def compile_For(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.For)
    target = node.target
    iterable = node.iter
    body = node.body
    
    if isinstance(iterable, ast.Call) and iterable.func.id == "range":
        #range
        range_args = iterable.args
        start = ast.Constant(value=0)
        stop = ast.Constant(value=1)
        step = ast.Constant(value=1)
        if len(range_args) == 1:
            stop = range_args[0]
        elif len(range_args) == 2:
            start = range_args[0]
            stop = range_args[1]
        elif len(range_args) == 3:
            start = range_args[0]
            stop = range_args[1]
            step = range_args[2]
        else:
            raise ValueError(f"Unsupported range() call: {range_args}")
        return [
            "for(int ", compile_part(target, identifier_datatype_map), "= ", compile_part(start, identifier_datatype_map), "; ", 
            compile_part(target, identifier_datatype_map), " < ", compile_part(stop, identifier_datatype_map), "; ", 
            compile_part(target, identifier_datatype_map), " += ", compile_part(step, identifier_datatype_map), ") {\n", 
            compile_body(body, identifier_datatype_map | {target.id: ast.Name(id="int")}),
            "\n}"
        ]
    
    iterable_type = get_datatype(iterable, identifier_datatype_map, **kwargs)
    if isinstance(iterable_type, ast.Constant):
        if iterable_type.value is None:
            raise ValueError("Nonetype is not iterable")
        match iterable_type.value:
            case "str":
                return [
                    "for(", "const", "char", target.id, " : ", compile_part(iterable, identifier_datatype_map), ") {\n", 
                    compile_body(body, identifier_datatype_map | {target.id: ast.Name(id="char")}),
                    "\n}"
                ]
            case _:
                raise ValueError(f"{iterable_type} is not iterable")
    elif isinstance(iterable_type, ast.Subscript):
        raw_dtype = iterable_type.slice
        if iterable_type.value.id in ("list", "set"):
            dtype = compile_part(raw_dtype, identifier_datatype_map, is_type_hint=True)
            return [
                "for(", "const", dtype, target.id, " : ", compile_part(iterable, identifier_datatype_map), ") {\n", 
                compile_body(body, identifier_datatype_map | {target.id: raw_dtype}), 
                "\n}"
            ]
        elif iterable_type.value.id == "dict":
            dtype = compile_part(raw_dtype.elts[0], identifier_datatype_map, is_type_hint=True)
            return [
                "for(", "const", dtype, target.id, " : ", "getKeys(", compile_part(iterable, identifier_datatype_map), ")", ") {\n", 
                compile_body(body, identifier_datatype_map | {target.id: raw_dtype.elts[0]}), 
                "\n}"
            ]
        else:
            raise ValueError(f"{iterable_type} is not iterable")
    elif isinstance(iterable_type, ast.Name):
        match iterable_type.id:
            case "str":
                return [
                    "for(", "const", "char", target.id, " : ", compile_part(iterable, identifier_datatype_map), ") {\n", 
                    compile_body(body, identifier_datatype_map | {target.id: ast.Name(id="char")}),
                    "\n}"
                ]
            case _:
                raise ValueError(f"{iterable_type} is not iterable")
    else:
        raise ValueError(f"{iterable_type} is not iterable")
        

def compile_While(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.While)
    test = node.test
    body = node.body
    return ["while(", compile_part(test, identifier_datatype_map), ") {\n", compile_body(body, identifier_datatype_map), "\n}"]

def compile_Match(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Match)
    subject = node.subject
    cases = node.cases
    
    subject_dtype = get_datatype(subject, identifier_datatype_map, **kwargs)
    
    match_type = ""
    if isinstance(subject_dtype, ast.Name):
        match subject_dtype.id:
            case "int":
                match_type = "switch"
            case "char":
                match_type = "switch"
            case _:
                match_type = "if"
    else:
        match_type = "if"
    
    if match_type == "switch":
        return [
            "switch (", compile_part(subject, identifier_datatype_map), ") {\n",
            [compile_match_case(case, identifier_datatype_map, match_type=match_type) for case in cases],
            "}\n",
        ]
    else:
        return ["{\n",
            "const auto __to_match = ", compile_part(subject, identifier_datatype_map), ";\n",
            [compile_match_case(case, identifier_datatype_map, match_type=match_type, varname="__to_match", case_index=i) for i, case in enumerate(cases)],
            "}\n",
        ]
        

def compile_match_case(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.match_case)
    pattern = node.pattern
    body = node.body
    if not isinstance(pattern, (ast.MatchAs, ast.MatchValue)):
        raise ValueError(f"Match case should have single value pattern, but got {pattern}")
    if isinstance(pattern, ast.MatchValue) and not isinstance(pattern.value, ast.Constant):
        raise ValueError(f"Match case should be a constant value, but got {pattern.value}")
    
    value = ast.Constant(value=None, kind=None) if isinstance(pattern, ast.MatchAs) else pattern.value
    
    if kwargs.get("match_type") == "switch":
        if isinstance(pattern, ast.MatchAs):
            return [
                "default:\n",
                compile_body(body, identifier_datatype_map),
                "break;\n"
            ]
        else:
            return [
                "case", compile_part(value, identifier_datatype_map), ":\n",
                compile_body(body, identifier_datatype_map),
                "break;\n"
            ]
    elif kwargs.get("match_type") == "if":
        if isinstance(pattern, ast.MatchAs):
            return [
                "else {\n",
                compile_body(body, identifier_datatype_map),
                "}"
            ]
        else:
            return [
                f"{'if' if kwargs.get('case_index') == 0 else 'else if'}({kwargs["varname"]} ==", compile_part(value, identifier_datatype_map), ") {\n",
                compile_body(body, identifier_datatype_map),
                "}"
            ]
    else:
        raise ValueError(f"Unknown match type {kwargs.get('match_type')}")

def compile_Break(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Break)
    return ["break"]

def compile_Continue(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Continue)
    return ["continue"]

def compile_FunctionDef(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.FunctionDef)
    name = node.name
    args = node.args
    body = node.body
    return_type_node = node.returns

    identifier_datatype_map[name] = return_type_node

    if isinstance(return_type_node, ast.Constant) and return_type_node.value is None:
        return [
            "void",
            name,
            "(",
            compile_part(args, identifier_datatype_map),
            ") {\n",
            compile_body(body, {arg.arg: arg.annotation for arg in args.args}),
            "\n}"
        ]
    else:
        return [
            compile_part(return_type_node, identifier_datatype_map, is_type_hint=True),
            name,
            "(",
            compile_part(args, identifier_datatype_map),
            ") {\n",
            compile_body(body, {arg.arg: arg.annotation for arg in args.args}),
            "\n}"
        ]


    

def compile_arguments(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.arguments)
    args = node.args
    raw_args = [[compile_part(arg.annotation, identifier_datatype_map, is_type_hint=True), arg.arg] for arg in args]
    result = []
    for arg in raw_args:
        result.append(arg)
        result.append(", ")
    return result[:-1]

def compile_Return(node, identifier_datatype_map, **kwargs) -> list[str]:
    assert isinstance(node, ast.Return)
    value = node.value
    return ["return ", compile_part(value, identifier_datatype_map)]

def find_function_defs(body, **kwargs) -> list[ast.FunctionDef]:
    result = []
    for code in body:
        if isinstance(code, ast.FunctionDef):
            result.append(code)
        if "body" in dir(code):
            result = result + find_function_defs(code.body)
    return result

def find_import_froms(body, **kwargs) -> list[ast.ImportFrom]:
    result = []
    for code in body:
        if isinstance(code, ast.ImportFrom):
            result.append(code)
        if "body" in dir(code):
            result = result + find_import_froms(code.body)
    return result

def compile_function_defs(entire_body, identifier_datatype_map, **kwargs) -> list[str]:
    functions_to_compile = find_function_defs(entire_body)

    result = []
    for func in functions_to_compile:
        result.append(compile_FunctionDef(func, identifier_datatype_map))
    return result
    

def compile_import_froms(entire_body, identifier_datatype_map, **kwargs) -> list[str]:
    import_froms_to_compile = find_import_froms(entire_body)

    result = []
    for import_from in import_froms_to_compile:
        result.append(compile_ImportFrom(import_from, identifier_datatype_map))
    return result

#TO_IMPLEMENT: ClassDef

def compile_body(body, identifier_datatype_map) -> list[str]:
    identifier_datatype_map = identifier_datatype_map.copy()
    result = []
    for code in body:
        print(f"compiling {code}")
        result.append(compile_part(code, identifier_datatype_map))
        result.append(";\n")
    return result

def assemble_to_string(body: list) -> str:
    result = ""
    for part in body:
        if isinstance(part, list):
            result += assemble_to_string(part)
        else:
            result += f"{r'{}'.format(part)} "
    return result

functions_for_converting_to_string = """
// Forward declarations of conversion functions
template <typename V>
std::string vec2str(const std::vector<V> &vec);

template <typename K, typename V>
std::string map2str(const std::map<K, V> &map);

template <typename V>
std::string set2str(const std::set<V> &set);

template <typename... Args>
std::string tuple2str(const std::tuple<Args...> &tup);

// Specialization for std::string
std::string valueToString(const std::string &value)
{
    return "\\"" + value + "\\"";
}

// Specialization for bool
std::string valueToString(const bool &value)
{
    return value ? "true" : "false";
}

// Specialization for std::tuple
template <typename... Args>
std::string valueToString(const std::tuple<Args...> &tup)
{
    return tuple2str(tup);
}

// Specialization for std::vector
template <typename V>
std::string valueToString(const std::vector<V> &vec)
{
    return vec2str(vec);
}

// Specialization for std::map
template <typename K, typename V>
std::string valueToString(const std::map<K, V> &map)
{
    return map2str(map);
}

// Specialization for std::set
template <typename V>
std::string valueToString(const std::set<V> &set)
{
    return set2str(set);
}

// Generic valueToString template
template <typename T>
std::string valueToString(const T &value)
{
    std::ostringstream oss;
    oss << value;
    return oss.str();
}

// Conversion functions
template <typename V>
std::string vec2str(const std::vector<V> &vec)
{
    std::string result = "[";
    for (const auto &item : vec)
    {
        result += valueToString(item) + ", ";
    }
    if (!vec.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "]";
    return result;
}

template <typename K, typename V>
std::string map2str(const std::map<K, V> &map)
{
    std::string result = "{";
    for (const auto &[key, value] : map)
    {
        result += valueToString(key) + ": ";
        result += valueToString(value) + ", ";
    }
    if (!map.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "}";
    return result;
}

template <typename V>
std::string set2str(const std::set<V> &set)
{
    std::string result = "{";
    for (const auto &item : set)
    {
        result += valueToString(item) + ", ";
    }
    if (!set.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "}";
    return result;
}

// Helper function to convert a tuple to a string
template <typename Tuple, std::size_t... Is>
std::string tuple2str_impl(const Tuple &tup, std::index_sequence<Is...>)
{
    std::string result = "(";
    ((result += valueToString(std::get<Is>(tup)) + ", "), ...);
    if constexpr (sizeof...(Is) > 0)
        result.resize(result.size() - 2); // Remove last ", "
    result += ")";
    return result;
}

template <typename... Args>
std::string tuple2str(const std::tuple<Args...> &tup)
{
    return tuple2str_impl(tup, std::index_sequence_for<Args...>{});
}"""

additional_functions = """
template<typename K, typename V>
std::vector<K> getKeys(const std::map<K, V>& m) {
    std::vector<K> keys;
    keys.reserve(m.size()); // Optional: Reserve memory to improve performance
    for (const auto& pair : m) {
        keys.push_back(pair.first);
    }
    return keys;
}

template<typename Container>
void deleteAtIndex(Container& container, typename Container::size_type index) {
    if (index >= 0 && index < container.size()) {
        container.erase(container.begin() + index);
    } else {
        std::cout << "Index out of range" << std::endl;
    }
}

template<typename Container, typename T>
void removeByValue(Container& container, const T& value) {
    container.erase(std::remove(container.begin(), container.end(), value), container.end());
}

template<typename T>
std::vector<T> sliceVector(const std::vector<T>& vec, int sliceStart, int sliceEnd, int step=1) {
    // Adjust negative indices
    if (sliceStart < 0) sliceStart += vec.size();
    if (sliceEnd < 0) sliceEnd += vec.size();

    // Ensure indices are within bounds
    sliceStart = std::max(0, sliceStart);
    sliceEnd = std::min(static_cast<int>(vec.size()), sliceEnd);

    std::vector<T> result;
    if (step > 0) {
        for (int i = sliceStart; i < sliceEnd; i += step) {
            result.push_back(vec[i]);
        }
    } else if (step < 0) {
        for (int i = sliceStart; i > sliceEnd; i += step) {
            result.push_back(vec[i]);
        }
    }
    return result;
}
std::string sliceString(const std::string& str, int sliceStart, int sliceEnd, int step) {
    if (step == 0) {
        throw std::invalid_argument("Step cannot be zero.");
    }

    // Adjust negative indices
    if (sliceStart < 0) sliceStart += str.size();
    if (sliceEnd < 0) sliceEnd += str.size();

    // Ensure indices are within bounds
    if (step > 0) {
        sliceStart = std::max(0, sliceStart);
        sliceEnd = std::min(static_cast<int>(str.size()), sliceEnd);
    } else {
        sliceStart = std::min(static_cast<int>(str.size() - 1), sliceStart);
        sliceEnd = std::max(-1, sliceEnd);
    }

    std::string result;
    if (step > 0) {
        for (int i = sliceStart; i < sliceEnd; i += step) {
            result.push_back(str[i]);
        }
    } else if (step < 0) {
        for (int i = sliceStart; i > sliceEnd; i += step) {
            result.push_back(str[i]);
        }
    }
    return result;
}
std::vector<std::string> splitString(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string item;
    while (std::getline(ss, item, delimiter)) {
        result.push_back(item);
    }
    return result;
}
std::vector<std::string> splitStringWithString(const std::string& str, const std::string& delimiter) {
    std::vector<std::string> result;
    std::string copy = str;
    std::string item;
    size_t pos = 0;
    while ((pos = copy.find(delimiter)) != std::string::npos) {
        item = copy.substr(0, pos);
        result.push_back(item);
        copy.erase(0, pos + delimiter.length());
    }
    result.push_back(copy);
    return result;
}
std::vector<char> splitStringToChars(const std::string& str) {
    std::vector<char> result(str.begin(), str.end());
    return result;
}
char maxCharInString(const std::string &str)
{
    char maxChar = '\\0';
    for (char c : str)
    {
        if (c > maxChar)
        {
            maxChar = c;
        }
    }
    return maxChar;
}
std::string string_join(const std::vector<std::string> &vec, const std::string &delimiter)
{
    std::string result = "";
    for (const auto &item : vec)
    {
        result += item + delimiter;
    }
    result.resize(result.size() - delimiter.size());
    return result;
}
std::string string_strip(const std::string &str, const std::string &chars)
{
    std::string result = str;
    result.erase(0, result.find_first_not_of(chars));
    result.erase(result.find_last_not_of(chars) + 1);
    return result;
}
std::string string_toupper(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return result;
}
std::string string_tolower(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}
std::string string_replace(const std::string &str, const std::string &from, const std::string &to)
{
    std::string result = str;
    size_t start_pos = 0;
    while ((start_pos = result.find(from, start_pos)) != std::string::npos)
    {
        result.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return result;
}
int string_count(const std::string& str, const std::string& sub)
{
	if (sub.length() == 0) return 0;
	int count = 0;
	for (size_t offset = str.find(sub); offset != std::string::npos;
	offset = str.find(sub, offset + sub.length()))
	{
		++count;
	}
	return count;
}
int string_count_char(std::string s, char c) {
    int count = 0;

    for (int i = 0; i < s.size(); i++)
        if (s[i] == c) count++;

    return count;
}
bool string_isdigit(const std::string& str) {
    for (char ch : str) {
        if (!std::isdigit(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isalpha(const std::string& str) {
    for (char ch : str) {
        if (!std::isalpha(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isalnum(const std::string& str) {
    for (char ch : str) {
        if (!std::isalnum(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isascii(const std::string& str) {
    for (char ch : str) {
        if (!(ch >= 0 && ch <= 127)) {
            return false;
        }
    }
    return true;
}
bool string_isspace(const std::string& str) {
    for (char ch : str) {
        if (!std::isspace(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isupper(const std::string& str) {
    for (char ch : str) {
        if (!std::isupper(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_islower(const std::string& str) {
    for (char ch : str) {
        if (!std::islower(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
std::string userInput(std::string prompt="") {
    std::cout << prompt;
    std::string input;
    std::getline(std::cin, input);
    return input;
}
template <typename T, typename... Types>
std::string createJoinedStr(T var1, Types... var2)
{
    std::stringstream ss;
    ss << var1;
    (ss << ... << var2);
    return ss.str();
}
template <typename T>
std::vector<T> concatVec(std::vector<T> vec1, std::vector<T> vec2)
{
    vec1.insert(vec1.end(), vec2.begin(), vec2.end());
    return vec1;
}
template <typename T>
std::set<T> concatSet(std::set<T> set1, std::set<T> set2){
    set1.insert(set2.begin(), set2.end());
    return set1;
}
template <typename T, typename U>
std::map<T, U> concatMap(std::map<T, U> map1, std::map<T, U> map2){
    map1.insert(map2.begin(), map2.end());
    return map1;
}
template <typename T>
std::vector<T> repeatVec(std::vector<T> vec, int count) {
    std::vector<T> result;
    for (int i = 0; i < count; i++) {
        result.insert(result.end(), vec.begin(), vec.end());
    }
    return result;
}

"""
import sys
import os

input_file = ""
output_file = ""
compiler_options = []

for arg in sys.argv[1:]:
    if arg[0] == '-':
        compiler_options.append(arg[1:])
    else:
        if input_file == "":
            input_file = arg
        else:
            output_file = arg
print(compiler_options)
print(input_file, output_file)


if input_file == "" and output_file == "":
    print("Arguments: input_file output_file_name")
    print("options:")
    print("    --debug   prints the compiling process")
    sys.exit(1)
    
if input_file == output_file:
    print("input_file and output_file cannot be the same")

if output_file == "":
    output_file = os.path.splitext(input_file)[0] + ".cpp"

with open(sys.argv[1], 'r') as f:
    parsed = ast.parse(f.read().split("\n###END_PRELUDE###\n")[-1])
    
identifier_datatype_map = {}

additional_includes = assemble_to_string(compile_import_froms(parsed.body, identifier_datatype_map))
function_defs = assemble_to_string(compile_function_defs(parsed.body, identifier_datatype_map))

include_statements = f"""
#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <set>
#include <cmath>
#include <tuple>
#include <sstream>
#include <string>
#include <utility>
#include <type_traits>
#include <typeinfo>
#include <numeric>
#include <algorithm>

{additional_includes}
"""

template = f"""
{include_statements}
{additional_functions}
{functions_for_converting_to_string}
{function_defs}
""" + """
int main() {
""" + assemble_to_string(compile_body(parsed.body, identifier_datatype_map)) + """
    return 0;
}
"""
with open(output_file, 'w') as f:
    f.write(template)
    
print(f"Compiled {input_file} to {output_file}")
print(f"Compile {output_file} with: g++ {output_file} --std=c++17 (use c++17 or above)")
